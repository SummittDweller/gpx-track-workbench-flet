# speed.py
#

import streamlit as st
import constants as c
import functions as f
import os
import shutil
import subprocess as sub
import WorkingGPX as WG


# run_command(command) - Run a subprocess command
# ----------------------------------------------------------------------------
def run_command(command):
    """Runs a command in a subprocess and returns the output.  See https://www.google.com/search?client=firefox-b-1-d&q=streamlit+subprocess+run"""
    cmd = command[:command.index(' ')]
    with st.spinner(f"Running `{cmd}` command: '{command}'"):
        result = sub.run(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE, text=True)
    if result.returncode == 0:
        st.success(f"`{cmd}` command executed successfully!")
        msg = f"Command: {command}\n" + result.stdout
        st.text_area("Output:", msg, height=160)
    else:
        st.error(f"`{cmd}` command execution failed.")
        msg = f"Command: {command}\n\n" + result.stderr 
        st.text_area("Error:", msg, height=160)
        return False
    return True


# gpsBabel_add_speed(st, working_path) - Run GPSBabel to add <speed> tags to the specified 
# working path and return success or NO if there are errors.
# --------------------------------------------------------------------------------------
def gpsBabel_add_speed(st, working_path):
    temp = f.make_temp( )
    parts = [ 'gpsbabel', '-t', '-i', 'gpx', '-f', working_path, '-x', 'track,speed', '-o', 'gpx,gpxver=1.0', '-F', temp ]
    command = ' '.join(parts)
    success = run_command(command)
    if success:
        f.state('logger').info(f"Copying file {temp} to '{working_path}'")
        try:
            shutil.copyfile(temp, working_path)
        except Exception as e:
            st.exception(e)
            return False
    msg = f"GPSBabel successfully added speed tags to file '{working_path}'."
    st.success(msg)
    return success 


# speed_gpx(st)
# -----------------------------------------------------------------------
def speed_gpx(st):
    loaded = f.state('loaded')
    if not loaded:
        return
    
    # This is a file operation, so no dataframe or GPX file handling needed here.
    num = len(loaded)
    if num == 1:
        msg = f"speed_gpx(st) called with '{loaded[0].title}' as '{loaded[0].fullname}'"
    else:
        msg = f"speed_gpx(st) called with {num} loaded GPX"
    st.write(msg)
    f.state('logger').info(msg)

    for index, g in enumerate(loaded):
        if gpsBabel_add_speed(st, g.fullname):
            g = g.update_from_file(g.fullname)

    return


# trim_gpx(st)
# -----------------------------------------------------------------------
def trim_gpx(st):
    loaded = f.state('loaded')
    if not loaded:
        return
    
    # This is a dataframe operation, load them one at a time
    num = len(loaded)
    if num == 1:
        msg = f"trim_gpx(st) called with '{loaded[0].title}' as '{loaded[0].fullname}'"
    else:
        msg = f"trim_gpx(st) called with {num} loaded GPX"
    st.write(msg)
    f.state('logger').info(msg)

    # Loop on the loaded GPX objects
    for index, g in enumerate(loaded):
        df = g.df
        # Find the index of the first speed greater than 10
        index = df['speed'].gt(10).idxmax()

        # Drop rows where 'speed' is None, then zero, then greater than 5
        # df.drop(df[df['speed'] == None].index, inplace=True)        
        # df.drop(df[df['speed'] == 0].index, inplace=True)        
        # df.drop(df[df['speed'] > 5].index, inplace=True)        

        df = df.truncate(after=index)
        g = g.update_from_df(df)

    return
