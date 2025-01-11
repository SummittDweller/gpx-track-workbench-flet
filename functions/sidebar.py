# sidebar.py

from functions import constants as c
from functions import utils as u
import os

# Common function abbreviations
# ------------------------------------------------------------------------
state = u.state

# sidebar(st)
#
# Display the left-hand sidebar for controls
# ------------------------------------------------------------------------
def sidebar(st):
    
    # File upload/selector
    uploaded_files = st.sidebar.file_uploader("Upload GPX files", key=f"uploader_{state('uploader_key')}", type=["gpx"], accept_multiple_files=True)
    
    if uploaded_files:
        state('logger').info(f"uploaded_files is TRUE") 
        st.session_state.file_list = uploaded_files
        count = len(uploaded_files)
        st.session_state.file_count = count
        st.session_state.file_index = 1 
    else:
        state('logger').info(f"uploaded_files is FALSE") 
        count = 0

    # Save each of the uploaded files to our working directory
    if count > 0:
        for uf in uploaded_files:
            gpx = u.load_file_to_dataframe(st, uf)
            new = u.save_temp_gpx(st, gpx)
            st.session_state.working_list.append(new)

    state('logger').info(f"file_index is: {state('file_index')}") 

    # Display number of selected files
    # plural logic from https://stackoverflow.com/questions/21872366/plural-string-formatting
    if count:
        msg = f"You have {count} file{'s'[:count^1]} selected."  
        state('logger').info(msg)
        st.success(msg)  
        if st.button(f"Reset!", icon="💥", help=f"Double-click to clear your selected file list and return to selection of files."):
            clear_selection(st)
            count = 0
    else:
        st.warning(f"You have selected NO files!")

    st.divider( )

    # If count > 0 load ONE file followed by processing options...
    if count:
        uploaded_file = load_one_file(st)
        if uploaded_file:
            u.load_file_to_dataframe(st, uploaded_file)
        label = f"🚀 Choose what to do with the loaded dataframe"    
        st.session_state.process = st.radio(label, ["Display", "Edit", "Add Speed Tags", "Reload"], index=None)
        st.divider( )
        

# clear_selection(st) - Callback for the "Reset!" button with 'st' passed
#
# Reset logic from https://discuss.streamlit.io/t/clear-the-file-uploader-after-using-the-file-data/66178/3
# -------------------------------------------------------------------------------
def clear_selection(st):
    st.session_state.file_list = []
    st.session_state.working_list = []
    st.session_state.file_index = False
    st.session_state.file_count = 0
    st.session_state.uploader_key += 1    # increment file_uploader key to clear it
    state('logger').info('clear_selection called') 


# load_one_file(st) - Select one file to be loaded for subsequent processing and return
# that UploadedFile object, not the filename!
# --------------------------------------------------------------------------------
def load_one_file(st):
    list = []
    files = state('file_list')
    
    if (files):
        for file in files:
            list.append(file.name)

        label = f"🔄 Choose one file to load for processing"
        option = st.selectbox(label, list)

        index = list.index(option)
        gpx = u.load_file_to_dataframe(st, files[index])

        # The load function above returns a gpx object, save a TEMP copy of the file from that gpx data.
        u.save_temp_gpx(st, gpx)

    return 

