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

The app is controled by the left-hand sidebar where the user is promoted to navigate to and choose one or more GPX files using [st.file_uploader](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader).  The function returns a list of `UploadedFile` objects saved in `st.session_state.file_list`.  There are NOT files or filenames!  Each `UploadedFile` object has a `.name` property and `ByteIO` contents.  

If a user "loads" one individual "file" it is automatically saved in a temporary "working copy" (`TEMP_DIR`) directory where it is also renamed to ensure there are no spaces in the filename. It is this "working copy" that populates the application's dataframe, and any changes made in the dataframe may be saved back into the "working copy", NOT the original choosen file!  

If the user elects to operate on all chosen files "in-bulk", each `UploadedFile` from `st.session_state.file_list` each will have a saved "working copy" in `TEMP_DIR`.  All operations impact the "working copy" file, NOT the original file!     

## st.session_state.file_list

As mentioned above, the list of `UploadedFile` objects is always held in the `file_list` session_state element.

## st.session_state.df

This session_state variable always holds the path of the current "working copy" file which.  This will NOT be the same as the original file!  Note that `session_state` cannot reliably hold a Pandas dataframe so functions are provided to `serialize` and `deserialize` working copy GPX files into CSV files and/or dataframes.  

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
