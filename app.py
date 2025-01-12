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
import pprint

# From https://github.com/JAlcocerT/Py_RouteTracker/blob/main/app.py
import folium
from streamlit_folium import st_folium
import gpxpy
import pandas as pd
from io import BytesIO

# Common function abbreviations
# -------------------------------------------------------------------------------
state = u.state

# In the sidebar display the UploadFile controls
# ------------------------------------------------------------------------
def uploader(st):
    count = 0

    # File upload/selector
    uploaded = st.sidebar.file_uploader("Upload GPX files", key=f"uploader_{state('uploader_key')}", type=["gpx"], accept_multiple_files=True)
    u.print_state(st)

    if uploaded:
        state('logger').info(f"uploaded is TRUE")
        count = u.prep_uploaded(st, uploaded)
        st.session_state.count = count
        st.session_state.index = 1 
        u.print_state( )
    else:
        state('logger').info(f"uploaded_files is FALSE") 

    state('logger').info(f"index is: {state('index')}") 

    # Display number of selected files
    # plural logic from https://stackoverflow.com/questions/21872366/plural-string-formatting
    if count:
        msg = f"You have {count} file{'s'[:count^1]} uploaded."  
        state('logger').info(msg)
        st.sidebar.success(msg)  
        if st.sidebar.button(f"Reset!", icon="💥", help=f"Double-click to clear your selected file list and return to selection of files."):
            u.clear_selection(st)
            count = 0
    else:
        st.sidebar.warning(f"You have uploaded NO files!")

    st.sidebar.divider( )


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

    # Display the app title
    st.title(c.APP_TITLE)

    # Add a sidebar for control. All data/display should take place in the main window.
    # -------------------------------------------------------------------------------

    # Do the Uploader...
    uploader(st)

    # Take action
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
        st.write("Nothing much going on here!  Choose an action.")    

