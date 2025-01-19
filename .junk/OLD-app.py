# GPX-Track-Workbenc/app.py

from . import constants as c
from . import functions as u
from functions import sidebar as s

import os 
import shutil
import streamlit as st
from loguru import logger
from st_click_detector import click_detector as did_click
import WorkingGPX as wgpx
import pprint
import time

# From https://github.com/JAlcocerT/Py_RouteTracker/blob/main/app.py
import folium
from streamlit_folium import st_folium
import gpxpy
import pandas as pd
from io import BytesIO

# Common function abbreviations
# -------------------------------------------------------------------------------
state = u.state

# init_state( )
# Initialize all of the st.session_state values
def init_state( ):
    if not state('logger'):
        logger.add("app.log", rotation="500 MB")
        logger.info('This is GPX-Track-Workbench/app.py!')
        st.session_state.logger = logger
    if not state('uploader_key'): 
        st.session_state.uploader_key = 0   # initialzie file_uploader key so it can be easily reset
    if not state('prepared'):
        st.session_state.prepared = False 
    if not state('working_gpx'):
        st.session_state.working_gpx = None   # our current WorkingGPX object
    if not state('GPXdict'):
        st.session_state.GPXdict = None   # session_state list of WorkingGPX objects in a GPXList object
    if not state('count'):                 
        st.session_state.count = 0    # track the number of working files
    if not state('index'):                 
        st.session_state.index = False    # index to the current working file
    if not state('process'):
        st.session_state.process = None
    if not state('print_state_checkbox'):
        st.session_state.print_state_checkbox = None 

    # UI containers
    if not state('controls'):
        st.session_state.controls = None 
    if not state('uploaded_status'):
        st.session_state.uploaded_status = None 
    if not state('working_status'):
        st.session_state.working_status = None 
    if not state('common'):
        st.session_state.common = None 

    # Unused for now
    if not state('gpx_center'):
        st.session_state.gpx_center = c.MAP_CENTER
    if not state('posted_to_local'):
        st.session_state.posted_to_local = None      # count of files posted to LOCAL hikes
    if not state('my_path'):                       
        st.session_state.my_path = c.RAW_GPX_DIR    # set appropriate starting directory
    if not state('mph_limit'):                 
        st.session_state.mph_limit = c.SPEED_THRESHOLD    # default walking speed threshold for trim


# Select an action for the working_gpx
# ------------------------------------------------------------------------
def select_action(st):
    label = f"🚀 Choose what to do with the working GPX"    
    st.session_state.process = st.sidebar.radio(label, ["Display", "Edit", "Add Speed Tags", "Reload"], index=None)
    st.divider( )


# Select and return ONE WorkingGPX object from our GPXList
# ------------------------------------------------------------------------
def pick_one(st):
    if not state('count'):
        return False
    
    # Build our options list... names of the uploaded GPX 
    options = []
    gList = state('GPXdict')    # a GPXList object, a dict of WorkingGPX objects. keys are the .alias elements
    for key in gList.list:
        options.append(key)

    label = f"🔄 Choose one GPX to load for processing"
    option = st.selectbox(label, options, index=None)      # wait for a selection and return it
    if option:
        working_gpx = gList.list[option]
        st.session_state.working_gpx = working_gpx
        return working_gpx

    return False


# uploader(st)
# In the sidebar display the UploadFile controls
# ------------------------------------------------------------------------
def uploader(st):
    if state('count') > 0:
        return state('count')
    
    count = 0

    # File upload/selector
    uploaded = st.sidebar.file_uploader("Upload GPX files", key=f"uploader_{state('uploader_key')}", type=["gpx"], accept_multiple_files=True)
    u.print_state(st, 33)

    if uploaded:
        state('logger').info(f"uploaded is TRUE")
        count = u.prep_uploaded(st, uploaded)
        st.session_state.count = count
        st.session_state.index = 1 
        u.print_state(st, 40)
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
    return count


