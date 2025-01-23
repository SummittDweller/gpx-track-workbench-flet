# map.py
#

import streamlit as st
import constants as c
import functions as f
import os
import shutil
import subprocess as s
import WorkingGPX as WG
import inspect

# From https://github.com/JAlcocerT/Py_RouteTracker/blob/main/app.py
import folium
from streamlit_folium import st_folium
import gpxpy
import pandas as pd
from io import BytesIO
import pprint


# Define a function to load and display GPX route on the map
def PyLoadRoutes(hex_color):
    loaded = f.state('loaded')
    if not loaded or len(loaded) < 1:
        return
        
    route_info = []
    all_coordinates = []

    for track in loaded[0].gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                route_info.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation if hasattr(point, 'elevation') else None
                })

    route_df = pd.DataFrame(route_info)
    new_coordinates = [tuple(x) for x in route_df[['latitude', 'longitude', 'elevation']].to_numpy()]

    # # Append new coordinates to our array of all coordinates
    all_coordinates.append(new_coordinates)

    # Fetch the map center
    (clat, clon) = loaded[0].center
    
    # Clear the existing map
    m = folium.Map(
        location=[clat, clon],  # Adjust the initial map center here
        zoom_start=15,
        tiles='OpenStreetMap',
        width='100%',
        height=800
    )

    # # Create separate polylines for each distinct sublist of coordinates
    for sublist in all_coordinates:
        folium.PolyLine([coord[:2] for coord in sublist], weight=3, color=hex_color, tooltop=loaded[0].title).add_to(m)

    # Display the updated Folium map
    st_folium(m, returned_objects=[])
        
    # Save the map
    m.save("generated_map.html")


# map_gpx(st)
# -----------------------------------------------------------------------
def map_gpx(st):
    hex_color = st.sidebar.color_picker("Select Route Color", "#FF0000")  # Default to RED

    # # Initialize a global list to store coordinates and their respective file names
    # all_coordinates = []
    # file_names = []

    # # Create a Folium map
    # m = folium.Map(
    #     location=[42, -92],  # Adjust the initial map center here
    #     zoom_start=1,
    #     tiles='cartodb positron',
    #     width=924,
    #     height=600
    # )

    # # Display the Folium map using streamlit-folium
    # st_folium(m, returned_objects=[])

    # # Subtitle after the first map
    # st.write("## Initial map")

    PyLoadRoutes(hex_color)      # You can customize the color here



