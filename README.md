# GPX-Track-Editor

Created by combining elements of [gpx2hikes](https://github.com/SummittDweller/gpx2hikes) and [streamlit-folium](https://github.com/randyzwitch/streamlit-folium), this is the app I use to edit GPX tracks for upload to https://hikes.summittdweller.com. 

## Building Locally from Scratch

The following command sequence is recommended when building this app locally.  

```zsh
╭─mark@Marks-Mac-Mini ~/GitHub/GPX-Track-Workbench ‹main› 
╰─$ python3 -m venv .venv  
╭─mark@Marks-Mac-Mini ~/GitHub/GPX-Track-Workbench ‹main*› 
╰─$ source .venv/bin/activate
(.venv) ╭─mark@Marks-Mac-Mini ~/GitHub/GPX-Track-Workbench ‹main*› 
╰─$ python --version  
Python 3.13.1
(.venv) ╭─mark@Marks-Mac-Mini ~/GitHub/GPX-Track-Workbench ‹main*› 
╰─$ pip3 install -r python_requirements.txt
```

If there are updates made to the packages be sure to...   

```zsh
(.venv) ╭─mark@Marks-Mac-Mini ~/GitHub/GPX-Track-Workbench ‹main*› 
╰─$ pip3 freeze > python_requirements.txt      
```

## Running the App Locally

Like so:  

```zsh
(.venv) ╭─mark@Marks-Mac-Mini ~/GitHub/GPX-Track-Workbench ‹main*› 
╰─$ streamlit run app.py
```

If that does not work, or to debug in VSCode, you should be more specific, like this:  

```zsh
(.venv) ╭─mark@Marks-Mac-Mini ~/GitHub/GPX-Track-Workbench ‹main*› 
╰─$ cd /Users/mark/GitHub/GPX-Track-Workbench; 
/usr/bin/env /Users/mark/GitHub/GPX-Track-Workbench/.venv/bin/python /Users/mark/.vscode/extensions/ms-python.debugpy-2024.15.2024121701-darwin-x64/bundled/libs/debugpy/adapter/../../debugpy/launcher 51475 -- -m streamlit run /Users/mark/GitHub/GPX-Track-Workbench/app.py --server.port 2000 
```

...or just open the `app.py` file in VSCode and then `start the debugger from within the project's VSCode environment`.  

# Basic Operation

The app is controled by the left-hand sidebar where the user is promoted to navigate to and choose one or more GPX files using [st.file_uploader](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader).  Selecting the GPX files creates a list `UploadedFile` objects.  A temporary file in TEMP_DIR, with a sanitized file name built from the `UploadedFile` `.name` property, is created and the temp file names populate `session_state['working_list']` in parallel to`session_state['uploaded_list']`.  

Each `UploadedFile` object has a `.name` property and `ByteIO` contents, but once the `working_list` files have been created they are used exclusively.    

The most important component in the code is `session_state['working_path']` which holds the complete file path of the CURRENT working file!  The contents of `working_path` is NEVER held in session_state, instead functions are provided to load its GPX data into either a Pandas `dataframe` or `df` variable, or into a `gpxPy` structure usually named `gpx`.    

All operations impact the `working_path` file, NEVER the original file!     

## st.session_state.uploaded_list

As mentioned above, the list file names for `UploadedFile` objects is always held in the `uploaded_list` `session_state` element.

## st.session_state.working_list

Maintained in parallel to `session_state` `uploaded_list`, this list holds cooresponding working file names, NOT contents. 

## st.session_state.working_path

This `session_state` variable always holds the path of the current "working" file.

<div style="background-color: whitesmoke; color: black; border: 3px solid red; text-align: center; padding: 1em; margin: 1em;">
What follows is from the original 'Streamlit File Browser' project.  The information below may be obsolete! 
</div>

# Streamlit File Browser

This is a Streamlit application that acts as a file browser allowing you to navigate through folders and view the files and subfolders. It provides a convenient way to explore the file system and select files for further processing or analysis.

## Usage

The file browser is implemented using the Streamlit library in Python. To run the application, simply execute the provided code. The application will start in your web browser, and you can interact with it to navigate through the folders and view the files.

The initial view of the file browser shows the current directory and its subfolders and files. You can click on a subfolder to navigate into it and view its contents. Similarly, clicking on a file will perform the desired action on the file, such as opening it or processing it further.

!["exploer view"](st_explorer_1.jpg)
!["exploer view"](st_explorer_2.jpg)

## Features

- **Folder Navigation**: You can navigate through the folders by clicking on the subfolders in the file browser.
- **File Selection**: Clicking on a file will select it for further processing or analysis.
- **Dynamic Updates**: The file browser automatically updates to reflect changes in the directory structure or file system.
- **Breadcrumb Navigation**: The current folder path is displayed as a breadcrumb trail, allowing you to easily track your location within the file system.
- **Customization**: You can customize the font size and colors of the file browser to suit your preferences.

## Potential Improvements

- **File Actions**: Currently, the file browser only displays the files and folders. It could be enhanced to allow various actions to be performed on the files, such as opening, editing, or deleting them.
- **File Filtering**: Adding the ability to filter files based on their names, extensions, or other attributes would make it easier to find specific files in large directories.
- **Sorting**: Providing options to sort the files and folders alphabetically or by other criteria would improve the usability of the file browser.
- **File Previews**: Adding the ability to preview file contents (such as text or images) directly in the file browser would eliminate the need to open them in external applications for quick inspection.

## Conclusion

The Streamlit file browser is a useful tool for exploring and selecting files in a directory structure. It provides an intuitive user interface and can be easily customized and extended to suit different use cases. By implementing additional features and improvements, it can become a powerful file management and analysis tool.

# streamlit-option-menu

![](./img/menu.png)
![](./img/horizontal_menu.png)
![](./img/styled_menu.png)

streamlit-option-menu is a simple Streamlit component that allows users to select a single item from a list of options in a menu.
It is similar in function to st.selectbox(), except that:
- It uses a simple static list to display the options instead of a dropdown
- It has configurable icons for each option item and the menu title
- The CSS styles of most HTML elements in the menu can be customized (see the styles parameter and Example #3 below)

It is built on [streamlit-component-template-vue](https://github.com/andfanilo/streamlit-component-template-vue), styled with [Bootstrap](https://getbootstrap.com/) and with icons from [bootstrap-icons](https://icons.getbootstrap.com/)

## Installation
```
pip install streamlit-option-menu
```

## Parameters
The `option_menu` function accepts the following parameters:
- menu_title (required): the title of the menu; pass None to hide the title
- options (required): list of (string) options to display in the menu; set an option to "---" if you want to insert a section separator
- default_index (optional, default=0): the index of the selected option by default
- menu_icon (optional, default="menu-up"): name of the [bootstrap-icon](https://icons.getbootstrap.com/) to be used for the menu title
- icons (optional, default=["caret-right"]): list of [bootstrap-icon](https://icons.getbootstrap.com/) names to be used for each option; its length should be equal to the length of options
- orientation (optional, default="vertical"): "vertical" or "horizontal"; whether to display the menu vertically or horizontally
- styles (optional, default=None): A dictionary containing the CSS definitions for most HTML elements in the menu, including:
    * "container": the container div of the entire menu
    * "menu-title": the &lt;a> element containing the menu title
    * "menu-icon": the icon next to the menu title
    * "nav": the &lt;ul> containing "nav-link"
    * "nav-item": the &lt;li> element containing "nav-link"
    * "nav-link": the &lt;a> element containing the text of each option
    * "nav-link-selected": the &lt;a> element containing the text of the selected option
    * "icon": the icon next to each option
    * "separator": the &lt;hr> element separating the options
- manual_select: Pass to manually change the menu item selection. 
The function returns the (string) option currently selected
- on_change: A callback that will happen when the selection changes. The callback function should accept one argument "key". You can use it to fetch the value of the menu (see [example 5](#examples))



### Manual Selection
This option was added to allow the user to manually move to a specific option in the menu. This could be useful when the user wants to move to another option automatically after finishing with one option (for example, if settings are approved, then move back to the main option).

To use this option, you need to pass the index of the desired option as `manual_select`. **Notice**: This option behaves like a button. This means that you should only pass `manual_select` once when you want to select the option, and not keep it as a constant value in your menu creation call (see example below).


## Examples
```python
import streamlit as st
from streamlit_option_menu import option_menu

# 1. as sidebar menu
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Settings'], 
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