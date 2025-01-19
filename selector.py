# selector.py
#

import constants as c
import functions as f
import streamlit as st
from loguru import logger
import WorkingGPX as WG
import StatusBox as SB
import inflect

# Select and return ONE WorkingGPX object from our GPXList
# ------------------------------------------------------------------------
def pick_one(st):
    count = f.state('count')
    if not count: 
        st.session_state.loaded = None
        return None

    # IF there is ONLY one GPX available, set our session_state and return it ASAP!
    if count == 1:
        gDict = f.state('GPXdict')    # a GPXList object, a dict of WorkingGPX objects. keys are the .alias elements
        first_key = list(gDict.list.keys( ))[0]
        loaded = gDict.list[first_key]
        st.session_state.loaded = loaded
        return loaded

    # Fetch the current "loaded" object, if any
    loaded = f.state('loaded')

    # Build our options list... names of the uploaded GPX 
    options = []
    gDict = f.state('GPXdict')    # a GPXList object, a dict of WorkingGPX objects. keys are the .alias elements
    for key in gDict.list:
        options.append(key)

    label = f"🔄 Choose one GPX to load for processing"

    # Open the WorkingGPX selector in an st.form( ) inside an st.empty( ) and clear once selected
    placeholder = st.empty( )

    # Invoke the dropdown selector
    with placeholder.form(key=f"selector_form", clear_on_submit=True):
        option = st.selectbox(label, options, index=None)      # wait for a selection and return it
        if option:
            loaded = gDict.list[option]
            st.session_state.loaded = loaded
        submitted = st.form_submit_button("Submit")
    
    # Once the form is submitted clear the placeholder
    if submitted:
        placeholder.empty( )

    return loaded

