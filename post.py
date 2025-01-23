# post.py
#

import streamlit as st
import constants as c
import functions as f
import os
import shutil
import subprocess as sub
import WorkingGPX as WG
import time
import datetime
import re
import requests
from geopy.geocoders import Nominatim


# # get_weather(lat, lon, dt) - Get historical weather data from 
# # OpenWeatherMap.org for the location and time specified.
# #-------------------------------------------------------------------------
# def get_weather(lat, lon, dt):
#     try:
#         unix_time = int(time.mktime(dt.timetuple()))
#         api_key = os.environ.get("OPEN_WEATHER_KEY", "Key Not Found!")
#         api_url = c.OPEN_WEATHER_CALL.format(lat, lon, unix_time, api_key)
#         response = requests.get(api_url)
#         # print(response.json( ))
#         return response
#     except Exception as e:
#         print(f"Exception: {e}")
#     return False


# # identify_city(lat, lon) - Use the reverse_geocode library to identify where 
# # (city) a particular lat,lon coordinate pair is on the Earth.
# #-------------------------------------------------------------------------
# def identify_city(lat, lon):
#     geolocator = Nominatim(user_agent="gpx2hikes")
#     coord = "{}, {}".format(lat, lon)
#     try:
#         location = geolocator.reverse(coord)
#         address = location.raw['address']
#         city = address.get('town','')
#         if not city: 
#             city = address.get('city','')
#         state = address.get('state', '')
#         country = address.get('country', '')

#         if country == "United States":
#             return "{}, {}".format(city, state)
#         else:
#             return "{}, {}".format(city, country)

#         # result = reverse_geocode.search(coord)
#         # if result[0]['country_code'] == "US":
#         #   us = united_states.UnitedStates( )
#         #   us_result = us.from_coords(lat, lon)
#         #   city = result[0]['city'] + ", " + us_result[0]['name']
#         # else:
#         #   city = result[0]['city'] + ", " + result[0]['country']

#     except Exception as e:
#         print("Exception: { }".format(e))

#     return False


# # make_gpxData - Return a new gpxData structure including:
# #   raw_name, date_time_obj, Ym, weight, type, and stage
# #-------------------------------------------------------------------------
# def make_gpxData(st, filepath):
#     gpxData = { }
#     name = os.path.basename(filepath)
#     # # pattern = re.compile('(\d{4}-\d{2}-\d{2}) (\d{2}).(\d{2}) - (.*).gpx')
#     # # pattern = re.compile('\w+ (\d{4}-\d{2}-\d{2})T(\d{2})(\d{2})\d{2}Z.gpx')
#     # # pattern = re.compile('\w+ (\d{4}-\d{2}-\d{2}T\d{2}\d{2})\d{2})Z.gpx')
#     pattern = re.compile('\w+_(\d{4}-\d{2}-\d{2}t\d{6})z.gpx')

#     try:
#         m = pattern.match(name)
#     except: 
#         return False
#     if not m:
#         return False

#     gpxData['raw_name'] = filepath

#     # Build a datatime object from the filename
#     d = datetime.datetime.strptime(m.group(1), "%Y-%m-%dt%H%M%S") 
#     d = d.replace(tzinfo=datetime.timezone.utc) 
#     date_time_object = d.astimezone( )  #Convert it to your local timezone (still aware)
#     gpxData['date_time_obj'] = date_time_object

#     # # Build a new filename from the date_time_object
#     # gpxData['new_name'] = date_time_object.strftime("%Y-%m-%d_%I:%M%p.gpx").lower( )

#     # Build the year/month directory name for the file
#     Ym = date_time_object.strftime('%Y/%m')
#     gpxData['Ym'] = Ym

#     # Calculate the negative "weight" of this new .md file based on the date.
#     weight = "-" + date_time_object.strftime('%Y%m%d%H%M')
#     gpxData['weight'] = weight

#     # Save some key data
#     gpxData['stage'] = 'renamed'
#     gpxData['date'] = '{}'.format(date_time_object.strftime('%Y-%m-%d'))
  
#     gpxData['time'] = '{}:{}'.format(date_time_object.strftime('%H'), date_time_object.strftime('%M'))
#     gpxData['type'] = None

#     # Get the <type> from the .gpx filename
#     if "walking" in filepath:
#         gpxData['type'] = 'walking'
#     elif "cycling" in filepath:
#         gpxData['type'] = 'cycling'
#     else:
#         gpxData['type'] = 'unknown'  

