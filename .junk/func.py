# func.py
#

# Community packages
import re
import os
import datetime
import subprocess as s
import gpxpy 
import gpxpy.gpx
import shutil
import time
import requests
import json
from geopy.geocoders import Nominatim
from lxml import etree
import calendar

# Local imports...
import constant as c

#-------------------------------------------------------------------------
# get_weather(lat, lon, dt) - Get historical weather data from 
# OpenWeatherMap.org for the location and time specified.
def get_weather(lat, lon, dt):
  try:
    unix_time = int(time.mktime(dt.timetuple()))
    api_key = os.environ.get("OPEN_WEATHER_KEY", "Key Not Found!")
    api_url = c.OPEN_WEATHER_CALL.format(lat, lon, unix_time, api_key)
    response = requests.get(api_url)
    # print(response.json( ))
    return response
  except Exception as e:
    print(f"Exception: {e}")
  return False

#-------------------------------------------------------------------------
# Use the reverse_geocode library to identify where (city) a particular
# lat,lon coordinate pair is on the Earth.
def identify_city(lat, lon):
  geolocator = Nominatim(user_agent="gpx2hikes")
  coord = "{}, {}".format(lat, lon)
  try:
    location = geolocator.reverse(coord)
    address = location.raw['address']
    city = address.get('town','')
    if not city: 
      city = address.get('city','')
    state = address.get('state', '')
    country = address.get('country', '')

    if country == "United States":
      return "{}, {}".format(city, state)
    else:
      return "{}, {}".format(city, country)

    # result = reverse_geocode.search(coord)
    # if result[0]['country_code'] == "US":
    #   us = united_states.UnitedStates( )
    #   us_result = us.from_coords(lat, lon)
    #   city = result[0]['city'] + ", " + us_result[0]['name']
    # else:
    #   city = result[0]['city'] + ", " + result[0]['country']

  except Exception as e:
    print("Exception: { }".format(e))

  return False


#-------------------------------------------------------------------------
# Open a new GPX with a single track and segment
def open_new_gpx( ):
  try: 
    gpx = gpxpy.gpx.GPX( )
    gpx_track = gpxpy.gpx.GPXTrack( )
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment( )
    gpx_track.segments.append(gpx_segment)
  except Exception as e:
    print(f"Exception: {e}")

  return (gpx, gpx_segment)


#-------------------------------------------------------------------------
# Add a new point to an open GPX segment
def add_point(segment, lat, lon, elev, time):
  segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elev, time))


#-------------------------------------------------------------------------
# Save the current GPX file
def save_gpx(gpx, path, track_count, point_count):
  track_count += 1                       # increment the track_count and return it
  file = c.TEMP_DIR + c.TEMP_FILE
  try:
    s = gpx.to_xml(version="1.0")    # gpx as a string
    new_path = path.replace('.gpx', f'-{track_count}.gpx')
    with open(new_path, 'w') as new_file:
      new_file.write(s)
  except Exception as e:
    print(f"Exception: {e}")

  print(f'Saved new {point_count} single-track GPX at track {track_count} to {new_path}')
  return track_count

