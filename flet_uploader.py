# flet_uploader.py
# Flet version of the uploader functionality

import constants as c
import functions as f
import flet as ft
from loguru import logger
import WorkingGPX as WG
import FletStatusBox as FSB
import inflect
import time
import os

def create_uploader_ui(app_state, update_callback=None):
    """Create the file uploader UI for Flet"""
    
    def on_files_selected(e):
        """Handle file selection"""
        if e.files:
            uploaded_files = []
            for file in e.files:
                # In Flet, we need to handle file reading differently
                uploaded_files.append(file)
            
            if uploaded_files:
                process_uploaded_files(app_state, uploaded_files, update_callback)
    
    # Create file picker
    file_picker = ft.FilePicker(
        on_result=on_files_selected
    )
    
    # Create upload button
    upload_button = ft.ElevatedButton(
        text="Upload GPX Data",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            dialog_title="Select GPX files",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["gpx"],
            allow_multiple=True
        ),
        width=300
    )
    
    return ft.Column([
        file_picker,
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "Upload GPX Data",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Select GPX files to upload and process",
                    size=14,
                    color=ft.colors.GREY_700
                ),
                upload_button
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
            ),
            padding=20,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            margin=20
        )
    ])

def process_uploaded_files(app_state, uploaded_files, update_callback=None):
    """Process the uploaded GPX files"""
    up_count = len(uploaded_files)
    if up_count > 0:
        p = inflect.engine()
        msg = f"{up_count} GPX {p.plural('file', up_count)} {p.plural('has', up_count)} been selected!"
        
        # Update status
        if 'uploader_status' in app_state:
            app_state['uploader_status'].update(msg, 'success')
        
        # Create WorkingGPX objects
        count = prep_uploaded_flet(app_state, uploaded_files)
        app_state['count'] = count
        
        if count:
            msg = f"{up_count} uploaded GPX {p.plural('file', up_count)} created {count} WorkingGPX {p.plural('object', count)}"
            if 'selection_status' in app_state:
                app_state['selection_status'].update(msg)
        
        # Notify parent component to update
        if update_callback:
            update_callback()

def prep_uploaded_flet(app_state, uploaded_files):
    """Prepare working copies (WorkingGPX) of the uploaded files for Flet"""
    count = 0
    gpx_dict = {}
    
    try:
        for uploaded_file in uploaded_files:
            # Read file content
            file_path = uploaded_file.path
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create WorkingGPX object
                wg = WG.WorkingGPX(uploaded_file.name, content)
                if wg.is_valid:
                    gpx_dict[wg.title] = wg
                    count += 1
                    if app_state.get('logger'):
                        app_state['logger'].info(f"Created WorkingGPX object: {wg.title}")
                else:
                    if app_state.get('logger'):
                        app_state['logger'].warning(f"Invalid GPX file: {uploaded_file.name}")
        
        # Store the GPX dictionary
        app_state['GPXdict'] = gpx_dict
        
        if app_state.get('logger'):
            app_state['logger'].info(f"Successfully processed {count} GPX files")
            
    except Exception as e:
        if app_state.get('logger'):
            app_state['logger'].error(f"Error processing uploaded files: {str(e)}")
        count = 0
    
    return count