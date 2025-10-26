# flet_selector.py
# Flet version of the selector functionality

import constants as c
# import functions as f  # COMMENTED OUT - functions.py removed
import flet as ft
from loguru import logger
import WorkingGPX as WG
import FletStatusBox as FSB
import inflect

def create_selector_ui(app_state, on_selection_change=None):
    """Create the GPX selector UI for Flet"""
    
    def on_checkbox_change(e):
        """Handle checkbox state changes"""
        update_loaded_gpx(app_state, checkbox_controls, on_selection_change)
    
    # Get available GPX files
    gpx_dict = app_state.get('GPXdict', {})
    if not gpx_dict:
        return ft.Container()
    
    # Create checkbox controls
    checkbox_controls = []
    for key, gpx_obj in gpx_dict.items():
        checkbox = ft.Checkbox(
            label=key,
            value=False,
            on_change=on_checkbox_change
        )
        checkbox_controls.append((checkbox, key, gpx_obj))
    
    # Store reference for later use
    app_state['_checkbox_controls'] = checkbox_controls
    
    # Create the selector UI
    selector_content = ft.Column([
        ft.Text(
            f"☑️ Choose one or more GPX (from {len(gpx_dict)} available) to load for processing",
            size=16,
            weight=ft.FontWeight.BOLD
        ),
        ft.Container(height=10),  # Spacer
        ft.Column([checkbox[0] for checkbox in checkbox_controls]),
        ft.Container(height=10),  # Spacer
        ft.ElevatedButton(
            text="Load Selected GPX",
            icon=ft.icons.CHECK_CIRCLE,
            on_click=lambda _: update_loaded_gpx(app_state, checkbox_controls, on_selection_change)
        )
    ])
    
    return ft.ExpansionTile(
        title=ft.Text("GPX Selector"),
        subtitle=ft.Text(f"{len(gpx_dict)} GPX files available"),
        leading=ft.Icon(ft.icons.LIST_ALT),
        controls=[
            ft.Container(
                content=selector_content,
                padding=20
            )
        ]
    )

def update_loaded_gpx(app_state, checkbox_controls, on_selection_change=None):
    """Update the loaded GPX list based on checkbox selections"""
    loaded = []
    
    for checkbox, key, gpx_obj in checkbox_controls:
        if checkbox.value:
            loaded.append(gpx_obj)
    
    app_state['loaded'] = loaded
    
    # Update status
    if loaded:
        num = len(loaded)
        if num == 1:
            msg = f"{loaded[0].alias} loaded with title '{loaded[0].title}'"
        else:
            msg = f"{num} GPX files have been loaded"
        
        if 'selection_status' in app_state:
            app_state['selection_status'].update(msg, 'success')
    else:
        if 'selection_status' in app_state:
            app_state['selection_status'].update("No GPX files selected", 'info')
    
    # Notify parent of selection change
    if on_selection_change:
        on_selection_change(loaded)

def check_loaded_flet(app_state, limit=20):
    """Check if at least one WorkingGPX is 'loaded' for processing (Flet version)"""
    loaded = app_state.get('loaded', [])
    
    if not loaded or len(loaded) < 1:
        return False, "Use the 'GPX Selector' to select at least ONE WorkingGPX object for processing!"
    
    if len(loaded) > limit:
        msg = f"You have selected {len(loaded)} WorkingGPX objects for processing but the limit is {limit}. Only the first, '{loaded[0].title}', will be processed."
        return True, msg
    
    if len(loaded) == 1:
        msg = f"GPX object '{loaded[0].title}' is loaded as '{loaded[0].fullname}' for processing."
    else:
        msg = f"{len(loaded)} GPX objects are loaded for processing."
    
    return True, msg

def get_selection_info_ui(app_state):
    """Create a UI component showing current selection info"""
    loaded = app_state.get('loaded', [])
    
    if not loaded:
        return ft.Text(
            "No GPX files selected",
            color=ft.colors.GREY_600,
            italic=True
        )
    
    if len(loaded) == 1:
        return ft.Text(
            f"Selected: {loaded[0].title}",
            color=ft.colors.GREEN_700,
            weight=ft.FontWeight.BOLD
        )
    
    return ft.Text(
        f"Selected: {len(loaded)} GPX files",
        color=ft.colors.GREEN_700,
        weight=ft.FontWeight.BOLD
    )