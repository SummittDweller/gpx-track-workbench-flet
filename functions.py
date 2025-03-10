# utils.py
#
# Frequently used functions
# ===============================================================================

import streamlit as st
import constants as c
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
import traceback as tb


# trace(offset=0) 
# Simple function to print a short traceback message into our log, if it exists
# --------------------------------------------------------------------------------
def trace(offset=0):
    logger = state('logger')
    if logger: 
        # tb.print_stack( )
        msg0 = tb.format_stack()[8+offset].strip()  # print the caller info, not this function!
        msg = msg0.replace('File', 'trace:', 1).replace(', in <module>\n    f.trace( )', '')
        logger.trace(msg)


# print_state(st, line=False)
# Pretty print the session_state IF that option is on
# --------------------------------------------------------------------------------
def print_state(st, line=False):
    caller = inspect.stack()[1].function
    if state('print_state_checkbox'):
        header = f"{caller}:{line} → session_state"
        st.header(header, divider=True)
        st.write(st.session_state)


# state(key) - Return the value of st.session_state[key] or False
# If state is set and equal to "None", return False.
# -------------------------------------------------------------------------------
def state(key):
    try:
        if st.session_state[key]:
            if st.session_state[key] == "None":
                return False
            return st.session_state[key]
        else:
            return False
    except Exception as e:
        # st.exception(f"Exception: {e}")
        return False


# Actions -------------------------------------------------------------------------


# add_speed_tags(st)
# -----------------------------------------------------------------------
def add_speed_tags(st):
    wp = state('working_path')

    # This is a file operation, so no dataframe or GPX file handling needed here.
    if wp:
        msg = f"add_speed_tags(st, '{wp}') has been called!"
        st.write(msg)
        state('logger').info(msg)
        if gpsBabel_add_speed(st, wp):
            return  
            # edit_df(st)  # Load and edit the new working_path


# display_gpx(st)
# -----------------------------------------------------------------------
def display_gpx(st):
    msg = f"display_gpx( ) has been called!"
    st.write(msg)
    state('logger').info(msg)


# dataframe_to_gpx - Return a gpxpy GPX structure from a WorkingGPX dataframe
# ------------------------------------------------------------------------
def dataframe_to_gpx(df):
    # Convert DataFrame to GPX format
    gpx = gpxpy.gpx.GPX( )
    track = gpxpy.gpx.GPXTrack( )
    gpx.tracks.append(track)
    segment = gpxpy.gpx.GPXTrackSegment( )
    track.segments.append(segment)

    for index, row in df.iterrows( ):
        point = gpxpy.gpx.GPXTrackPoint(row['latitude'], row['longitude'], elevation=row['elevation'], speed=row['speed'], time=pd.to_datetime(row['time']))
        segment.points.append(point)

    return gpx


# save_working_copy(st, df) - Present a button below the dataframe 
#   that can be used to save the updated dataframe back to the working copy GPX file.
# --------------------------------------------------------------------
def save_working_copy(st, df):
    if st.button("Save the Working Copy of Changes Made", icon="💥", help=f"Click to save a working copy of your GPX changes"):
        gpx = dataframe_to_gpx(df)
        wp = state('working_path')    

        # Write the temporary GPX file
        with open(wp, 'w') as f:
            f.write(gpx.to_xml( ))

        # Report
        msg = f"Working copy file '{wp}' was replaced with our dataframe contents."  
        st.success(msg)
        state('logger').info(msg)

        # Put us back into datafream edit mode    
        edit_df(st)

        return


# reload(st) - Reload the dataframe from the working file
# --------------------------------------------------------------------
def reload(st):
    msg = f"reload( ) has been called!"
    # st.write(msg)
    state('logger').info(msg)

    if not state('df'):
        st.error(f"GPX dataframe is NOT loaded!")
        return False


# # load_working(st, working) - Load a selected WorkingGPX object to
# #   our dataframe and return the dataframe and gpxpy GPX object
# # ---------------------------------------------------------------------------------
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


# gpx_to_dataframe(st, gpx) - Load a GPX structure into a dataframe
#   and return the dataframe
# ---------------------------------------------------------------------------------
def gpx_to_dataframe(st, gpx):
    route_info = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.speed is None:
                    mph = None
                else:
                    mph = point.speed * 2.2321  # convert meter-per-second to mph

                route_info.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation if hasattr(point, 'elevation') else None,
                    'speed': mph,
                    'time': point.time if hasattr(point, 'time') else None
                })
                
    msg = f"route_info has been populated with {len(route_info)} points!"
    state('logger').info(msg)

    # Create a dataframe from the route_info
    df = pd.DataFrame(route_info)

    # Get track center lifted from https://www.google.com/search?client=firefox-b-1-d&q=python+gpx+track+center
    # st.session_state.center = get_track_center(gpx)

    return df


