# GPX-Track-Workbench/app.py

import constants as c
import functions as f
import uploader as u
# import map as m
# import speed as s

# import os 
# import shutil
import streamlit as st
from loguru import logger
from streamlit_option_menu import option_menu
# from st_click_detector import click_detector as did_click
import WorkingGPX as wgpx
# import pprint
# import time

# From https://github.com/JAlcocerT/Py_RouteTracker/blob/main/app.py
# import folium
# from streamlit_folium import st_folium
# import gpxpy
# import pandas as pd
# from io import BytesIO


# on_change(key) - Define the menu's on_change callback
# ------------------------------------------------------------------------------------------
def on_change(key):
    selection = st.session_state[key]
    st.success(f"Selection changed to: {selection}")

    # Act on the selected key
    match selection:
        case c.HOME:
            st.warning("HOME not available")
        case c.UPLOAD:
            st.warning("UPLOAD not available")
        case c.EDIT:
            st.warning("EDIT not availabe")
        case c.MAP:
            st.warning("MAP not available")
        case c.SPEED:
            st.warning("SPEED not available")
        case c.POST:
            st.warning("POST not available")
        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            st.error("Something's wrong in on_change( )")


# MAIN ---------------------------------------------------------

# Create the sidebar menu
with st.sidebar:
    selected = option_menu("GPX Track Workbench", [ c.HOME, c.UPLOAD, c.EDIT, c.MAP, c.SPEED, c.POST ], 
    icons=['house-fill', 'cloud-upload-fill', 'pencil', 'map', 'speedometer', 'signpost-split'], 
    menu_icon="cast", default_index=0, on_change=on_change, key='main_menu')    

# Do some things in the main area
st.write(selected)

# # 3. CSS style definitions
# selected3 = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
#     icons=['house', 'cloud-upload', "list-task", 'gear'], 
#     menu_icon="cast", default_index=0, orientation="horizontal",
#     styles={
#         "container": {"padding": "0!important", "background-color": "#fafafa"},
#         "icon": {"color": "orange", "font-size": "25px"}, 
#         "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "green"},
#     }
# )

# # 4. Manual item selection
# if st.session_state.get('switch_button', False):
#     st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
#     manual_select = st.session_state['menu_option']
# else:
#     manual_select = None
    


    
    