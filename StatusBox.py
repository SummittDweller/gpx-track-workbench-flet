# StatusBox Class
#---------------------------------------------------------------------------
# This class, used in a Streamlit app, can place an st.empty( ) container in 
# the app's sidebar interface.  
# 
# StatusBox.StatusBox(box_name) class constructor
# ----
# Creates an st.empty( ) container in the sidebar.  StatusBox attributes .name, 
# .text. and .container are popluated but the named box is not visible until 
# .update( ) is called.
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

class StatusBox(object):
    
    # Constructor
    def __init__(self, box='status_box'):
        self.name = box
        self.text = f"{box}: Initialized"
        with st.sidebar:
            self.container = st.empty( )   # create a Streamlit st.empty( ) container in the sidebar                
            self.container.warning(self.text)        # write our text in the container as a warning
        st.session_state[box] = self

    # update the container message
    def update(self, msg, type='info'):
        self.text = msg
        with self.container:
            match type:
                case 'info': st.info(msg)
                case 'success': st.success(msg)
                case 'warning': st.warning(msg)
                case 'error': st.error(msg)        
                case _: st.error(f'StatusBox update( ) called with an unknown type: {type}')