#-------------------------------------------------------------------------
# Process high-speed trkpts from a .gpx
def process_high_speed_trkpts(gpxData, trim):
  local_trim = trim
  path = c.TEMP_DIR + gpxData['new_name']
  gpx_file = open(path, 'r')

  # Parse the gpx file and prep for our loop
  gpx = gpxpy.parse(gpx_file)
  threshold = float(c.SPEED_THRESHOLD)
  skipping = False
  track_count = 0
  point_count = 0
  first = True

  # Adjust threshold based on track type, if available
  if 'type' in gpxData.keys( ):
    if gpxData['type'] == 'cycling':
      threshold = float(c.BIKE_SPEED_THRESHOLD)
      local_trim = False                           # do NOT trim bike rides!  

  # Open a new GPX to receive unskipped points from this GPX
  (new_gpx, new_segment) = open_new_gpx( )

  # Loop on tracks, segments and points
  for track in gpx.tracks:
    for segment in track.segments:
      for index, point in enumerate(segment.points):
        # if point.horizontal_dilution > c.HDOP_THRESHOLD:
        #   print(f'Point VDOP and HDOP are: {point.vertical_dilution} and {point.horizontal_dilution}')

        # If point is too speedy...
        if local_trim and point.speed and point.speed > threshold:
          # print(f'High-speed point ({point.speed} m/s) at ({point.latitude},{point.longitude}) -> {point.elevation}')
        
          # Got a speedy point. If we are not already skipping save what we have!
          if not skipping:
            if point_count > c.HIKE_POINTS_THRESHOLD:
              track_count = save_gpx(new_gpx, path, track_count, point_count)
            else:
              print(f'Small set (point count = {point_count}) of points was discarded.')

          # Make sure we start (or continue) skipping!
          skipping = True

        # Got a viable point under the speed threshold...
        else:
          if first:
            print(f'Got our first track point under the speed threshold. Identify the city.')
            city = identify_city(point.latitude, point.longitude)
            if city:
              gpxData['city'] = city
              print(f"Location has been identified as '{city}'.")
            else:
              print(f"Location could NOT be identified!")


            print(f"Query for the weather...")
            response = get_weather(point.latitude, point.longitude, point.time)
            if response:
              weather = json.loads(response.text)
              d = weather['data'][0]
              w = d['weather'][0]
              gpxData['weather'] = f"{w['main']} and {d['temp']}&deg;F (wind chill={d['feels_like']}) with {d['humidity']}% humidity and winds at {d['wind_speed']} mph."
              print(f"Weather response was positive and returned: {gpxData['weather']}.")
            else:
              print(f"Weather response was FALSE!")

            first = False
          
          # If we have been skipping, begin a new GPX
          if skipping:  
            (new_gpx, new_segment) = open_new_gpx( )
            point_count = 0

          # Add this point to the current GPX
          point_count += 1
          add_point(new_segment, point.latitude, point.longitude, point.elevation, point.time)

          # Make sure we stop skipping or continue to not skip!
          skipping = False

  # Loop is complete, save the last track segment if it has points
  if point_count > c.HIKE_POINTS_THRESHOLD:
    track_count = save_gpx(new_gpx, path, track_count, point_count)
  else:
    print(f'Small set (point count = {point_count}) of points was discarded.')

  # Save the track info in GPXData
  gpxData['track_count'] = track_count      


#-------------------------------------------------------------------------
# Run a GPSBabel command and print output
def gpsBabel(command):
  try:
    result = s.run(command, cwd=c.TEMP_DIR, shell=True, capture_output=True, text=True)
    print('\n')
    print("Running subprocess command: '{}'.".format(command))
    print("  stdout: {}".format(result.stdout))
    print("  stderr: {}".format(result.stderr))
    return True
  except Exception as e:
    print('Exception: {}\n'.format(e))  
    return False


#-------------------------------------------------------------------------
# GPSBabel command to add <speed> tags to trkpts and save to same file
def gpsBabel_add_speed(gpxData):
  import shutil
  parts = [ 'gpsbabel', '-t', '-i', 'gpx', '-f', gpxData['new_name'], '-x', 'track,speed', '-o', 'gpx,gpxver=1.0', '-F', c.TEMP_FILE ]
  command = ' '.join(parts)
  if gpsBabel(command):
    shutil.move(c.TEMP_FILE, gpxData['new_name'])


#-------------------------------------------------------------------------
# GPSBabel command to combine tracks from two files into one
# Example: gpsbabel -i geo -f 1.loc -i gpx -f 2.gpx -i pcx 3.pcx -o gpsutil -F big.gps
def gpsBabel_merge_files(path1, path2):
  new_name = c.TEMP_DIR + c.TEMP_FILE
  parts = [ 'gpsbabel', '-i', 'gpx', '-f', path1.replace(' ','\ '), '-i', 'gpx', '-f', path2.replace(' ','\ '), '-o', 'gpx', '-F', new_name ]
  command = ' '.join(parts)
  if gpsBabel(command):
    return new_name 


