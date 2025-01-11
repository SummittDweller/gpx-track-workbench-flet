# utils.py
#
# Frequently used functions
# ===============================================================================

import streamlit as st
from functions import constants as c
import os
import shutil
import subprocess as s

# From https://github.com/JAlcocerT/Py_RouteTracker/blob/main/app.py
import folium
from streamlit_folium import st_folium
import gpxpy
import pandas as pd
from io import BytesIO


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


# add_speed_tags(st)
# -----------------------------------------------------------------------
def add_speed_tags(st):
    msg = f"add_speed_tags( ) has been called!"
    st.write(msg)
    state('logger').info(msg)
    gpsBabel_add_speed( )


# display_gpx(st)
# -----------------------------------------------------------------------
def display_gpx(st):
    msg = f"display_gpx( ) has been called!"
    st.write(msg)
    state('logger').info(msg)


# make_gpx_from_dataframe(df) - Return a gpxpy GPX structure from a dataframe
# ------------------------------------------------------------------------
def make_gpx_from_dataframe(df):
  
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


# save_working_copy(st, dataframe) - Present a button below the dataframe 
#   that can be used to save the updated dataframe back to the working copy GPX file.
# --------------------------------------------------------------------
def save_working_copy(st, df):
    if st.button("Save the Working Copy of Changes Made", icon="💥", help=f"Click to save a working copy of your GPX changes"):
        gpx = make_gpx_from_dataframe(df)

        # Replace our working GPX file with this new GPX
        working = os.path.join(c.TEMP_DIR, state('df'))

        # Write the temporary GPX file
        with open(working, 'w') as f:
            f.write(gpx.to_xml( ))

        # Report
        msg = f"Working copy file '{working}' was replaced with our dataframe contents"
        st.success(msg)
        state('logger').info(msg)

        return True


# edit_gpx(st) - Edit the loaded dataframe of GPX data
# --------------------------------------------------------------------
def edit_gpx(st):
    msg = f"edit_gpx( ) has been called!"
    # st.write(msg)
    state('logger').info(msg)

    msg = f"To remove track points select one or more rows on the left then use the trashcan icon to remove them."
    st.write(msg)

    if not state('df'):
        st.error(f"GPX dataframe is NOT loaded!")
        return False

    # Deserialzie the session_state dataframe!
    df = deserialize_dataframe( )
    # st.dataframe(df)

    # Display the associated dataframe w/ edit capability
    rows = int(df.size / 5)
    st.write(f"Loaded {rows} rows of data from '{state('df')}'...")

    # Edit the dataframe and serialize it for session_state
    df = st.data_editor(df, num_rows='dynamic', key='editor')
    st.session_state.df = serialize_dataframe(st, df, state('df'))

    # Present a button below the dataframe that can be used to save the updated 
    # dataframe back to the original GPX file.
    result = save_working_copy(st, df)

    # rows2 = int(state('df').size / 5)
    # st.write(f"Edited GPX dataframe has {rows2} of data...")

    # # If edited, write the dataframe to our TEMP_FILE and replace our current_file with the TEMP_FILE
    # if rows2 < rows:
    #     write_dataframe_to_gpx(state('df'))
    #     temp = os.path.join(c.TEMP_DIR, c.TEMP_FILE)
    #     current = state('current_file')
    #     shutil.copy(temp, current)
    #     st.success(f"GPX file '{current}' replaced with {rows2} rows of edited data.")
    # else:
    #     st.status(f"No GPX changes made.")


# reload(st) - Reload the dataframe from the working file
# --------------------------------------------------------------------
def reload(st):
    msg = f"reload( ) has been called!"
    # st.write(msg)
    state('logger').info(msg)

    if not state('df'):
        st.error(f"GPX dataframe is NOT loaded!")
        return False


# load_file_to_dataframe(st, uploaded_file) - Load the selected GPX file to our dataframe
#   and return the gpxpy GPX object
# ---------------------------------------------------------------------------------
def load_file_to_dataframe(st, uploaded_file):
    gpx_contents = uploaded_file.read( )
    gpx_file = BytesIO(gpx_contents)
    gpx = gpxpy.parse(gpx_file)

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
    dataframe = pd.DataFrame(route_info)
    df = serialize_dataframe(st, dataframe, uploaded_file.name)
    msg = f"Route info from {df} is serialized in {c.DF_CSV}!"
    state('logger').info(msg)
    # st.write(msg)

    # Get track center lifted from https://www.google.com/search?client=firefox-b-1-d&q=python+gpx+track+center
    # st.session_state.center = get_track_center(gpx)

    return gpx


# save_temp_gpx(st, gpx) - The load function above returns a gpx object, 
#   save a TEMP copy of the file from that gpx data.
# ------------------------------------------------------------------------------
def save_temp_gpx(st, gpx):
    new_path = os.path.join(c.TEMP_DIR, state('df'))
    with open(new_path, 'w') as f:
        f.write(gpx.to_xml( ))
    new_pathname = rename_file_in_place(new_path)
    msg = f"A working copy of this GPX file has been saved in '{new_pathname}'."
    state('logger').info(msg)
    # st.write(msg)
    st.session_state.df = new_pathname
    return new_pathname


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
    dataframe.to_csv(c.DF_CSV, index=False)
    st.session_state.df = source
    return source


# deserialize_dataframe( ) - Dataframes cannot be stored in session_state, so we
#   must read our dataframe or 'deserialize' it
# ---------------------------------------------------------------------------
def deserialize_dataframe( ):
    df = pd.read_csv(c.DF_CSV)
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
        msg = f"Command: {command}\n" + result.stdout + '\n' +  f"GPSBabel successfully added speed tags and to file '{state('current_file')}'."
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
        os.mkdir(c.TEMP_DIR)
    except FileExistsError:
        pass
    except Exception as e:
        st.exception(e)

    temp_path = os.path.join(c.TEMP_DIR, c.TEMP_FILE)
    st.session_state.temp_path = temp_path

    return temp_path


# gpsBabel_add_speed( ) - Run GPSBabel to add <speed> tags to the loaded working file.
# --------------------------------------------------------------------------------------
def gpsBabel_add_speed( ):
    temp = make_temp( )
    parts = [ 'gpsbabel', '-t', '-i', 'gpx', '-f', state('df'), '-x', 'track,speed', '-o', 'gpx,gpxver=1.0', '-F', temp ]
    command = ' '.join(parts)
    success = run_command(command)
    if success:
        state('logger').info(f"Copying file {temp} to {state('df')}")
        try:
            shutil.copyfile(temp, state('df'))
        except Exception as e:
            st.exception(e)
            return False

    return success


# rename_file_in_place(filepath) - Rename a file
# --------------------------------------------------------------------------------------
def rename_file_in_place(filepath):
    st.session_state.current_file = filepath
    dir = os.path.dirname(filepath)
    file = os.path.basename(filepath)
    new_name = os.path.join(dir, file.replace(' ','_').lower( ))
    if new_name != filepath:
        os.rename(filepath, new_name)
        st.session_state.current_file = new_name

    return new_name

