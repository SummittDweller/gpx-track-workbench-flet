# uploader.py
#

import constants as c
import functions as f
import streamlit as st
from loguru import logger
import WorkingGPX as WG
import StatusBox as SB
import inflect
import time


def uploader( ):
    # If we already have GPX objects... do nothing here
    if f.state('count'):
        return

    # If we have no uploaded GPX... invoke file_uploader inside an st.form, inside an st.empty
    # See https://discuss.streamlit.io/t/delete-remove-from-app-screen-streamlit-form-st-form-after-feeling/25041/2
    placeholder = st.empty( )

    # Invoke file_uploader
    with placeholder.form(key=f"uploader_form", clear_on_submit=True):
        uploaded = st.file_uploader("Upload GPX Data", key=f"file_uploader", 
            type=["gpx"], accept_multiple_files=True, 
            help='Drag GPX files here and/or "Browse files" and select.  Click "Submit and Clear Uploader" when finished.')
        submitted = st.form_submit_button("Submit and Open the Selector")
    
    # Once the form is submitted clear the placeholder
    if submitted:
        placeholder.empty( )

    # When the uploader form is submitted...  create WorkingGPX objects from the uploads
    up_count = len(uploaded)
    if uploaded is not None and up_count > 0:
        p = inflect.engine( )
        msg = (f"{up_count} GPX {p.plural('has', up_count)} been uploaded!")
        f.state('uploader_status').update(msg, 'success')
        # Now prep the uploaded by creating a dict of WorkingGPX objects
        count = prep_uploaded(st, uploaded)
        st.session_state.count = count
        if count:
            msg = f"{up_count} uploaded GPX {p.plural('object', up_count)} created {count} WorkingGPX {p.plural('object', count)}"
            f.state('selection_status').update(msg)


# prep_uploaded(st, uploaded) - Prepare working copies (WorkingGPX) of the uploaded list
# -----------------------------------------------------------------------------------
def prep_uploaded(st, uploaded):
    p = inflect.engine( )
    count = len(uploaded)

    # Create an empty GPXList    
    GPXdict = WG.GPXList( )
    st.session_state.GPXdict = GPXdict

    # Run the prep in an st.container and clear it when done
    prep = st.empty( )

    with prep:

        progress_text = "Upload and WorkingGPX creation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
 
        # Loop on the list of UploadedFile objects 
        for up in uploaded:

            # Create a single WorkingGPX object for each of the uploaded objects
            w = WG.WorkingGPX(up)
            msg = f"New WorkingGPX.status from {up.name} is: {w.status}"
            f.state('logger').info(msg)
            st.info(msg)

            # Add the new WorkingGPX object to our GPXList
            st.session_state.count = GPXdict.append(w)
            st.session_state.GPXdict = GPXdict
            # st.session_state.uploaded_list.append(w.alias)

            count = f.state('count')
            if count:
                msg = f"Successfully created {count} WorkingGPX {p.plural('object', count)}"
                f.state('selection_status').update(msg, 'success')
                st.success(msg)

            percent_complete = count / len(uploaded)
            my_bar.progress(percent_complete, text=progress_text)

        my_bar.empty( )

    time.sleep(3)
    prep.empty( )

        # else:
        #     msg = f"Unable to load/parse GPX upload '{up.name}'.  It has been removed from the uploaded list."
        #     state('logger').warning(msg)
        #     st.warning(msg)
        #     uploaded.remove(up)
        #     count -= 1

    return count


