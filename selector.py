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
        msg = f"Use the 'Select GPX' button in the sidebar to select at least ONE WorkingGPX object for processing!"
        st.error(msg)
        return False
    if len(loaded) > limit:
        msg = f"You have selected {len(loaded)} WorkingGPX objects for processing but the limit is {limit}.  Only the first, '{loaded[0].title}', will be processed."
        st.warning(msg)
    if len(loaded) == 1:
        msg = f"GPX object '{loaded[0].title}' is loaded as '{loaded[0].fullname}' for processing."
        st.info(msg)
        f.state('selection_status').update(msg)
    else:
        msg = f"{len(loaded)} GPX objects are loaded for processing."
        st.info(msg)
        f.state('selection_status').update(msg)
    return True


# # Select and return ONE WorkingGPX object from our GPXList
# # ------------------------------------------------------------------------
# def pick_one(st):
#     count = f.state('count')
#     if not count: 
#         st.session_state.loaded = None
#         return None

#     # IF there is ONLY one GPX available, set our session_state and return it ASAP!
#     if count == 1:
#         gDict = f.state('GPXdict')    # a GPXList object, a dict of WorkingGPX objects. keys are the .alias elements
#         first_key = list(gDict.list.keys( ))[0]
#         loaded = gDict.list[first_key]
#         st.session_state.loaded = loaded
#         return loaded

#     # Fetch the current "loaded" object, if any
#     loaded = f.state('loaded')

#     # Build our options list... names of the uploaded GPX 
#     options = []
#     gDict = f.state('GPXdict')    # a GPXList object, a dict of WorkingGPX objects. keys are the .alias elements
#     for key in gDict.list:
#         options.append(key)

#     label = f"🔄 Choose one GPX to load for processing"

#     # Open the WorkingGPX selector in an st.form( ) inside an st.empty( ) and clear once selected
#     placeholder = st.empty( )

#     # Invoke the dropdown selector
#     with placeholder.form(key=f"selector_form", clear_on_submit=True):
#         option = st.selectbox(label, options, index=None)      # wait for a selection and return it
#         loaded = gDict.list[option]
#         st.session_state.loaded = loaded
#         submitted = st.form_submit_button("Submit")
    
#     # Once the form is submitted clear the placeholder
#     if submitted:
#         placeholder.empty( )

#     return loaded


# Select and return a list of selected WorkingGPX objects from our GPXList
# ------------------------------------------------------------------------
def pick_some(st, limit=10):
    count = f.state('count')
    if not count: 
        st.session_state.loaded = []
        return None

    # Fetch the current "loaded" object, if any
    loaded = f.state('loaded')

    # Build our options list... names of the uploaded GPX 
    options = []
    gDict = f.state('GPXdict')    # a GPXList object, a dict of WorkingGPX objects. keys are the .title elements
    for key in gDict.list:
        title = gDict.list[key].title
        if key != title:
            st.error(f"Found errant GPXDict key '{key}' which does not match the object's title: '{title}'")
        options.append(key)

    # Open the WorkingGPX selector in an st.form( ) inside an st.expander( )
    label = f"☑️ Choose one or more GPX (from {count} available) to load for processing"
    placeholder = st.expander(label, expanded=False)

    # Invoke a CheckBoxArray to create st.session_state.loaded_X values where X is 0 through the number of options
    with placeholder.form(key=f"selector_form", clear_on_submit=True):
    # with st.form(key=f"selector_form", clear_on_submit=True):
        cb_array = CheckBoxArray("loaded", st, checkboxes=options, num_cols=1, max_select=limit)
        submitted = st.form_submit_button("Submit")

    # Once the form is submitted shrink the selector
    if submitted:
        st.session_state.loaded = []
        for i, opt in enumerate(options):
            key = f'loaded_{i}' 
            if f.state(key):
                st.session_state.loaded.append(gDict.list[opt])

    # Dump the session state if checkbox is checked.
    if f.state('dump_state'):
        st.write(st.session_state)

    loaded = f.state('loaded')
    if loaded:
        num = len(loaded)
        if num == 1:
            f.state('selection_status').update(f"{loaded[0].alias} loaded with title '{loaded[0].title}'")
        else:
            f.state('selection_status').update(f"{num} GPX have been loaded")
        # placeholder.empty( )

    # Fetch the current "loaded" list and return it
    loaded = f.state('loaded')
    return loaded


# from https://stackoverflow.com/questions/66718228/select-multiple-options-in-checkboxes-in-streamlit
class CheckBoxArray:
    def __init__(self, name: str, anchor, checkboxes: list[str], max_select: int, num_cols=1):
        self.name = name
        self.anchor = anchor
        # self.checkboxes = checkboxes
        # self.num_cols = num_cols
        cols = self.anchor.columns(num_cols)
        cb_values = [st.session_state.get(f"{self.name}_{i}", False) for i, _ in enumerate(checkboxes)]
        disable = sum(cb_values) == max_select
        for i, cb in enumerate(checkboxes):
            # cols[i % num_cols].checkbox(label=cb, disabled=(not cb_values[i] and disable), key=f"{self.name}_{i}")
            # self.cols[i % self.num_cols].checkbox(label=cb, value=cb_values[i], key=f"{self.name}_{i}")
            cols[i % num_cols].checkbox(label=cb, value=cb_values[i], disabled=disable, key=f"{self.name}_{i}")


    def reload(self, max_select=10):
        cb_values = [st.session_state.get(f"{self.name}_{i}", False) for i, _ in enumerate(self.checkboxes)]
        disable = sum(cb_values) == max_select
        for i, cb in enumerate(self.checkboxes):
            # cols[i % num_cols].checkbox(label=cb, disabled=(not cb_values[i] and disable), key=f"{self.name}_{i}")
            # self.cols[i % self.num_cols].checkbox(label=cb, value=cb_values[i], key=f"{self.name}_{i}")
            self.cols[i % self.num_cols].checkbox(label=cb, value=cb_values[i], disabled=disable, key=f"{self.name}_{i}")