#     # Get the weather and location (city)
#     weather = get_weather(g.center[0], g.center[1], g.datetime)
#     city = identify_city(g.center[0], g.center[1])


#     # Print key data just for luck
#     st.info(f"Raw file name: {gpxData['raw_name']}")
#     st.info(f"  Type: {gpxData['type']}")
#     st.info(f"  Datetime Object: {gpxData['date_time_obj']}")
#     st.info(f"  Y/m Directory Name: {gpxData['Ym']}")
#     st.info(f"  Weight (for sorting): {gpxData['weight']}")
#     st.info(f"  Stage: {gpxData['stage']}")

#     return gpxData


# make_markdown - Make a Markdown file to represent GPX tracks
#-------------------------------------------------------------------------
def make_markdown(st, g):
    gpx_name = os.path.basename(g.fullname)
    md_name = gpx_name.replace('.gpx','.md')

    pubDate = '{}'.format(g.datetime.strftime('%Y-%m-%d'))
    pubTime = '{}:{}'.format(g.datetime.strftime('%H'), g.datetime.strftime('%M'))

    # Open the new .md file
    pubDate = '{}'.format(g.datetime.strftime('%Y-%m-%d'))

    md_dir = c.CONTENT_HIKES_DIR + g.Ym + '/'
    try:
        os.makedirs(md_dir, exist_ok=True)
    except FileExistsError:
        pass
    except Exception as e:
        print(f'Exception: {e}')  

    # Open a new .md file IF it exists or not  
    try:
        md_file = open(md_dir + md_name, 'w')
    except FileExistsError:
        print(f"Markdown file {md_dir + md_name} already exists and will be replaced!")
        pass

    leaflet_start = '{{< leaflet-map mapHeight="500px" mapWidth="100%" >}}'

    if g.mode == 'Cycling':
        bike = 'True'
    else:
        bike = 'False'

    # Write it line-by-line
    md_file.write("---\n")
    md_file.write(f"title: {g.title}\n")
    md_file.write(f"weight: {g.weight}\n")
    md_file.write(f"publishDate: {pubDate}\n")
    md_file.write(f"location: {g.city}\n")
    md_file.write("highlight: false\n")
    md_file.write(f"bike: {bike}\n")
    md_file.write(f"trackType: {g.mode}.lower( )\n")
    md_file.write("trashBags: false\n")
    md_file.write("trashRecyclables: false\n")
    md_file.write("trashWeight: false\n")
    md_file.write(f"weather: {g.weather}\n")
    md_file.write("---\n")
    md_file.write(leaflet_start + "\n")

    return md_file


# add_track_to_markdown - Add GPX reference to the open Markdown file
#-------------------------------------------------------------------------
def add_track_to_markdown(st, g, md_file):
    from random import randint

    gpx_name = os.path.basename(g.fullname)
    Ym = g.Ym

    # Write the .md track reference if the md_file is open
    if md_file:
        # leaflet_track = '  {{< leaflet-track trackPath="' + Ym + "/" + gpx_name   #  + '" lineColor=" ' + color + '" lineWeight="5" graphDetached=True >}}'
        leaflet_track = '  {{' + f'< leaflet-track trackPath="{g.Ym}/{gpx_name}"' + ' lineColor=#c838d1 lineWeight="5" graphDetached=True >}}'
        md_file.write(leaflet_track + '\n');

        # Copy the .gpx file to c.STATIC_GPX_DIR year/month subdirectory
        gpx_dir = c.STATIC_GPX_DIR + g.Ym + '/'

        try:
            os.makedirs(gpx_dir, exist_ok=True)
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


# post_gpx(st)
# -----------------------------------------------------------------------
def post_gpx(st):
    loaded = f.state('loaded')
    if not loaded:
        return
    
    # Set the time zone ------------------------
    os.environ['TZ'] = c.TIME_ZONE
    time.tzset( )

    # This is a file operation, so no dataframe or GPX file handling needed here.
    num = len(loaded)
    if num == 1:
        msg = f"post_gpx(st) called with '{loaded[0].alias}' as '{loaded[0].fullname}'"
    else:
        msg = f"post_gpx(st) called with {num} loaded GPX"
    st.write(msg)
    f.state('logger').info(msg)

    # Loop on loaded GPX
    for index, g in enumerate(loaded):
        # gpxData = make_gpxData(st, g.fullname)   # build GPX file data structure
        md = make_markdown(st, g)
        add_track_to_markdown(st, g, md)
        # Close the Markdown file 
        if md:
            md.write('{{< /leaflet-map >}}\n')
            md.write(' ')
            md.close( )

    return

