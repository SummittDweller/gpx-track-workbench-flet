# GPX Track Workbench - Flet Version

This is a Flet-based port of the original Streamlit GPX Track Workbench application. The Flet version provides the same core functionality but uses Flet's desktop/mobile app framework instead of Streamlit's web interface.

## Files Overview

### Main Application Files
- `flet_app.py` - Main Flet application (equivalent to `app.py`)
- `flet_requirements.txt` - Python dependencies for Flet version
- `FletStatusBox.py` - Flet version of StatusBox class
- `flet_uploader.py` - File upload functionality for Flet
- `flet_selector.py` - GPX file selection interface for Flet
- `flet_functions.py` - State management utilities for Flet

### Shared Components
The following files are shared between Streamlit and Flet versions:
- `constants.py` - Application constants
- `WorkingGPX.py` - GPX file processing class
- `functions.py` - Core utility functions (original Streamlit version)
- Core processing modules: `editor.py`, `map.py`, `speed.py`, `post.py`

## Key Differences from Streamlit Version

### UI Framework
- **Streamlit**: Web-based interface with automatic reactivity
- **Flet**: Desktop/mobile app with manual UI updates

### State Management
- **Streamlit**: Uses `st.session_state` for state persistence
- **Flet**: Uses custom app state dictionary with helper functions

### File Upload
- **Streamlit**: Built-in `st.file_uploader()` widget
- **Flet**: Uses `ft.FilePicker()` with file system access

### Layout
- **Streamlit**: Sidebar + main area with automatic responsive layout
- **Flet**: Custom layout with navigation rail, sidebar, and main content area

### User Interactions
- **Streamlit**: Form-based interactions with automatic rerun
- **Flet**: Event-driven with explicit UI updates

## Installation and Setup

1. **Install Flet dependencies:**
   ```bash
   pip install -r flet_requirements.txt
   ```

2. **Run the Flet application:**
   ```bash
   python flet_app.py
   ```

## Architecture

### Main Components

1. **GPXTrackWorkbench Class**: Main application controller
   - Manages app state
   - Handles UI updates
   - Coordinates between components

2. **State Management**: 
   - `flet_functions.py` provides Streamlit-like state access
   - Global app state dictionary
   - Helper functions for logging and tracing

3. **UI Components**:
   - **Sidebar**: Status displays and controls
   - **Navigation Rail**: Menu selection (Edit, Map, Speed, etc.)
   - **Main Content**: Dynamic content based on menu selection

4. **File Processing**:
   - Reuses existing `WorkingGPX` class
   - Adapted upload and selection interfaces
   - Compatible with existing processing modules

### Adaptation Strategy

The Flet version maintains compatibility with the existing codebase by:

1. **Preserving Core Logic**: Business logic in `WorkingGPX`, processing modules unchanged
2. **Adapter Pattern**: New UI components (`flet_uploader`, `flet_selector`) wrap existing functionality
3. **State Mapping**: `flet_functions.py` provides familiar state access patterns
4. **Modular Design**: Clear separation between UI and processing logic

## Current Implementation Status

### ✅ Completed
- Basic application structure
- File upload interface
- GPX selection interface  
- Navigation menu
- Status display system
- State management

### 🔄 In Progress / To Do
- Integration with existing processing modules (`editor.py`, `map.py`, etc.)
- File picker implementation testing
- Error handling and validation
- UI polish and responsive design
- Testing with actual GPX files

### 🎯 Future Enhancements
- Mobile-responsive layout
- Advanced file management
- Real-time processing updates
- Export/import functionality
- Settings and preferences

## Usage Notes

The Flet version aims to provide the same user experience as the Streamlit version but with the benefits of a native desktop application:

- **Performance**: Faster startup and response times
- **Offline**: No web server required
- **Integration**: Better OS integration (file dialogs, notifications)
- **Distribution**: Can be packaged as standalone executable

## Development Notes

When adapting Streamlit modules for Flet:

1. Replace `st.session_state` with `app_state` dictionary
2. Replace Streamlit widgets with Flet controls
3. Handle UI updates explicitly (call `.update()` methods)
4. Adapt form-based flows to event-driven patterns
5. Test file operations with actual file system access