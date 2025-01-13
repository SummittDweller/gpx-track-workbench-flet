# sidebar.py

from functions import constants as c
from functions import utils as u
import os
import WorkingGPX as wgpx

# Common function abbreviations
# ------------------------------------------------------------------------
state = u.state


# sidebar(st)
#
# Display the left-hand sidebar for controls and return the path of 
# a selected working file.
# ------------------------------------------------------------------------
def sidebar(st):
    count = 0

    # File upload/selector
    uploaded = st.sidebar.file_uploader("Upload GPX files", key=f"uploader_{state('uploader_key')}", type=["gpx"], accept_multiple_files=True)

    if uploaded:
        state('logger').info(f"uploaded is TRUE")
        count = u.prep_uploaded(st, uploaded)
        st.session_state.count = count
        st.session_state.index = 1 
    else:
        state('logger').info(f"uploaded_files is FALSE") 

    state('logger').info(f"index is: {state('index')}") 

    # Display number of selected files
    # plural logic from https://stackoverflow.com/questions/21872366/plural-string-formatting
    if count:
        msg = f"You have {count} file{'s'[:count^1]} uploaded."  
        state('logger').info(msg)
        st.success(msg)  
        if st.button(f"Reset!", icon="💥", help=f"Double-click to clear your selected file list and return to selection of files."):
            clear_selection(st)
            count = 0
    else:
        st.warning(f"You have uploaded NO files!")

    st.divider( )

    # If count > 0 load ONE file followed by processing options...
    if count:
        uploaded_file = load_one_working_file(st)
        if uploaded_file:
            (df, gpx) = u.load_working_to_dataframe(st, uploaded_file)
        label = f"🚀 Choose what to do with the working GPX"    
        st.session_state.process = st.radio(label, ["Display", "Edit", "Add Speed Tags", "Reload"], index=None)
        st.divider( )
        

# clear_selection(st) - Callback for the "Reset!" button with 'st' passed
#
# Reset logic from https://discuss.streamlit.io/t/clear-the-file-uploader-after-using-the-file-data/66178/3
# -------------------------------------------------------------------------------
def clear_selection(st):
    st.session_state.gpx_list = None
    st.session_state.index = False
    st.session_state.count = 0
    st.session_state.preparred = False      # set this so the working copies can be rebuilt from our uploads
    st.session_state.uploader_key += 1    # increment file_uploader key to clear it
    state('logger').info('clear_selection called') 


# load_one_working_file(st) - Select one working file to be loaded for subsequent 
# processing and set the `working_path` session_state. 
# --------------------------------------------------------------------------------
def load_one_working_file(st):
    files = state('uploaded_list')
    
    if (files):
        label = f"🔄 Choose one GPX to load for processing"
        option = st.selectbox(label, files, index=None)         # wait for a selection and return it

        if option:
            i = files.index(option)
            working_path = state('working_list')[i]
            st.session_state.working_path = working_path    # This is CRITICAL! 

    return state('working_path')

