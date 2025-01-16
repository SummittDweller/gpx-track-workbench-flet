# Create the StatusBox class

import streamlit as st

class StatusBox(object):
    
    # Constructor
    def __init__(self, box='status_box', initial_message="Undefined"):
        self.name = box
        self.text = initial_message
        with st.sidebar:
            self.container = st.empty( )        # create a Streamlit st.empty( ) container in the sidebar
            self.container.warning(self.text)        # write our text in the container as a warning

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
