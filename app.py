# GPX-Track-Workbenc/app.py

from functions import constants as c
from functions import utils as u
from functions import sidebar as s

import os 
import shutil
import streamlit as st
from loguru import logger
from st_click_detector import click_detector as did_click
import WorkingGPX as wgpx

# From https://github.com/JAlcocerT/Py_RouteTracker/blob/main/app.py
import folium
from streamlit_folium import st_folium
import gpxpy
import pandas as pd
from io import BytesIO

# Common function abbreviations
# -------------------------------------------------------------------------------
state = u.state

# MAIN ---------------------------------------------------------

if __name__ == '__main__':

    # Initialize the session_state
    if not state('logger'):
        logger.add("app.log", rotation="500 MB")
        logger.info('This is GPX-Track-Workbench/app.py!')
        st.session_state.logger = logger
    if not state('uploader_key'): 
        st.session_state.uploader_key = 0   # initialzie file_uploader key so it can be easily reset
    if not state('prepared'):
        st.session_state.prepared = False 
    if not state('working_path'):
        st.session_state.working_path = None   
    if not state('uploaded_list'):
        st.session_state.uploaded_list = []
    if not state('working_list'):
        st.session_state.working_list = []
    if not state('count'):                 
        st.session_state.count = 0    # track the number of working files
    if not state('index'):                 
        st.session_state.index = False    # index to the current working file
    if not state('process'):
        st.session_state.process = None

    if not state('gpx_center'):
        st.session_state.gpx_center = c.MAP_CENTER
    if not state('posted_to_local'):
        st.session_state.posted_to_local = None      # count of files posted to LOCAL hikes
    if not state('my_path'):                       
        st.session_state.my_path = c.RAW_GPX_DIR    # set appropriate starting directory
    if not state('mph_limit'):                 
        st.session_state.mph_limit = c.SPEED_THRESHOLD    # default walking speed threshold for trim

    # In the main window...
    # -------------------------------------------------------------------------------

    # Display the app header
    st.header(c.APP_TITLE, divider=True)

    # Add a sidebar for control. All data/display should take place in the main window.
    # -------------------------------------------------------------------------------

    # Display and process the left sidebar 
    with st.sidebar:
      s.sidebar(st)

    # No longer in the sidebar... take action
    process = state('process')

    if process == "Display":
        u.display_gpx(st)
    elif process == "Edit":
        u.edit_df(st)    
    elif process == "Add Speed Tags":
        u.add_speed_tags(st)    
    elif process == "Reload":
        u.add_speed_tags(st)    
    else:
        st.write("Nothing much going on here!")    