#-------------------------------------------------------------------------
# combine_gpxFiles - Combine two GPX files into one
def combine_gpxFiles(gpx1, gpx2):
  import shutil

  print("Combine files {} --> {}".format(gpx1['new_name'], gpx2['new_name']))
  gpx1['ignore'] = True
  gpx2['combined'] = True
  new_name = gpsBabel_merge_files(gpx1['new_name'], gpx2['new_name'])
  if new_name:
    shutil.copyfile(new_name, gpx2['new_name'])
  return new_name


#-------------------------------------------------------------------------
# make_markdown - Make a Markdown file to represent GPX tracks
def make_markdown(gpxData):
  gpx_name = gpxData['new_name']
  md_name = gpx_name.replace('.gpx','.md')
  title = md_name[0:-3]                       # drop .md for the Markdown title
  pubDate = gpxData['date']
  pubTime = gpxData['time']

  # Open the new .md file
  md_dir = c.CONTENT_HIKES_DIR + gpxData['Ym'] + '/'
  try:
    os.mkdir(md_dir)
  except FileExistsError:
    pass
  except Exception as e:
    print(f'Exception: {e}')  

  # Open a new .md file IF it does not already exist  
  try:
    md_file = open(md_dir + md_name, 'x')
  except FileExistsError:
    print(f"Markdown file {md_dir + md_name} already exists and will not be replaced!")
    return False

  leaflet_start = '{{< leaflet-map mapHeight="500px" mapWidth="100%" >}}'

  bike = 'False'
  type = 'Unspecified'
  if 'type' in gpxData.keys( ):
    type = gpxData['type']  
    if type == 'cycling':
      bike = 'True'

  # Write it line-by-line
  md_file.write("---\n")
  md_file.write(f"title: {title}\n")
  md_file.write(f"weight: {gpxData['weight']}\n")
  md_file.write(f"publishDate: {pubDate}\n")
  # md_file.write(f"last_modified_at: {lastMod}\n")
  if 'city' in gpxData.keys( ):
    md_file.write(f"location: {gpxData['city']}\n")
  md_file.write("highlight: false\n")
  md_file.write(f"bike: {bike}\n")
  md_file.write(f"trackType: {type}\n")
  md_file.write("trashBags: false\n")
  md_file.write("trashRecyclables: false\n")
  md_file.write("trashWeight: false\n")
  if 'weather' in gpxData.keys( ):
    md_file.write(f"weather: {gpxData['weather']}\n")
  md_file.write("---\n")
  md_file.write(leaflet_start + "\n")

  return md_file


#-------------------------------------------------------------------------
# add_track_to_markdown - Add a track to the open Markdown file
def add_track_to_markdown(gpxData, counter, md_file):
  from random import randint

  gpx_name = gpxData['new_name']
  Ym = gpxData['Ym']
  color = c.COLOR_PALETTE[0]

  if counter > 0:
    gpx_name = gpx_name.replace('.gpx', '-{}.gpx'.format(counter))
    color = c.COLOR_PALETTE[counter % 9]

    # Write the .md track reference if the md_file is open
    if md_file:
      leaflet_track = '  {{< leaflet-track trackPath="' + Ym + "/" + gpx_name + '" lineColor=" ' + color + '" lineWeight="5" graphDetached=True >}}'
      md_file.write(leaflet_track + '\n');

    # Copy the .gpx file to c.STATIC_GPX_DIR year/month subdirectory
    gpx_dir = c.STATIC_GPX_DIR + Ym + '/'

    try:
      os.mkdir(gpx_dir)
    except FileExistsError:
      pass
    except Exception as e:
      print(f'Exception: {e}')

    try:
      shutil.copy(c.TEMP_DIR + gpx_name, gpx_dir + gpx_name)
    except FileExistsError:
      pass
    except Exception as e:
      print(f'Exception: {e}')

  return md_file


