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
import json
import requests
from geopy.geocoders import Nominatim


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

    # Get the weather...
    weather = get_weather(g.center[0], g.center[1], g.datetime)

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
    md_file.write(f"weather: {weather}\n")
    md_file.write("---\n")
    md_file.write(leaflet_start + "\n")

    return md_file


# get_weather(lat, lon, dt) - Get historical weather data from 
# OpenWeatherMap.org for the location and time specified.
#-------------------------------------------------------------------------
def get_weather(lat, lon, dt):
    try:
        unix_time = int(time.mktime(dt.timetuple()))
        api_key = os.environ.get("OPEN_WEATHER_KEY", "Key Not Found!")
        api_url = c.OPEN_WEATHER_CALL.format(lat, lon, unix_time, api_key)
        response = requests.get(api_url)
        if response:
            weather = json.loads(response.text)
            d = weather['data'][0]
            w = d['weather'][0]
            return f"{w['main']} and {d['temp']}&deg;F (wind chill={d['feels_like']}) with {d['humidity']}% humidity and winds at {d['wind_speed']} mph."
    except Exception as e:
        print(f"Exception: {e}")
    return False


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
        msg = f"post_gpx(st) called with '{loaded[0].title}' as '{loaded[0].fullname}'"
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

