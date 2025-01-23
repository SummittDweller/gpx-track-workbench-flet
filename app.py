# GPX-Track-Workbench/app.py

# Key state( ) elements -----------------------------------------------
#
# uploader_status - A StatusBox object in the sidebar just below the menu
# selection_status - A StatusBox object in the sidebar below the uploader_status container
# count - Number of uploaded WorkingGPX objects to choose from
# GPXdict - dict( ) of count WorkingGPX objects with key=WorkingGPX.title
# loaded - dict( ) of selected/loaded WorkingGPX(s) for Edit, Map, Speed and Post actions

# Test the ability to change 'uploader_status' using the state variable.  It works!
#   f.state('uploader_status').update("This text uses the 'uploader_status' state( ) variable.")
# # Now, set the selection_status text using the stored uploader_status text as an error
#   f.state('selection_status').update(f.state('uploader_status').text, 'error')


import constants as c
import functions as f
import uploader as u
import selector as select
import editor as e
import map as m
import speed as s
import traceback as tb
import post as p

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
#                 f.state('selection_status').update(f"{loaded.name} loaded for {selection}")
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
    f.trace(1)
    if not f.state('count'):                 
        st.session_state.count = 0    # track the number of working files
    if not f.state('loaded'):                 
        st.session_state.loaded = []   # WorkingGPX object(s) loaded for processing
    if not f.state('GPXdict'):
        st.session_state.GPXdict = None   # session_state list of WorkingGPX objects in a GPXList object
    if not f.state('select_button'):
        st.session_state.select_button = None
    if not f.state('dump_state'):
        st.session_state.dump_state = None

    # Unused for now
    f.trace(1)
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

    with st.sidebar:
        # Present the Reset! button
        if st.button('Reset!', key='reset', icon='💣', help="Click here to restart from scratch!", use_container_width=True):
            for key in st.session_state.keys( ):
                del st.session_state[key]   # delete all session_state 
            st.rerun( )
        f.trace( )

        # UI containers
        f.trace(1)
        if not f.state('uploader_status'):
            SB.StatusBox('uploader_status', 'Uploader Status:')  # Call the class constructor 
        if not f.state('selection_status'):
            SB.StatusBox('selection_status', 'GPX Selection Status:')   # Call the class constructor 

        # Checkbox controls
        st.session_state.dump_state = st.checkbox(f"Debug: Print session_state")


# MAIN ---------------------------------------------------------

st.title("GPX Track Workbench")

# Initialize our state variables!  Make sure the logger is initialized!
init_state( )

# Initialize our sidebar state variables!
init_sidebar( )

# Display sidebar controls and status
f.state('uploader_status').display( )
f.state('selection_status').display( )

# If there are no WorkingGPX objects, upload some now!
if not f.state('count'):
    u.uploader( )

loaded = f.state('loaded')
if loaded:
    st.session_state.count = len(loaded)

# Show the GPX selector in the main area if we have uploaded some GPX
if st.session_state.count:
    st.session_state.loaded = select.pick_some(st)

    # Create our main menu container 
    if st.session_state.count:
        menu = st.container( )
        with menu:
            st.session_state.main_menu_selection = option_menu("Main Menu", [ '---', c.EDIT, c.MAP, c.SPEED, c.TRIM, c.POST], 
            icons=['', 'pencil', 'map', 'speedometer', 'scissors', 'signpost-split'], 
            menu_icon="", key='main_menu', default_index=0)  # , on_change=on_change  
            f.trace( )

            # Do some things in the main area
            selected = f.state('main_menu_selection')
            if selected:
                st.write(selected)
                f.trace( )

                # Fetch what's loaded... at least one GPX
                loaded = f.state('loaded')

                # Take action!  Replaces the on_change( ) function...
                match selected:

                    case '---':
                        st.write('Select an action from the Main Menu')
                        f.trace( )
        
                    case c.EDIT:
                        loaded = select.check_loaded(st, 1)
                        f.trace( )
                        loaded = f.state('loaded')
                        f.trace( )
                        if loaded:
                            e.edit_df(st)
                            f.trace( )
        
                    case c.MAP:
                        loaded = select.check_loaded(st, 1)
                        f.trace( )
                        loaded = f.state('loaded')
                        f.trace( )
                        if loaded:
                            m.map_gpx(st)
                            f.trace( )
        
                    case c.SPEED:
                        loaded = select.check_loaded(st)
                        f.trace( )
                        loaded = f.state('loaded')
                        f.trace( )
                        if loaded:
                            s.speed_gpx(st)
                            f.trace( )
        
                    case c.TRIM:
                        loaded = select.check_loaded(st)
                        f.trace( )
                        loaded = f.state('loaded')
                        f.trace( )
                        if loaded:
                            s.trim_gpx(st)
                            f.trace( )
                    
                    case c.POST:
                        loaded = select.check_loaded(st)
                        f.trace( )
                        loaded = f.state('loaded')
                        f.trace( )
                        if loaded:
                            p.post_gpx(st)
                            f.trace( )
                    
                    case c.RESET:
                        st.warning('Hold on to your butt!')
                        f.trace( )
                    
                    # If an exact match is not confirmed, this last case will be used if provided
                    case _:
                        st.error("Something's wrong in on_change( )")
                        f.trace( )

# # Print the GPXList dict of WG objects
# f.trace( )
# gpx_dict = f.state('GPXdict')
# if gpx_dict: 
#     gpx_dict.print_GPXdict(st)

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
