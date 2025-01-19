# GPX-Track-Workbench/app.py

# Key state( ) elements -----------------------------------------------
#
# uploader_status - A StatusBox object in the sidebar just below the menu
# working_status - A StatusBox object in the sidebar below the uploader_status container
# count - Number of loaded WorkingGPX objects to choose from
# GPXdict - dict( ) of count WorkingGPX objects with key=WorkingGPX.alias, the name of the uploaded object it was created from
# loaded - The selected/loaded WorkingGPX(s) for Edit, Map, Speed and Post actions

# Test the ability to change 'uploader_status' using the state variable.  It works!
#   f.state('uploader_status').update("This text uses the 'uploader_status' state( ) variable.")
# # Now, set the working_status text using the stored uploader_status text as an error
#   f.state('working_status').update(f.state('uploader_status').text, 'error')


import constants as c
import functions as f
import uploader as u
import selector as select
import editor as e
import map as m
import speed as s
import traceback as tb

# import map as m
# import speed as s

# import os 
# import shutil
import streamlit as st
from loguru import logger
from streamlit_option_menu import option_menu
# from st_click_detector import click_detector as did_click
import WorkingGPX as WG
import StatusBox as SB
# import pprint
import time
import inflect

# From https://github.com/JAlcocerT/Py_RouteTracker/blob/main/app.py
# import folium
# from streamlit_folium import st_folium
# import gpxpy
# import pandas as pd
# from io import BytesIO




# # on_change(key) - Define the menu's on_change callback
# # ------------------------------------------------------------------------------------------
# def on_change(key):
#     selection = st.session_state[key]
#     # st.success(f"Selection changed to: {selection}")
#     # st.session_state

#     # Act on the selected key
#     match selection:
#         case c.EDIT:
#             if not f.state('loaded'):
#                 st.session_state.loaded = select.pick_one(st)
            
#             loaded = f.state('loaded')
#             if loaded:
#                 f.state('working_status').update(f"{loaded.name} loaded for {selection}")
#                 f.edit_df(st)

#         case c.MAP:
#             st.warning("MAP not available")
#         case c.SPEED:
#             st.warning("SPEED not available")
#         case c.POST:
#             st.warning("POST not available")
#         case c.RESET:
#             st.warning('Hold on to your butt!')
#         # If an exact match is not confirmed, this last case will be used if provided
#         case _:
#             st.error("Something's wrong in on_change( )")
    
#     return


# init_state( )
# Initialize all of the st.session_state values
def init_state( ):
    if not f.state('logger'):
        logger.add("app.log", rotation="500 MB", level='TRACE')    # Change this to DEBUG to turn off TRACE
        logger.info('This is GPX-Track-Workbench/app.py!')
        st.session_state.logger = logger
    f.trace( )
    if not f.state('count'):                 
        st.session_state.count = 0    # track the number of working files
    if not f.state('loaded'):                 
        st.session_state.loaded = None    # WorkingGPX object(s) loaded for processing
    if not f.state('GPXdict'):
        st.session_state.GPXdict = None   # session_state list of WorkingGPX objects in a GPXList object

    # Unused for now
    f.trace( )
    if not f.state('working_gpx'):
        st.session_state.working_gpx = None   # our current WorkingGPX object
    if not f.state('index'):                 
        st.session_state.index = False    # index to the current working file
    if not f.state('process'):
        st.session_state.process = None
    if not f.state('print_state_checkbox'):
        st.session_state.print_state_checkbox = None 
    if not f.state('gpx_center'):
        st.session_state.gpx_center = c.MAP_CENTER
    if not f.state('posted_to_local'):
        st.session_state.posted_to_local = None      # count of files posted to LOCAL hikes
    if not f.state('my_path'):                       
        st.session_state.my_path = c.RAW_GPX_DIR    # set appropriate starting directory
    if not f.state('mph_limit'):                 
        st.session_state.mph_limit = c.SPEED_THRESHOLD    # default walking speed threshold for trim


def init_sidebar( ):
    # UI containers
    f.trace( )
    if not f.state('uploader_status'):
        SB.StatusBox('uploader_status')  # Call the class constructor 
    if not f.state('working_status'):
        SB.StatusBox('working_status')  # Call the class constructor 


# MAIN ---------------------------------------------------------

# Initialize our state variables!  Make sure the logger is initialized!
init_state( )

# Present the Reset! button
reset = st.empty( )
f.trace( )

if reset.button('Reset!', key='reset', icon='💣', help="Click here to restart from scratch!", use_container_width=True):
    for key in st.session_state.keys( ):
        del st.session_state[key]   # delete all session_state 
    st.rerun( )
    f.trace( )

# If there are no WorkingGPX objects, upload some now!
if not f.state('count'):
    f.trace( )
    u.uploader( )
    f.trace( )

# Create the sidebar menu
with st.sidebar:
    selected = option_menu("GPX Track Workbench", [ '---', c.EDIT, c.MAP, c.SPEED, c.POST], 
    icons=['', 'pencil', 'map', 'speedometer', 'signpost-split'], 
    menu_icon="cast", key='main_menu', default_index=0)  # , on_change=on_change  
    f.trace( )

    # Initialize our state variables!
    init_sidebar( )
    f.trace( )

# Do some things in the main area
selected = f.state('main_menu')
if selected:
    st.write(selected)
    f.trace( )

    # Take action!  Replaces the on_change( ) function...
    match selected:
        case '---':
            f.trace( )
            st.write('Select an action from the Main Menu')
        case c.EDIT:
            f.trace( )
            if not f.state('loaded'):
                st.session_state.loaded = select.pick_one(st)
                loaded = f.state('loaded')
                if loaded:
                    f.state('working_status').update(f"{loaded.alias} loaded to '{selected}'")
                    e.edit_df(st)
        case c.MAP:
            f.trace( )
            if not f.state('loaded'):
                st.session_state.loaded = select.pick_one(st)
                loaded = f.state('loaded')
                if loaded:
                    f.state('working_status').update(f"{loaded.alias} loaded to '{selected}'")
                    m.map_gpx(st)
        case c.SPEED:
            f.trace( )
            if not f.state('loaded'):
                st.session_state.loaded = select.pick_one(st)
                loaded = f.state('loaded')
                if loaded:
                    f.state('working_status').update(f"{loaded.alias} loaded to '{selected}'")
                    s.speed_gpx(st)
        case c.POST:
            f.trace( )
            st.warning("POST not available")
        case c.RESET:
            f.trace( )
            st.warning('Hold on to your butt!')
        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            f.trace( )
            st.error("Something's wrong in on_change( )")

# Print the GPXList dict of WG objects
f.trace( )
gpx_dict = f.state('GPXdict')
if gpx_dict: 
    gpx_dict.print_GPXdict(st)

f.trace( )

# Menu options and examples
#
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
#
# # 4. Manual item selection
# if st.session_state.get('switch_button', False):
#     st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
#     manual_select = st.session_state['menu_option']
# else:
#     manual_select = None
