# editor.py
#

import constants as c
import functions as f
import streamlit as st
from loguru import logger
import WorkingGPX as WG
import StatusBox as SB
import inflect

# edit_df(st, workingGPX) - Edit the 'loaded' workingGPX dataframe of GPX data
# --------------------------------------------------------------------
def edit_df(st):
    loaded = f.state('loaded')
    if not loaded:
        st.error(f"GPX dataframe is NOT loaded!")
        return
    
    msg = f"EDIT called for '{loaded.alias}' with WorkingGPX named '{loaded.fullname}'!"
    f.state('uploader_status').update(msg)

    msg = f"To remove track points select one or more rows on the left then use the trashcan icon to remove them."
    st.write(msg)

    # Fetch the loaded WorkingGPX dataframe and GPX 
    df = loaded.df
    gpx = loaded.gpx

    # (df, gpx) = f.load_working(st, loaded)
    # st.dataframe(df)

    # Display the associated dataframe w/ edit capability
    rows = int(df.size / 5)
    st.write(f"Loaded {rows} rows of data from '{loaded.fullname}'...")

    # Edit the dataframe
    placeholder = st.empty( )
    new_df = loaded.df

    # Invoke file_uploader
    with placeholder.form(key=f"editor_form", clear_on_submit=True):
        new_df = st.data_editor(df, num_rows='dynamic', key='editor')
        submitted = st.form_submit_button("Save Changes")
    
    # Once the form is submitted clear the placeholder and update the WorkingGPX.df 
    # with the new dataframe.  Update the loaded session_state and replace the updated WorkingGPX
    # object into our session_state.gpx_list
    if submitted:
        placeholder.empty( )
        updated = loaded.update_from_df(new_df)
        st.session_state.loaded = updated
        st.session_state.gpx_list[loaded.alias] = updated

