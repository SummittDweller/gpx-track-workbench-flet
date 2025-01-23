# editor.py
#

import constants as c
import functions as f
import streamlit as st
from loguru import logger
import WorkingGPX as WG
import StatusBox as SB
import inflect

def highlight_row(row):
    return ['background-color: yellow'] * len(row) if row.name == 1 else [''] * len(row)


# edit_df(st, workingGPX) - Edit the 'loaded' workingGPX dataframe of GPX data
# --------------------------------------------------------------------
def edit_df(st):
    loaded = f.state('loaded')
    if not loaded or len(loaded) < 1:
        st.error(f"GPX dataframe is NOT loaded!")
        return
    
    msg = f"EDIT called for '{loaded[0].title}' with WorkingGPX named '{loaded[0].fullname}'!"
    f.state('uploader_status').update(msg)

    msg = f"To remove track points select one or more rows on the left then use the trashcan icon to remove them."
    st.write(msg)

    # Fetch the loaded WorkingGPX dataframe and GPX 
    df = loaded[0].df
    gpx = loaded[0].gpx

    # (df, gpx) = f.load_working(st, loaded)
    # st.dataframe(df)

    # Display the associated dataframe w/ edit capability
    rows = int(df.size / 5)
    st.write(f"Loaded {rows} rows of data from '{loaded[0].fullname}'...")

    # Edit the dataframe
    placeholder = st.empty( )
    new_df = loaded[0].df

    # Invoke the data_editor
    with placeholder.form(key=f"editor_form", clear_on_submit=True):
        df_styled = df.style.apply(highlight_row, axis=1)
        # new_df = st.data_editor(df, num_rows='dynamic', key='editor')
        new_df = st.data_editor(df_styled, num_rows='dynamic', key='editor')
        submitted = st.form_submit_button("Save Changes")
    
    # Once the form is submitted clear the placeholder and update the WorkingGPX.df 
    # with the new dataframe.  Update the loaded session_state and replace the updated WorkingGPX
    # object into our session_state.GPXdict
    if submitted:
        placeholder.empty( )
        updated = loaded[0].update_from_df(new_df)
        st.session_state.loaded[0] = updated
        st.session_state.GPXdict.update(updated)



