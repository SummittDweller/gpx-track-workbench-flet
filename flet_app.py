# flet_app.py
# Main Flet application - equivalent to app.py but using Flet instead of Streamlit

import os
import time
import traceback as tb
import inflect

import flet as ft
from loguru import logger

import constants as c
import functions as f
import flet_uploader as fu
import flet_selector as fs
import WorkingGPX as WG
import FletStatusBox as FSB

# Import the original modules for processing (these should work with minor modifications)
import editor as e
import map as m
import speed as s
import post as p

class GPXTrackWorkbench:
    def __init__(self):
        self.app_state = {}
        self.page = None
        self.main_content = None
        self.sidebar = None
        self.uploader_ui = None
        self.selector_ui = None
        self.menu_rail = None
        
    def init_state(self):
        """Initialize all application state values"""
        if not self.app_state.get('logger'):
            logger.add("app.log", rotation="500 MB", level='TRACE')
            logger.info('This is GPX-Track-Workbench/flet_app.py!')
            self.app_state['logger'] = logger
            
        # Initialize state variables
        if not self.app_state.get('count'):
            self.app_state['count'] = 0
        if not self.app_state.get('loaded'):
            self.app_state['loaded'] = []
        if not self.app_state.get('GPXdict'):
            self.app_state['GPXdict'] = {}
        if not self.app_state.get('working_gpx'):
            self.app_state['working_gpx'] = None
        if not self.app_state.get('index'):
            self.app_state['index'] = False
        if not self.app_state.get('process'):
            self.app_state['process'] = None
        if not self.app_state.get('gpx_center'):
            self.app_state['gpx_center'] = c.MAP_CENTER
        if not self.app_state.get('posted_to_local'):
            self.app_state['posted_to_local'] = None
        if not self.app_state.get('my_path'):
            self.app_state['my_path'] = os.environ.get('HOME') + c.RAW_GPX_DIR
        if not self.app_state.get('mph_limit'):
            self.app_state['mph_limit'] = c.SPEED_THRESHOLD
        if not self.app_state.get('selected_menu'):
            self.app_state['selected_menu'] = 0

    def init_sidebar(self):
        """Initialize sidebar components"""
        # Create status boxes
        if not self.app_state.get('uploader_status'):
            FSB.FletStatusBox('uploader_status', 'Uploader Status:', self.app_state)
        if not self.app_state.get('selection_status'):
            FSB.FletStatusBox('selection_status', 'GPX Selection Status:', self.app_state)

    def on_reset_click(self, e):
        """Handle reset button click"""
        self.app_state.clear()
        self.init_state()
        self.init_sidebar()
        self.update_ui()

    def on_menu_select(self, e):
        """Handle menu selection"""
        self.app_state['selected_menu'] = e.control.selected_index
        self.update_main_content()

    def on_file_upload_complete(self):
        """Handle file upload completion"""
        self.update_ui()

    def on_selection_change(self, loaded_gpx):
        """Handle GPX selection change"""
        self.app_state['loaded'] = loaded_gpx
        self.update_main_content()

    def create_sidebar(self):
        """Create the sidebar with controls and status"""
        reset_button = ft.ElevatedButton(
            text="Reset!",
            icon=ft.icons.REFRESH,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_600,
            on_click=self.on_reset_click,
            width=200
        )

        debug_checkbox = ft.Checkbox(
            label="Debug: Print app state",
            value=False,
            on_change=self.on_debug_change
        )

        sidebar_content = ft.Column([
            reset_button,
            ft.Divider(),
            self.app_state.get('uploader_status', ft.Text("")).control,
            ft.Divider(),
            self.app_state.get('selection_status', ft.Text("")).control,
            ft.Divider(),
            debug_checkbox
        ], 
        spacing=10,
        scroll=ft.ScrollMode.AUTO
        )

        return ft.Container(
            content=sidebar_content,
            width=250,
            padding=20,
            bgcolor=ft.colors.GREY_100
        )

    def on_debug_change(self, e):
        """Handle debug checkbox change"""
        if e.control.value:
            print("=== App State ===")
            for key, value in self.app_state.items():
                if key != 'logger':  # Skip logger object
                    print(f"{key}: {value}")

    def create_menu_rail(self):
        """Create the navigation menu rail"""
        destinations = [
            ft.NavigationRailDestination(
                icon=ft.icons.HOME,
                selected_icon=ft.icons.HOME,
                label="Home"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.EDIT,
                selected_icon=ft.icons.EDIT,
                label="Edit"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.MAP,
                selected_icon=ft.icons.MAP,
                label="Map"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SPEED,
                selected_icon=ft.icons.SPEED,
                label="Speed"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CONTENT_CUT,
                selected_icon=ft.icons.CONTENT_CUT,
                label="Trim"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SEND,
                selected_icon=ft.icons.SEND,
                label="Post"
            )
        ]

        return ft.NavigationRail(
            selected_index=self.app_state.get('selected_menu', 0),
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            destinations=destinations,
            on_change=self.on_menu_select
        )

    def create_main_content(self):
        """Create the main content area"""
        selected_menu = self.app_state.get('selected_menu', 0)
        count = self.app_state.get('count', 0)

        # If no files uploaded, show uploader
        if count == 0:
            return ft.Container(
                content=fu.create_uploader_ui(self.app_state, self.on_file_upload_complete),
                padding=20
            )

        # Show selector if files are uploaded
        content_column = [
            fs.create_selector_ui(self.app_state, self.on_selection_change)
        ]

        # Add menu-specific content
        loaded = self.app_state.get('loaded', [])
        
        if selected_menu == 0:  # Home
            content_column.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("GPX Track Workbench", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Select GPX files and choose an action from the menu", size=16),
                        fs.get_selection_info_ui(self.app_state)
                    ]),
                    padding=20
                )
            )
        elif selected_menu == 1 and loaded:  # Edit
            content_column.append(self.create_edit_content())
        elif selected_menu == 2 and loaded:  # Map
            content_column.append(self.create_map_content())
        elif selected_menu == 3 and loaded:  # Speed
            content_column.append(self.create_speed_content())
        elif selected_menu == 4 and loaded:  # Trim
            content_column.append(self.create_trim_content())
        elif selected_menu == 5 and loaded:  # Post
            content_column.append(self.create_post_content())
        else:
            if not loaded:
                content_column.append(
                    ft.Container(
                        content=ft.Text(
                            "Please select at least one GPX file to proceed",
                            color=ft.colors.AMBER_700,
                            size=16
                        ),
                        padding=20
                    )
                )

        return ft.Column(content_column, scroll=ft.ScrollMode.AUTO)

    def create_edit_content(self):
        """Create edit functionality content"""
        loaded = self.app_state.get('loaded', [])
        if not loaded:
            return ft.Text("No GPX files selected")
        
        return ft.Container(
            content=ft.Column([
                ft.Text(f"Edit: {loaded[0].title}", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Edit functionality will be implemented here", size=14),
                ft.Text("(Original editor module would be adapted for Flet)", italic=True)
            ]),
            padding=20
        )

    def create_map_content(self):
        """Create map functionality content"""
        loaded = self.app_state.get('loaded', [])
        if not loaded:
            return ft.Text("No GPX files selected")
        
        return ft.Container(
            content=ft.Column([
                ft.Text(f"Map: {loaded[0].title}", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Map functionality will be implemented here", size=14),
                ft.Text("(Original map module would be adapted for Flet)", italic=True)
            ]),
            padding=20
        )

    def create_speed_content(self):
        """Create speed functionality content"""
        loaded = self.app_state.get('loaded', [])
        if not loaded:
            return ft.Text("No GPX files selected")
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Speed Analysis", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Speed functionality will be implemented here", size=14),
                ft.Text("(Original speed module would be adapted for Flet)", italic=True)
            ]),
            padding=20
        )

    def create_trim_content(self):
        """Create trim functionality content"""
        loaded = self.app_state.get('loaded', [])
        if not loaded:
            return ft.Text("No GPX files selected")
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Trim Speed", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Trim functionality will be implemented here", size=14),
                ft.Text("(Original trim module would be adapted for Flet)", italic=True)
            ]),
            padding=20
        )

    def create_post_content(self):
        """Create post functionality content"""
        loaded = self.app_state.get('loaded', [])
        if not loaded:
            return ft.Text("No GPX files selected")
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Post Tracks to Hikes", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Post functionality will be implemented here", size=14),
                ft.Text("(Original post module would be adapted for Flet)", italic=True)
            ]),
            padding=20
        )

    def update_ui(self):
        """Update the entire UI"""
        if self.page:
            self.page.controls.clear()
            
            # Recreate sidebar
            self.sidebar = self.create_sidebar()
            
            # Recreate menu rail
            self.menu_rail = self.create_menu_rail()
            
            # Recreate main content
            self.main_content = self.create_main_content()
            
            # Add to page
            main_row = ft.Row([
                self.sidebar,
                ft.VerticalDivider(width=1),
                self.menu_rail,
                ft.VerticalDivider(width=1),
                ft.Container(content=self.main_content, expand=True)
            ], expand=True)
            
            self.page.add(main_row)
            self.page.update()

    def update_main_content(self):
        """Update just the main content area"""
        if self.main_content and self.page:
            new_content = self.create_main_content()
            # Find the main content in the row and replace it
            main_row = self.page.controls[0]  # Should be the Row
            main_row.controls[-1] = ft.Container(content=new_content, expand=True)
            self.page.update()

def main(page: ft.Page):
    """Main Flet application entry point"""
    page.title = "GPX Track Workbench"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 800
    page.window_min_height = 600
    
    # Create app instance
    app = GPXTrackWorkbench()
    app.page = page
    
    # Initialize app
    app.init_state()
    app.init_sidebar()
    
    # Build initial UI
    app.update_ui()

if __name__ == "__main__":
    ft.app(target=main)