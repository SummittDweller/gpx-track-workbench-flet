# uploader.py
#
# Frequently used functions
# ===============================================================================

import constants as c
import functions as f
# import map as m
# import speed as s

# import os 
# import shutil
import streamlit as st
from loguru import logger
from streamlit_option_menu import option_menu
# from st_click_detector import click_detector as did_click
import WorkingGPX as WG


# prep_uploaded(st, uploaded) - Prepare working copies of the uploaded list IF the 
# list has not yet been prepared 
# -----------------------------------------------------------------------------------
def prep_uploaded(st, uploaded):
    
    count = len(uploaded)
    # st.write(f"prep_uploaded:27 : <br/>{st.session_state}")
    
    # Check the session_state so the uploaded files NEVER replace the working copies!
    if f.state('prepared'):
        return count
        
    # Create an empty GPXList    
    gpxList = WG.GPXList( )
    st.session_state.gpx_list = gpxList
    # st.write(f"prep_uploaded:36 : <br/>{st.session_state}")
 
    with st.container( ):
        # Loop on the list of UploadedFile objects 
        for up in uploaded:
            # Create a single WorkingGPX object for each of the uploaded objects
            w = WG.WorkingGPX(up)
            msg = f"New WorkingGPX.status from {up.name} is: {w.status}"
            f.state('logger').info(msg)
            st.info(msg)

            # Add the new WorkingGPX object to our GPXList
            count = gpxList.append(w)
            st.session_state.count = count
            st.session_state.gpx_list = gpxList
            # st.session_state.uploaded_list.append(w.alias)

    if f.state('count'): 
        f.state('uploaded_status').success(f"You have successfully created **{f.state('count')}** WorkingGPX objects")

        # else:
        #     msg = f"Unable to load/parse GPX upload '{up.name}'.  It has been removed from the uploaded list."
        #     state('logger').warning(msg)
        #     st.warning(msg)
        #     uploaded.remove(up)
        #     count -= 1

    # print_state(st, 69)

    # Set the session_state so the uploaded files do not replace the working copies!
    st.session_state.prepared = True    

    return count


