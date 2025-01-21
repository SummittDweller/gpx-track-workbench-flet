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


# make_gpxData - Return a new gpxData structure including:
#   raw_name, date_time_obj, Ym, weight, type, and stage
#-------------------------------------------------------------------------
def make_gpxData(st, filepath):
    gpxData = { }
    name = os.path.basename(filepath)
    # # pattern = re.compile('(\d{4}-\d{2}-\d{2}) (\d{2}).(\d{2}) - (.*).gpx')
    # # pattern = re.compile('\w+ (\d{4}-\d{2}-\d{2})T(\d{2})(\d{2})\d{2}Z.gpx')
    # # pattern = re.compile('\w+ (\d{4}-\d{2}-\d{2}T\d{2}\d{2})\d{2})Z.gpx')
    pattern = re.compile('\w+_(\d{4}-\d{2}-\d{2}t\d{6})z.gpx')

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
    gpxData['date_time_obj'] = date_time_object

    # # Build a new filename from the date_time_object
    # gpxData['new_name'] = date_time_object.strftime("%Y-%m-%d_%I:%M%p.gpx").lower( )

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

    # Get the <type> from the .gpx filename
    if "walking" in filepath:
        gpxData['type'] = 'walking'
    elif "cycling" in filepath:
        gpxData['type'] = 'cycling'
    else:
        gpxData['type'] = 'unkknown'  

    # Print key data just for luck
    st.info(f"Raw file name: {gpxData['raw_name']}")
    st.info(f"  Type: {gpxData['type']}")
    st.info(f"  Datetime Object: {gpxData['date_time_obj']}")
    st.info(f"  Y/m Directory Name: {gpxData['Ym']}")
    st.info(f"  Weight (for sorting): {gpxData['weight']}")
    st.info(f"  Stage: {gpxData['stage']}")

    return gpxData


# make_markdown - Make a Markdown file to represent GPX tracks
#-------------------------------------------------------------------------
def make_markdown(st, gpxData):
    gpx_name = os.path.basename(gpxData['raw_name'])
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

    # Open a new .md file IF it exists or not  
    try:
        md_file = open(md_dir + md_name, 'w')
    except FileExistsError:
        print(f"Markdown file {md_dir + md_name} already exists and will be replaced!")
        pass

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


# add_track_to_markdown - Add GPX reference to the open Markdown file
#-------------------------------------------------------------------------
def add_track_to_markdown(st, gpxData, md_file):
    from random import randint

    gpx_name = os.path.basename(gpxData['raw_name'])
    Ym = gpxData['Ym']

    # Write the .md track reference if the md_file is open
    if md_file:
        # leaflet_track = '  {{< leaflet-track trackPath="' + Ym + "/" + gpx_name   #  + '" lineColor=" ' + color + '" lineWeight="5" graphDetached=True >}}'
        leaflet_track = '  {{' + f"< leaflet-track trackPath='{Ym}/{gpx_name}" + "' >}}"
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

    for index, g in enumerate(loaded):
        gpxData = make_gpxData(st, g.fullname)   # build GPX file data structure
        md = make_markdown(st, gpxData)
        add_track_to_markdown(st, gpxData, md)
        # Close the Markdown file 
        if md:
            md.write('{{< /leaflet-map >}}\n')
            md.write(' ')
            md.close( )

    return

