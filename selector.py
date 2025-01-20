# selector.py
#

import constants as c
import functions as f
import streamlit as st
from loguru import logger
import WorkingGPX as WG
import StatusBox as SB
import inflect

# check_loaded(st, limit=10) 
# Check if at least one WorkingGPX is 'loaded' for processing.  The number loaded 
# should not exceed 'limit'.
# --------------------------------------------------------------------------------
def check_loaded(st, limit=10):
    loaded = f.state('loaded')
    if not loaded or len(loaded) < 1:
        msg = f"You must load/select at least ONE WorkingGPX object for processing!"
        st.error(msg)
        return False
    if len(loaded) > limit:
        msg = f"You have loaded/selected more than the limit of {limit} WorkingGPX objects for processing.  Only the first, '{loaded[0].alias}', will be processed."
        st.warning(msg)
    if len(loaded) == 1:
        msg = f"GPX object '{loaded[0].alias}' is loaded as '{loaded[0].fullname}' for processing."
        st.info(msg)
        f.state('working_status').update(msg)
    else:
        msg = f"{len(loaded)} GPX objects are loaded for processing."
        st.info(msg)
        f.state('working_status').update(msg)
    return True


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
        loaded = gDict.list[option]
        st.session_state.loaded = loaded
        submitted = st.form_submit_button("Submit")
    
    # Once the form is submitted clear the placeholder
    if submitted:
        placeholder.empty( )

    return loaded


# Select and return a list of selected WorkingGPX objects from our GPXList
# ------------------------------------------------------------------------
def pick_some(st, max=10):
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

    # Open the WorkingGPX selector in an st.form( ) inside an st.empty( ) and clear once selected
    placeholder = st.empty( )

    # Invoke the dropdown selector
    with placeholder.form(key=f"selector_form", clear_on_submit=True):
        if max == 1:
            label = f"🔄 Choose ONE GPX to load for processing"
            option = st.selectbox(label, options, index=None)      # wait for a selection and return it
            selections[0] = option
        else: 
            label = f"🔄 Choose one or more GPX to load for processing"
            selections = st.multiselect(label, options)      # wait for a selection and return it
        selected = []
        for sel in selections:
            selected.append(gDict.list[sel])
        st.session_state.loaded = selected
        submitted = st.form_submit_button("Submit")
    
    # Once the form is submitted clear the placeholder
    if submitted:
        loaded = f.state('loaded')
        num = len(loaded)
        if num == 1:
            f.state('working_status').update(f"{loaded[0].alias} loaded as '{loaded[0].fullname}'")
        else:
            f.state('working_status').update(f"{num} GPX have been loaded")
        placeholder.empty( )

    # Fetch the current "loaded" list and return it
    loaded = f.state('loaded')
    return loaded