# reset(st) - Callback for the "Reset!" button with 'st' passed
#
# Reset logic from https://discuss.streamlit.io/t/clear-the-file-uploader-after-using-the-file-data/66178/3
# -------------------------------------------------------------------------------
def reset(st):
    st.session_state.GPXdict = None
    st.session_state.index = False
    st.session_state.count = 0
    st.session_state.preparred = False      # set this so the working copies can be rebuilt from our uploads
    st.session_state.uploader_key += 1    # increment file_uploader key to clear it
    state('logger').info('reset( ) called') 



# MAIN ---------------------------------------------------------

# if __name__ == '__main__':

    # Initialize the session_state
    init_state( )

    # In the main window...
    # -------------------------------------------------------------------------------

    # Display the app title
    st.title(c.APP_TITLE)

    # Add a sidebar with 1 container for common controls and sone for uploaded tatus.
    # The single active control and data/display should take place in the main window.
    # -------------------------------------------------------------------------------
    
    st.session_state.common = st.sidebar.container( )
    with state('common'):
        st.session_state.print_state_checkbox = st.sidebar.checkbox("Print Session State?", value=False)
        if st.sidebar.button(f"Reset!", icon="💥", help=f"Double-click to clear all uploads and working GPX."):
            reset(st)

    # In the rest of the sidebar... create status "empty" containers 
    st.session_state.uploaded_status = st.sidebar.empty( )
    with state('uploaded_status'):
        if state('count'):
            st.success(f"You have successfully created **{state('count')}** WorkingGPX objects")
        else: 
            st.warning(f"You have **NO** WorkingGPX objects")

    st.session_state.working_status = st.sidebar.empty( )
    with state('working_status'):
        if state('working_gpx'):
            w = state('working_gpx')
            st.success(f"The selected WorkingGPX is: **'{w.alias}'**")
        else: 
            st.warning(f"You have selected **NO** WorkingGPX object")

    # Now controls should be an st.empty( ) in the main window since it can only have a single element
    st.session_state.controls = st.empty( )
    with state('controls'):

        # If we have no uploaded GPX...
        if not state('count'):
            # File upload/selector
            uploaded = st.file_uploader("Upload GPX files", key=f"uploader_{state('uploader_key')}", type=["gpx"], accept_multiple_files=True)
            u.print_state(st, 177)
            if uploaded is not None and len(uploaded) > 0:
                state('logger').info(f"uploaded is TRUE")
                count = u.prep_uploaded(st, uploaded)
                st.session_state.count = count
                u.print_state(st, 182)


        # If we don't have a working_gpx...
        if not state('working_gpx'):
            working_gpx = pick_one(st)
            st.session_state.working_gpx = working_gpx
            if state('working_gpx'):
                state('working_status').success(f"The selected WorkingPGX is: **'{working_gpx.alias}'**")

        # If we do have a working_gpx...
        if state('working_gpx'):
            w = state('working_gpx')
            # st.success(f"We have a working_gpx named {w.alias} in the FINAL section..." )
            label = f"🚀 Choose what to do with the selected WorkingGPX object"    
            st.session_state.process = st.radio(label, ["Display", "Edit", "Add Speed Tags", "Reload"], index=None)


    # # Do the Uploader...
    # if not state('count'):
    #     count = uploader(st)

    # # Report the uploader outcome
    # if count:
    #     report_uploader(st, bar)

    # # If we have one or more GPX uploaded...
    # if count:
    #     working_gpx = pick_one(st, count)
    #     st.session_state.working_gpx = working_gpx

    # # If we have a working_gpx, choose a process to take action
    # if state('working_gpx'):
    #     process = select_action(st)
    #     st.session_state.process = process
    
    # # Take action
    # process = state('process')

    # if process == "Display":
    #     u.display_gpx(st)
    # elif process == "Edit":
    #     u.edit_df(st)    
    # elif process == "Add Speed Tags":
    #     u.add_speed_tags(st)    
    # elif process == "Reload":
    #     u.add_speed_tags(st)    
    # else:
    #     st.write("Nothing much going on here!  Choose an action.")    

