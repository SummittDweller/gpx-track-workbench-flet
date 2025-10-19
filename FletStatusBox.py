# FletStatusBox Class
#---------------------------------------------------------------------------
# This class, used in a Flet app, can place a status container in 
# the app's sidebar interface.  
# 
# FletStatusBox.FletStatusBox(box_name) class constructor
# ----
# Creates a Text container in the sidebar. FletStatusBox attributes .name, 
# .text and .control are populated but the named box is not visible until 
# .update() or .display() is called.
# 
# update(msg, type='info')
# ----
# Use the 'update' method to change the Text content. The message can 
# be formatted as 'info' (the default), 'success', 'warning' or 'error' as desired.
#

import flet as ft
from loguru import logger

class FletStatusBox(object):
    
    # Constructor
    def __init__(self, box='status_box', heading='This is a StatusBox!', app_state=None):
        self.name = box
        self.mode = 'warning'
        self.heading = f"**{heading}**"
        self.text = f"Initialized"
        self.app_state = app_state
        
        # Create a Text control for status display
        self.control = ft.Text(
            value=f"{self.heading}\n{self.text}",
            color=ft.colors.AMBER_700,
            size=14,
            weight=ft.FontWeight.W_400
        )
        
        # Store in app state if provided
        if app_state:
            app_state[box] = self
            
        # If a logger is defined, repeat the warning there
        if app_state and app_state.get('logger'):
            app_state['logger'].warning(self.text)
    
    def update(self, text, mode='info'):
        """Update the status box with new text and styling"""
        self.text = text
        self.mode = mode
        
        # Set color based on mode
        color_map = {
            'info': ft.colors.BLUE_700,
            'success': ft.colors.GREEN_700,
            'warning': ft.colors.AMBER_700,
            'error': ft.colors.RED_700
        }
        
        self.control.value = f"{self.heading}\n{self.text}"
        self.control.color = color_map.get(mode, ft.colors.BLUE_700)
        
        # Update the control if it has a page reference
        if hasattr(self.control, 'page') and self.control.page:
            self.control.update()
            
        # Log the message if logger is available
        if self.app_state and self.app_state.get('logger'):
            getattr(self.app_state['logger'], mode, self.app_state['logger'].info)(self.text)
    
    def display(self):
        """Display the status box (compatibility with Streamlit version)"""
        # In Flet, the control is always "displayed" when added to a container
        pass