# uploaded_to_working(st, uploaded) - Create WorkingGPX dataframe and GPX elements 
#   from a GPX upload
# ---------------------------------------------------------------------------------
def uploaded_to_working(st, uploaded):
    gpx = False
    try:
        gpx_contents = uploaded.read( )
        gpx_file = BytesIO(gpx_contents)
        gpx = gpxpy.parse(gpx_file)
    except Exception as e:
        st.exception(f"Exception: {e}")
        return False
    df = gpx_to_dataframe(st, gpx)
    return (df, gpx)

    
# save_temp_gpx(st, gpx) - The load functions above returns a serailized dataframe object and GPX,
#   save a TEMP copy of the GPX.
# ------------------------------------------------------------------------------
def save_temp_gpx(st, gpx, name):
    new_path = os.path.join(os.environ.get('HOME') + c.TEMP_DIR, working_name(name))
    with open(new_path, 'w') as f:
        f.write(gpx.to_xml( ))
    msg = f"A working copy of '{name}' was saved in '{new_path}'."
    state('logger').info(msg)
    # st.write(msg)
    return new_path


# get_track_center - From a gpxpy "parsed" gpx file
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


# serialize_dataframe(st, dataframe, source) - Dataframes cannot be stored 
# in session_state, so we must 'serialize' them and store the temporary 
# source GPX filename in session_state
# ---------------------------------------------------------------------------
def serialize_dataframe(st, dataframe, source):
    dataframe.to_csv(os.environ.get('HOME') + c.DF_CSV, index=False)
    st.session_state.df = source
    return source


# deserialize_dataframe( ) - Dataframes cannot be stored in session_state, so we
#   must read our dataframe or 'deserialize' it
# ---------------------------------------------------------------------------
def deserialize_dataframe( ):
    df = pd.read_csv(os.environ.get('HOME') + c.DF_CSV)
    return df


# run_command(command) - Run a subprocess command
# ----------------------------------------------------------------------------
def run_command(command):
    """Runs a command in a subprocess and returns the output.  See https://www.google.com/search?client=firefox-b-1-d&q=streamlit+subprocess+run"""
    cmd = command[:command.index(' ')]
    with st.spinner(f"Running `{cmd}` command: '{command}'"):
        result = s.run(command, shell=True, stdout=s.PIPE, stderr=s.PIPE, text=True)

    if result.returncode == 0:
        st.success(f"`{cmd}` command executed successfully!")
        msg = f"Command: {command}\n" + result.stdout + '\n' +  f"GPSBabel successfully added speed tags and to file '{state('working_path')}'."
        st.text_area("Output:", msg, height=160)
    else:
        st.error(f"`{cmd}` command execution failed.")
        msg = f"Command: {command}\n\n" + result.stderr 
        st.text_area("Error:", msg, height=160)
        return False

    return True


# make_temp( ) - Return our TEMP_DIR/TEMP_FILE path
# ------------------------------------------------------------------------
def make_temp( ):
    # Make the c.TEMP_DIR directory if needed
    try:
        os.mkdir(os.environ.get('HOME') + c.TEMP_DIR)
    except FileExistsError:
        pass
    except Exception as e:
        st.exception(e)

    temp_path = os.path.join(os.environ.get('HOME') + c.TEMP_DIR, c.TEMP_FILE)
    st.session_state.temp_path = temp_path

    return temp_path


# gpsBabel_add_speed(st, working_path) - Run GPSBabel to add <speed> tags to the specified 
# working path and return success or NO if there are errors.
# --------------------------------------------------------------------------------------
def gpsBabel_add_speed(st, working_path):
    temp = make_temp( )
    parts = [ 'gpsbabel', '-t', '-i', 'gpx', '-f', working_path, '-x', 'track,speed', '-o', 'gpx,gpxver=1.0', '-F', temp ]
    command = ' '.join(parts)
    success = run_command(command)
    if success:
        state('logger').info(f"Copying file {temp} to '{working_path}'")
        try:
            shutil.copyfile(temp, working_path)
        except Exception as e:
            st.exception(e)
            return False

    return success 


# working_name(path) - Return a new working file name
# --------------------------------------------------------------------------------------
def working_name(path):
    dir = os.path.dirname(path)
    file = os.path.basename(path)
    new_name = os.path.join(os.environ.get('HOME') + c.TEMP_DIR, file.replace(' ','_').lower( ))
    return new_name


# rename_file_in_place(filepath) - Rename a file
# --------------------------------------------------------------------------------------
def rename_file_in_place(filepath):
    dir = os.path.dirname(filepath)
    file = os.path.basename(filepath)
    new_name = os.path.join(dir, file.replace(' ','_').lower( ))
    if new_name != filepath:
        os.rename(filepath, new_name)

    return new_name