#-------------------------------------------------------------------------
# make_gpxData - Return a new gpxData structure including:
#   raw_name, new_name, date_time_obj, Ym, weight, type, and stage
#
def make_gpxData(filepath):
  gpxData = { }
  name = os.path.basename(filepath)
  # pattern = re.compile('(\d{4}-\d{2}-\d{2}) (\d{2}).(\d{2}) - (.*).gpx')
  # pattern = re.compile('\w+ (\d{4}-\d{2}-\d{2})T(\d{2})(\d{2})\d{2}Z.gpx')
  # pattern = re.compile('\w+ (\d{4}-\d{2}-\d{2}T\d{2}\d{2})\d{2})Z.gpx')
  pattern = re.compile('\w+ (\d{4}-\d{2}-\d{2}T\d{6})Z.gpx')

  try:
    m = pattern.match(name)
  except: 
    return False
  
  if not m:
    return False

  gpxData['raw_name'] = filepath

  # Build a datatime object from the filename
  d = datetime.datetime.strptime(m.group(1), "%Y-%m-%dT%H%M%S") 
  d = d.replace(tzinfo=datetime.timezone.utc) 
  date_time_object = d.astimezone( )  #Convert it to your local timezone (still aware)
  
  # dt = m.group(1)
  # utc_time = time.strptime("dt", "%Y-%m-%dT%H%M%S")
  # utc_seconds = calendar.timegm(utc_time)
  # local_time = time.localtime(utc_seconds)

  # yyyymmdd = m.group(1)
  # hh = m.group(2)
  # mm = m.group(3)
  # # remainder = m.group(4).replace(' ','')  
  # date_time_str = "{}T{}:{}".format(yyyymmdd, hh, mm)
  # date_time_object = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')  

  gpxData['date_time_obj'] = date_time_object

  # Build a new filename from the date_time_object
  gpxData['new_name'] = date_time_object.strftime("%Y-%m-%d_%I:%M%p.gpx").lower( )

  # Build the year/month directory name for the file
  Ym = date_time_object.strftime('%Y/%m')
  gpxData['Ym'] = Ym

  # Calculate the negative "weight" of this new .md file based on the date.
  weight = "-" + date_time_object.strftime('%Y%m%d%H%M')
  gpxData['weight'] = weight

  # Save some key data
  gpxData['stage'] = 'renamed'
  gpxData['date'] = '{}'.format(date_time_object.strftime('%Y-%m-%d'))
  
  gpxData['time'] = '{}:{}'.format(date_time_object.strftime('%H'), date_time_object.strftime('%M'))
  gpxData['type'] = None

  # # Open the GPX with lxml and find the <type> tag, add value to gpxData
  # root = etree.parse(c.RAW_GPX_DIR + filepath)
  # for e in root.getiterator( ):
  #   simple_tag = etree.QName(e.tag).localname
  #   if simple_tag == 'type':                        # got the track type
  #     gpxData['type'] = e.text.strip( )
  #     break


  # Get the <type> from the .gpx filename
  if "Walking" in filepath:
    gpxData['type'] = 'walking'
  elif "Cycling" in filepath:
    gpxData['type'] = 'cycling'
  else:
    gpxData['type'] = 'unkknown'  


  # Print key data just for luck
  print("\n")
  print(f"New file name: {gpxData['new_name']}")
  print(f"  Raw file name: {gpxData['raw_name']}")
  print(f"  Type: {gpxData['type']}")
  print(f"  Datetime Object: {gpxData['date_time_obj']}")
  print(f"  Y/m Directory Name: {gpxData['Ym']}")
  print(f"  Weight (for sorting): {gpxData['weight']}")
  print(f"  Stage: {gpxData['stage']}")

  return gpxData
  
