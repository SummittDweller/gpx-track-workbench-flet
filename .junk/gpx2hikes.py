# main.py
#

import os
import sys
import time
import glob
import getopt
import shutil
from datetime import datetime, timedelta

# Local packages
import constant as c
import func as f

##-----------------------------------------------------------------------------------------
## gpx2hikes.py
##

# Set the time zone ------------------------
os.environ['TZ'] = c.TIME_ZONE
time.tzset( )

#----------------------------------------------------------------
# Process command line args 
# per https://www.tutorialspoint.com/python/python_command_line_arguments.htm
#
args = sys.argv[1:]

print('\n')
print('Number of arguments: {}'.format(len(args)))
print('Argument list: {}'.format(str(args)))

combine = False
trim = False

try:
  opts, args = getopt.getopt(args, 'hct', ["help", "combine", "trim"])
except getopt.GetoptError:
  print("gpx2hikes --help --combine --trim \n")
  sys.exit(2)

for opt, arg in opts:
  if opt in ("-h", "--help"):
    print("gpx2hikes --help --combine --trim \n")
    sys.exit()
  elif opt in ("-c", "--combine"):
    combine = True
  elif opt in ("-t", "--trim"):
    trim = True
  else:
    assert False, "Unhandled option"
  
print("Combine: {}".format(combine))
print("Trim: {}".format(trim))

#--------------------------------------------------------------------------
# Make the c.TEMP_DIR directory if needed
try:
  os.mkdir(c.TEMP_DIR)
except Exception as e:
  print("Exception: {}\n".format(e)) 

#--------------------------------------------------------------------------
# Save the current working directory and 'cd' into c.TEMP_DIR for all
# future operations
cwd = os.getcwd( )
os.chdir(c.TEMP_DIR)  

#--------------------------------------------------------------------------
# Glob up all the FILENAME_PATTERN .gpx files in the raw GPX directory for processing
gpxFiles = glob.glob(c.FILENAME_PATTERN, root_dir=c.RAW_GPX_DIR)
print("List of GPX files to examine in {}: {}\n".format(c.RAW_GPX_DIR, gpxFiles))

#--------------------------------------------------------------------------
# Loop on all the gpxFiles sorted in chronological order and build a 
# sorted list, gpxData_list, in c.TEMP_DIR with no spaces in the names
try:
  gpxFiles.sort(key=lambda x: datetime.strptime(x[8:-4], '%Y-%m-%dT%H%M'))
except Exception as e:
  assert("Exception: {}\n".format(e))  

gpxData_list = [ ]

for index, file in enumerate(gpxFiles):     # now in sorted order
  gpxData = f.make_gpxData(file)   # build GPX file data structure
  if gpxData:
    gpxData_list.append(gpxData)
    shutil.copy(c.RAW_GPX_DIR + file, gpxData['new_name'])

print('\n')

#-----------------------------------------------------------------------
# Loop on all the new GPX files in chronological order.  If consecutive 
# files are timestamped within TWO hours of each other, combine them using GPSBabel
# Do NOT combine files of different type, like walking with cycling!

previous_dt = False
previous_type = False

for index, file in enumerate(gpxData_list):
  type = False
  dt = file['date_time_obj']
  if 'type' in file.keys( ):
    type = file['type']  
  if previous_dt:
    diff = dt - previous_dt
    delta = timedelta(hours=c.TIME_DELTA_THRESHOLD)
    if diff < delta and type == previous_type:
      print("\nFile timestamp difference is less than {} hours. Combine the files!".format(c.TIME_DELTA_THRESHOLD))
      result = f.combine_gpxFiles(gpxData_list[index-1], gpxData_list[index])
  previous_dt = dt
  previous_type = type

#-------------------------------------------------------------------------
# Run GPSBabel on each of the GPX files to add <speed> tags in meters/sec
# Example: gpsbabel -t -i gpx -f input.gpx -x track,speed -o gpx -F output.gpx

for index, gpxData in enumerate(gpxData_list):     
  try:
    f.gpsBabel_add_speed(gpxData)
  except Exception as e:
    assert("Exception: {}\n".format(e))

#-------------------------------------------------------------------------
# Run process_high_speed_trkpts on each of the NOT ignored files to remove 
# points based on <speed>

for index, gpxData in enumerate(gpxData_list):     
  if not 'ignore' in gpxData.keys( ):
    try:
      num_tracks = f.process_high_speed_trkpts(gpxData, trim)
    except Exception as e:
      print("Exception: { }\n".format(e))
      assert( )

#-------------------------------------------------------------------------
# Ok, we are ready to generate some Markdown (.md) files now...
md_file = False

for gpxData in gpxData_list:     
  if 'track_count' in gpxData.keys( ):
    if gpxData['track_count'] > 0:
      try:
        md_file = f.make_markdown(gpxData)
      except Exception as e:
        print("Exception: {}\n".format(e))
        assert( )
    
    for x in reversed(range(1, gpxData['track_count']+1)):
      f.add_track_to_markdown(gpxData, x, md_file)
    
    # Close the Markdown file if track_count > 0
    if md_file and gpxData['track_count'] > 0:
      md_file.write('{{< /leaflet-map >}}\n')
      md_file.write(' ')
      md_file.close( )

  # GPX has NO track_points
  else:  
    print(f"GPX file {gpxData['new_name']} has NO track points.  It will be ignored!")

# All done, delete the c.TEMP_DIR directory and its contents
try:
  shutil.rmtree(c.TEMP_DIR)
except OSError as e:
  print(f"Error: {c.TEMP_DIR} : {e.strerror}")

# Move (cd) back where we started
os.chdir(cwd)  