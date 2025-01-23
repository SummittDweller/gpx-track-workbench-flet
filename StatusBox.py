# StatusBox Class
#---------------------------------------------------------------------------
# This class, used in a Streamlit app, can place an st.empty( ) container in 
# the app's sidebar interface.  
# 
# StatusBox.StatusBox(box_name) class constructor
# ----
# Creates an st.empty( ) container in the sidebar.  StatusBox attributes .name, 
# .text. and .container are popluated but the named box is not visible until 
# .update( ) or .display( ) is called.
# 
# update(msg, type='info')
# ----
# Use the 'update' method to change the st.empty( ) content.  The message can 
# be formatted as 'info' (the default), 'success', 'warning' or 'error' as desired.
#
# Example use: 
#
# with st.sidebar:
#     selected = option_menu("GPX Track Workbench", [ c.HOME, c.UPLOAD, c.EDIT, c.MAP, c.SPEED, c.POST ], 
#     icons=['house-fill', 'cloud-upload-fill', 'pencil', 'map', 'speedometer', 'signpost-split'], 
#     menu_icon="cast", default_index=0, on_change=on_change, key='main_menu')  
#
#     # Add uploader status text below the menu
#     us = SB.StatusBox('uploader_status')
#     us.update('Is this working?')
#     time.sleep(5)
#     f.state('uploader_status').update('Yes it is!')
#

import streamlit as st
from loguru import logger

class StatusBox(object):
    
    # Constructor
    def __init__(self, box='status_box', heading='This is a StatusBox!'):
        self.name = box
        self.mode = 'warning'
        self.heading = f"**{heading}** \n"
        self.text = f"Initialized"
        with st.sidebar:
            self.container = st.empty( )   # create a Streamlit st.empty( ) container in the sidebar                
            with self.container:
                msg = f"{self.heading}{self.text}"
                st.warning(msg)        # write our text in the container as a warning
        st.session_state[box] = self
        # If a logger is defined, repeat the warning there
        if st.session_state.logger:
            st.session_state.logger.warning(self.text)


    # update the container message and type/mode
    def update(self, msg, type='info'):
        self.text = msg
        self.mode = type
        with self.container:
            msg = f"{self.heading}{self.text}"
            match type:
                case 'info': st.info(msg)
                case 'success': st.success(msg)
                case 'warning': st.warning(msg)
                case 'error': st.error(msg)        
                case _: st.error(f'StatusBox update( ) called with an unknown type: {type}')
        # If a logger is defined, repeat the message there
        if st.session_state.logger:
            log = st.session_state.logger
            match type:
                case 'info': log.info(msg)
                case 'success': log.success(msg)
                case 'warning': log.warning(msg)
                case 'error': log.error(msg)        
                case _: log.error(f'StatusBox update( ) called with an unknown type: {type}')


    # display the container as it was before
    def display(self):
        msg = self.text
        type = self.mode
        with self.container:
            msg = f"{self.heading}{self.text}"
            match type:
                case 'info': st.info(msg)
                case 'success': st.success(msg)
                case 'warning': st.warning(msg)
                case 'error': st.error(msg)        
                case _: st.error(f'StatusBox display( ) called with an unknown mode: {type}')
