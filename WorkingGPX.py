# Create the WorkingGPX and GPXList classes 

import streamlit as st
import functions as f
import constants as c
import gpxpy
import pandas as pd
from datetime import datetime
import os
import time
import json
import requests
from geopy.geocoders import Nominatim


# get_track_center - Calculate map center (lat, lon) from a gpxpy track object
# --------------------------------------------------------------------------------
def get_track_center(gpx):
    lats = []
    lons = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lats.append(point.latitude)
                lons.append(point.longitude)
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    return center_lat, center_lon


# get_datetime - Fetch the first <time> tag from a GPX and return a local datetime object
# --------------------------------------------------------------------------------
def get_datetime(gpx):
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                t = point.time
                local = t.astimezone( )  # Convert it to your local timezone (still aware)
                return local
    return False


# get_weather(lat, lon, dt) - Get historical weather data from 
# OpenWeatherMap.org for the location and time specified.
#-------------------------------------------------------------------------
def get_weather(lat, lon, dt):
    try:
        unix_time = int(time.mktime(dt.timetuple()))
        api_key = os.environ.get("OPEN_WEATHER_KEY", "Key Not Found!")
        api_url = c.OPEN_WEATHER_CALL.format(lat, lon, unix_time, api_key)
        # response = requests.get(api_url)
        # if response:
        #     weather = json.loads(response.text)
        #     d = weather['data'][0]
        #     w = d['weather'][0]
        #     return f"{w['main']} and {d['temp']}&deg;F (wind chill={d['feels_like']}) with {d['humidity']}% humidity and winds at {d['wind_speed']} mph."
        return f"Bogus clouds and -20&deg;F (wind chill=-30) with 200% humidity and winds at 20 mph."
    except Exception as e:
        print(f"Exception: {e}")
    return False


# identify_city(lat, lon) - Use the reverse_geocode library to identify where 
# (city) a particular lat,lon coordinate pair is on the Earth.
#-------------------------------------------------------------------------
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


# WorkingGPX Class
# ==============================================================================

class WorkingGPX(object):
    
    # Constructor
    def __init__(self, source):
        self.df = None
        self.gpx = None
        self.alias = None
        self.fullname = None
        self.datetime = None
        self.city = None
        self.weather = None
        self.mode = "Walking"       # Assumed.  Fix me!
        self.title = None
        self.weight = None
        self.Ym = None
        self.status = "Incomplete"
        
        # Identify what type of source we have
        t = type(source)
        # st.info(f"Constructor 'source' is type: {t}")

        # If source type is a Streamlit UploadedFile object...
        if t == st.runtime.uploaded_file_manager.UploadedFile:
            self.alias = source.name
            (df, gpx) = f.uploaded_to_working(st, source)
            if df.info and gpx:
                self.df = df
                self.gpx = gpx
                self.fullname = f.save_temp_gpx(st, gpx, self.alias)
                self.center = get_track_center(gpx)
                self.datetime = dt = get_datetime(gpx)
                self.city = identify_city(self.center[0], self.center[1])
                if self.city:
                    loc = f"in {self.city.replace(', Iowa', '')}"
                else: 
                    loc = ""
                self.weather = get_weather(self.center[0], self.center[1], dt)
                self.title = f"{dt.strftime("%a %b %d")} at {dt.strftime("%-l%p").lower()} - {self.mode} {loc}"
                self.weight = "-" + dt.strftime('%Y%m%d%H%M')
                self.Ym = '{}'.format(dt.strftime('%Y')) + '/' + '{}'.format(dt.strftime('%m'))
                self.status = "Constructed from UploadedFile"
            else:
                self.status = "Constructor Failed!"

        # All other sources... needs work!
        else:
            self.status = "Unknown 'source' type in Constructor"

    
    # Methods

    # update_from_df(df) - Given a GPX dataframe, update the corresponding WorkingGPX object
    # --------------------------------------------------------------------------------
    def update_from_df(self, df):
        self.df = df
        g = self.gpx = f.dataframe_to_gpx(df)
        self.center = get_track_center(g)
        self.datetime = get_datetime(g)
        with open(self.fullname, 'w') as wf:
            wf.write(g.to_xml( ))
        msg = f"WorkingGPX.update_from_df( ) has updated object '{self.title}' as '{self.fullname}'."
        f.state('logger').info(msg)
        # Store the new object in our GPXdict
        d = f.state('GPXdict')
        d.update(self)
        st.session_state.GPXdict = d
        return self


    # update_from_file(alias) - Given a GPX file, update the corresponding WorkingGPX object
    # --------------------------------------------------------------------------------
    def update_from_file(self, fullname):
        try:
            with open(fullname) as g:
                gpx_contents = g.read( )
                gpx = gpxpy.parse(gpx_contents)
        except Exception as e:
            st.exception(f"Exception: {e}")
            return False
        df = f.gpx_to_dataframe(st, gpx)
        if isinstance(df, pd.DataFrame) and gpx:
            self.fullname = fullname
            self.df = df
            self.gpx = gpx
            self.center = get_track_center(gpx)
            self.datetime = get_datetime(gpx)
            self.status = "Updated from GPX file {fullname}"
            # Store the new object in our GPXdict
            d = f.state('GPXdict')
            d.update(self)
            st.session_state.GPXdict = d
            return self
        else:
            st.error(f"Unable to update WorkingGPX[{self.alias}] from file {fullname}")
        return False



# def load_working(st, workingGPX):
#     gpx = False
#     working_path = workingGPX.fullname
#     try:
#         with open(working_path) as w:
#             gpx_contents = w.read( )
#             gpx = gpxpy.parse(gpx_contents)
#     except Exception as e:
#         st.exception(f"Exception: {e}")
#         return False
#     df = gpx_to_dataframe(st, gpx, working_path)
#     return (df, gpx)





        # g = self.gpx = f.dataframe_to_gpx(df)
        # self.center = get_track_center(g)
        # with open(self.fullname, 'w') as wf:
        #     wf.write(g.to_xml( ))
        # msg = f"WorkingGPX.update_from_df( ) has updated object '{self.alias}' as '{self.fullname}'."
        # f.state('logger').info(msg)
        # # Store the new object in our GPXdict
        # d = f.state('GPXdict')
        # d[self.alias] = self
        # st.session_state.GPXdict = d
        # return self


# GPXList Class
# ==============================================================================

class GPXList( ):
    
    # Constructor
    def __init__(self):
        self.list = dict( )

    # Methods
    # --------------------------------------------------------------------


    def update(self, object):
        self.list[object.title] = object
        count = len(self.list)
        return count


    def append(self, object):
        self.list[object.title] = object
        count = len(self.list)
        return count


    # print_GPXdict(st) - Print datafraes of all gox_list objects
    # ------------------------------------------------------------------------------------
    def print_GPXdict(self, st):
        Gd = f.state('GPXdict')
        if Gd:
            for key, WG in Gd.list.items( ):
                heading = f"{key} is {WG.fullname}"
                st.header(heading)
                st.write(WG.df)
        else:
            st.warning(f"print_GPXdict( ) called but there is no list to print")
