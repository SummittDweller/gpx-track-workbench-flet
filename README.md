# GPX Track Workbench

A desktop/mobile application built with Flet for processing and analyzing GPX track data. Created by combining elements of [gpx2hikes](https://github.com/SummittDweller/gpx2hikes) and various GPX processing tools, this is the app I use to edit GPX tracks for upload to https://hikes.summittdweller.com.

## Features

- **GPX File Upload**: Drag-and-drop or browse to select multiple GPX files
- **Track Selection**: Choose specific tracks for processing with an intuitive interface
- **Track Editing**: Modify GPX track data and metadata
- **Interactive Mapping**: Visualize tracks on interactive maps
- **Speed Analysis**: Analyze and add speed tags to track data
- **Speed Trimming**: Remove sections of tracks based on speed thresholds
- **Track Publishing**: Post processed tracks to your hiking blog/website
- **Cross-platform**: Runs on Windows, macOS, Linux, and mobile
- **Native performance**: Desktop application with native OS integration
- **Offline Capable**: No internet connection required for core functionality

## Installation

### Prerequisites

- Python 3.8 or higher
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SummittDweller/gpx-track-workbench-flet.git
   cd gpx-track-workbench-flet
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r flet_requirements.txt
   ```

## Usage

### Quick Start

1. **Launch the application:**
   ```bash
   python run_flet.py
   ```
   
   or
   
   ```bash
   python flet_app.py
   ```

2. **Upload GPX files:**
   - Click "Upload GPX Data" button
   - Select one or more GPX files from your computer
   - Files will be processed and made available for selection

3. **Select tracks:**
   - Use the GPX Selector to choose which tracks to work with
   - Multiple tracks can be selected for batch operations

4. **Choose an action:**
   - **Edit**: Modify track data and metadata
   - **Map**: View tracks on an interactive map
   - **Speed**: Analyze and add speed information
   - **Trim**: Remove slow sections from tracks
   - **Post**: Publish tracks to your website

### Sample Data

The `sample_data/` directory contains example GPX files for testing:
- Various walking tracks with different characteristics
- Use these to explore the application features

## Architecture

### Built with Flet

- Modern UI framework for Python
- Cross-platform desktop and mobile support
- Native performance and responsive design

### Core Components

- **GPX Processing**: Robust GPX file parsing and manipulation
- **Mapping**: Interactive maps powered by Folium
- **Speed Analysis**: Sophisticated speed calculation and filtering
- **Data Export**: Multiple output formats and publishing options

## Development

### Project Structure

```
├── flet_app.py              # Main Flet application
├── run_flet.py              # Application launcher
├── FletStatusBox.py         # Status display component
├── flet_uploader.py         # File upload functionality
├── flet_selector.py         # Track selection interface
├── flet_functions.py        # State management utilities
├── WorkingGPX.py           # Core GPX processing class
├── constants.py            # Application constants
└── sample_data/            # Example GPX files
```

## Configuration

### Environment Variables

Set these in your environment or create a `.env` file:

```bash
# Default paths (adjust for your system)
RAW_GPX_DIR=/path/to/your/gpx/files
CONTENT_HIKES_DIR=/path/to/your/blog/content
STATIC_GPX_DIR=/path/to/your/blog/static/gpx

# Weather API (optional, for enhanced track information)
OPENWEATHER_API_KEY=your_api_key_here
```

### Speed Thresholds

Adjust speed analysis thresholds in `constants.py`:
- `SPEED_THRESHOLD`: Walking speed limit (default: 5 mph)
- `BIKE_SPEED_THRESHOLD`: Cycling speed limit (default: 25 mph)

## Contributing

Contributions are welcome! This project is part of a larger GPX processing ecosystem.

### Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. See the original project for license details.

## Related Projects

- **gpx2hikes**: Original GPX processing utilities
- **Blog Integration**: Automated publishing to hiking blogs

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: See `README_FLET.md` for technical implementation details
- **Examples**: Check the `sample_data/` directory for example files

## Acknowledgments

This Flet version builds upon various open-source GPX processing tools, providing a native desktop experience with powerful GPX processing capabilities.


   - Click "Upload GPX Data" button

   - Select one or more GPX files from your computerAll operations impact the `working_path` file, NEVER the original file!     

   - Files will be processed and made available for selection

## st.session_state.uploaded_list

3. **Select tracks:**

   - Use the GPX Selector to choose which tracks to work withAs mentioned above, the list file names for `UploadedFile` objects is always held in the `uploaded_list` `session_state` element.

   - Multiple tracks can be selected for batch operations

## st.session_state.working_list

4. **Choose an action:**

   - **Edit**: Modify track data and metadataMaintained in parallel to `session_state` `uploaded_list`, this list holds cooresponding working file names, NOT contents. 

   - **Map**: View tracks on an interactive map

   - **Speed**: Analyze and add speed information## st.session_state.working_path

   - **Trim**: Remove slow sections from tracks

   - **Post**: Publish tracks to your websiteThis `session_state` variable always holds the path of the current "working" file.



### Sample Data<div style="background-color: whitesmoke; color: black; border: 3px solid red; text-align: center; padding: 1em; margin: 1em;">

What follows is from the original 'Streamlit File Browser' project.  The information below may be obsolete! 

The `sample_data/` directory contains example GPX files for testing:</div>

- Various walking tracks with different characteristics

- Use these to explore the application features# Streamlit File Browser



## ArchitectureThis is a Streamlit application that acts as a file browser allowing you to navigate through folders and view the files and subfolders. It provides a convenient way to explore the file system and select files for further processing or analysis.



### Built with Flet## Usage

- **Cross-platform**: Runs on Windows, macOS, Linux, and mobile

- **Native performance**: Desktop application with native OS integrationThe file browser is implemented using the Streamlit library in Python. To run the application, simply execute the provided code. The application will start in your web browser, and you can interact with it to navigate through the folders and view the files.

- **Modern UI**: Clean, responsive interface built with Flet framework

The initial view of the file browser shows the current directory and its subfolders and files. You can click on a subfolder to navigate into it and view its contents. Similarly, clicking on a file will perform the desired action on the file, such as opening it or processing it further.

### Core Components

- **GPX Processing**: Robust GPX file parsing and manipulation!["exploer view"](st_explorer_1.jpg)

- **Mapping**: Interactive maps powered by Folium!["exploer view"](st_explorer_2.jpg)

- **Speed Analysis**: Sophisticated speed calculation and filtering

- **Data Export**: Multiple output formats and publishing options## Features



## Development- **Folder Navigation**: You can navigate through the folders by clicking on the subfolders in the file browser.

- **File Selection**: Clicking on a file will select it for further processing or analysis.

### Project Structure- **Dynamic Updates**: The file browser automatically updates to reflect changes in the directory structure or file system.

```- **Breadcrumb Navigation**: The current folder path is displayed as a breadcrumb trail, allowing you to easily track your location within the file system.

├── flet_app.py              # Main Flet application- **Customization**: You can customize the font size and colors of the file browser to suit your preferences.

├── FletStatusBox.py         # Status display component

├── flet_uploader.py         # File upload functionality## Potential Improvements

├── flet_selector.py         # Track selection interface

├── flet_functions.py        # State management utilities- **File Actions**: Currently, the file browser only displays the files and folders. It could be enhanced to allow various actions to be performed on the files, such as opening, editing, or deleting them.

├── WorkingGPX.py           # Core GPX processing class- **File Filtering**: Adding the ability to filter files based on their names, extensions, or other attributes would make it easier to find specific files in large directories.

├── constants.py            # Application constants- **Sorting**: Providing options to sort the files and folders alphabetically or by other criteria would improve the usability of the file browser.

├── functions.py            # Utility functions- **File Previews**: Adding the ability to preview file contents (such as text or images) directly in the file browser would eliminate the need to open them in external applications for quick inspection.

├── editor.py               # Track editing functionality

├── map.py                  # Mapping functionality## Conclusion

├── speed.py                # Speed analysis

├── post.py                 # Publishing functionalityThe Streamlit file browser is a useful tool for exploring and selecting files in a directory structure. It provides an intuitive user interface and can be easily customized and extended to suit different use cases. By implementing additional features and improvements, it can become a powerful file management and analysis tool.

└── sample_data/            # Example GPX files

```# streamlit-option-menu



### Key Features of Flet Version![](./img/menu.png)

- **Desktop Native**: No browser required, runs as a standalone application![](./img/horizontal_menu.png)

- **File System Access**: Direct access to local files and folders![](./img/styled_menu.png)

- **Better Performance**: Faster startup and processing compared to web version

- **Offline Capable**: No internet connection required for core functionalitystreamlit-option-menu is a simple Streamlit component that allows users to select a single item from a list of options in a menu.

It is similar in function to st.selectbox(), except that:

## Configuration- It uses a simple static list to display the options instead of a dropdown

- It has configurable icons for each option item and the menu title

### Environment Variables- The CSS styles of most HTML elements in the menu can be customized (see the styles parameter and Example #3 below)

Set these in your environment or create a `.env` file:

It is built on [streamlit-component-template-vue](https://github.com/andfanilo/streamlit-component-template-vue), styled with [Bootstrap](https://getbootstrap.com/) and with icons from [bootstrap-icons](https://icons.getbootstrap.com/)

```bash

# Default paths (adjust for your system)## Installation

RAW_GPX_DIR=/path/to/your/gpx/files```

CONTENT_HIKES_DIR=/path/to/your/blog/contentpip install streamlit-option-menu

STATIC_GPX_DIR=/path/to/your/blog/static/gpx```



# Weather API (optional, for enhanced track information)## Parameters

OPENWEATHER_API_KEY=your_api_key_hereThe `option_menu` function accepts the following parameters:

```- menu_title (required): the title of the menu; pass None to hide the title

- options (required): list of (string) options to display in the menu; set an option to "---" if you want to insert a section separator

### Speed Thresholds- default_index (optional, default=0): the index of the selected option by default

Adjust speed analysis thresholds in `constants.py`:- menu_icon (optional, default="menu-up"): name of the [bootstrap-icon](https://icons.getbootstrap.com/) to be used for the menu title

- `SPEED_THRESHOLD`: Walking speed limit (default: 5 mph)- icons (optional, default=["caret-right"]): list of [bootstrap-icon](https://icons.getbootstrap.com/) names to be used for each option; its length should be equal to the length of options

- `BIKE_SPEED_THRESHOLD`: Cycling speed limit (default: 25 mph)- orientation (optional, default="vertical"): "vertical" or "horizontal"; whether to display the menu vertically or horizontally

- styles (optional, default=None): A dictionary containing the CSS definitions for most HTML elements in the menu, including:

## Contributing    * "container": the container div of the entire menu

    * "menu-title": the &lt;a> element containing the menu title

Contributions are welcome! This project is part of a larger GPX processing ecosystem.    * "menu-icon": the icon next to the menu title

    * "nav": the &lt;ul> containing "nav-link"

### Getting Started    * "nav-item": the &lt;li> element containing "nav-link"

1. Fork the repository    * "nav-link": the &lt;a> element containing the text of each option

2. Create a feature branch    * "nav-link-selected": the &lt;a> element containing the text of the selected option

3. Make your changes    * "icon": the icon next to each option

4. Add tests if applicable    * "separator": the &lt;hr> element separating the options

5. Submit a pull request- manual_select: Pass to manually change the menu item selection. 

The function returns the (string) option currently selected

## License- on_change: A callback that will happen when the selection changes. The callback function should accept one argument "key". You can use it to fetch the value of the menu (see [example 5](#examples))



This project is open source. See the original project for license details.



## Related Projects### Manual Selection

This option was added to allow the user to manually move to a specific option in the menu. This could be useful when the user wants to move to another option automatically after finishing with one option (for example, if settings are approved, then move back to the main option).

- **Original Streamlit Version**: Web-based GPX Track Workbench

- **Blog Integration**: Automated publishing to hiking blogsTo use this option, you need to pass the index of the desired option as `manual_select`. **Notice**: This option behaves like a button. This means that you should only pass `manual_select` once when you want to select the option, and not keep it as a constant value in your menu creation call (see example below).



## Support

## Examples

- **Issues**: Report bugs and request features via GitHub Issues```python

- **Documentation**: See `README_FLET.md` for technical implementation detailsimport streamlit as st

- **Examples**: Check the `sample_data/` directory for example filesfrom streamlit_option_menu import option_menu



## Acknowledgments# 1. as sidebar menu

with st.sidebar:

This Flet version builds upon the original Streamlit GPX Track Workbench, providing a native desktop experience while maintaining all the powerful GPX processing capabilities.    selected = option_menu("Main Menu", ["Home", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected

# 2. horizontal menu
selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2

# 3. CSS style definitions
selected3 = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

# 4. Manual item selection
if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
    manual_select = st.session_state['menu_option']
else:
    manual_select = None
    
selected4 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    orientation="horizontal", manual_select=manual_select, key='menu_4')
st.button(f"Move to Next {st.session_state.get('menu_option', 1)}", key='switch_button')
selected4

# 5. Add on_change callback
def on_change(key):
    selection = st.session_state[key]
    st.write(f"Selection changed to {selection}")
    
selected5 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
                        icons=['house', 'cloud-upload', "list-task", 'gear'],
                        on_change=on_change, key='menu_5', orientation="horizontal")
selected5
```