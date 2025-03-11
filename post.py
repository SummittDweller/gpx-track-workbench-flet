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
import openmeteo_requests
import requests_cache
import pandas as pd
from datetime import datetime, timedelta
from retry_requests import retry
from geopy.geocoders import Nominatim
import pytz


# make_markdown - Make a Markdown file to represent GPX tracks
#-------------------------------------------------------------------------
def make_markdown(st, g):
    gpx_name = os.path.basename(g.fullname)
    md_name = gpx_name.replace('.gpx','.md')

    pubDate = '{}'.format(g.datetime.strftime('%Y-%m-%d'))
    pubTime = '{}:{}'.format(g.datetime.strftime('%H'), g.datetime.strftime('%M'))

    # Open the new .md file
    pubDate = '{}'.format(g.datetime.strftime('%Y-%m-%d'))

    md_dir = os.environ.get('HOME') + c.CONTENT_HIKES_DIR + g.Ym + '/'
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
    md_file.write(f"location: {g.place}\n")
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


# def calculate_timezone_offset(lat: float, lng: float, dt: datetime) -> float:
#     """
#     Calculates the timezone offset in hours for a given latitude, longitude, and datetime.

#     Args:
#         lat: Latitude.
#         lng: Longitude.
#         dt: Datetime object.

#     Returns:
#         Timezone offset in hours.
#     """
#     tf = TimezoneFinder( )
#     timezone_str = tf.timezone_at(lng=lng, lat=lat)

#     if timezone_str is None:
#         raise ValueError("Could not determine timezone for the given coordinates.")

#     timezone = pytz.timezone(timezone_str)
#     localized_dt = timezone.localize(dt, is_dst=None)
#     utc_dt = localized_dt.astimezone(pytz.utc)

#     offset_seconds = (dt - utc_dt).total_seconds()
#     offset_hours = offset_seconds / 3600
#     return offset_hours


def calculate_wind_chill(temp_fahrenheit, wind_speed_mph):
    """
    Calculates the wind chill temperature in Fahrenheit.

    Args:
        temp_fahrenheit: The air temperature in degrees Fahrenheit.
        wind_speed_mph: The wind speed in miles per hour.

    Returns:
        The wind chill temperature in degrees Fahrenheit.
        Returns None if inputs are outside the valid range.
    """
    if temp_fahrenheit > 50 or wind_speed_mph < 3:
        return temp_fahrenheit      # Wind chill is not defined for these conditions

    wind_chill = 35.74 + (0.6215 * temp_fahrenheit) - (35.75 * (wind_speed_mph ** 0.16)) + (0.4275 * temp_fahrenheit * (wind_speed_mph ** 0.16))

    return wind_chill


# get_weather(lat, lon, dt) - Get historical weather data from open-meteo.com for the location and local time specified.  
# See https://open-meteo.com/en/docs/historical-weather-api
#-------------------------------------------------------------------------
def get_weather(lat, lon, dt):

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "past_days": 92,
        "forecast_days": 1,
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly( )
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy( )
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy( )
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy( )
    hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy( )

    hourly_data = { "date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    ) }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

    df = pd.DataFrame(data = hourly_data)
    # print(df)            
    
    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Set 'date' column as index
    df = df.set_index('date')

    # Get equiv UTC datetime
    utc_dt = dt.astimezone(pytz.utc)

    specific_date = utc_dt.strftime("%Y-%m-%d %H:00:00+00:00")
    
    try:
        selected_rows_specific_date = df.loc[specific_date]
    except Exception as e:
        print(f'Exception: {e}')
        return False

    # print(selected_rows_specific_date)
    
    temp = selected_rows_specific_date['temperature_2m']
    wind = selected_rows_specific_date['wind_speed_10m']
    humid = selected_rows_specific_date['relative_humidity_2m']
    precip = selected_rows_specific_date['precipitation']

    wc = calculate_wind_chill(temp, wind)

    return f"{temp:.1f}&deg;F (wind chill={wc:.1f}) with {humid:.1f}% humidity and winds at {wind:.1f} mph. Hourly precipitation of {precip:.2f} inches."


# # get_weather(lat, lon, dt) - Get historical weather data from 
# # OpenWeatherMap.org for the location and time specified.
# #-------------------------------------------------------------------------
# def get_weather(lat, lon, dt):
#     try:
#         unix_time = int(time.mktime(dt.timetuple()))
#         api_key = os.environ.get("OPEN_WEATHER_KEY", "Key Not Found!")
#         api_url = c.OPEN_WEATHER_CALL.format(lat, lon, unix_time, api_key)
#         response = requests.get(api_url)
#         if response:
#             weather = json.loads(response.text)
#             d = weather['data'][0]
#             w = d['weather'][0]
#             return f"{w['main']} and {d['temp']}&deg;F (wind chill={d['feels_like']}) with {d['humidity']}% humidity and winds at {d['wind_speed']} mph."
#         return f"Weather request returned a negative response."
#     except Exception as e:
#         print(f"Exception: {e}")
#     return f"Weather data is not available."


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
        gpx_dir = os.environ.get('HOME') + c.STATIC_GPX_DIR + g.Ym + '/'

        try:
            os.makedirs(gpx_dir, exist_ok=True)
        except FileExistsError:
            pass
        except Exception as e:
            print(f'Exception: {e}')

        try:
            shutil.copy(os.environ.get('HOME') + c.TEMP_DIR + gpx_name, gpx_dir + gpx_name)
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

