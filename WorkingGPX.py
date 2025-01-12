# Create the WorkingGPX and WGPXList classes 

import streamlit as st
from functions import utils as u

class WorkingGPX(object):
    
    # Constructor
    def __init__(self, source):
        self.df = None
        self.gpx = None
        self.alias = None
        self.fullname = None
        self.status = "Incomplete"
        
        # Identify what type of source we have
        t = type(source)
        # st.info(f"Constructor 'source' is type: {t}")

        # If source type is a Streamlit UploadedFile object...
        if t == st.runtime.uploaded_file_manager.UploadedFile:
            self.alias = source.name
            (df, gpx) = u.load_uploaded_to_dataframe(st, source)
            if df.info and gpx:
                self.df = df
                self.gpx = gpx
                self.fullname = u.save_temp_gpx(st, gpx, self.alias)
                self.status = "Constructed from UploadedFile"
            else:
                self.status = "Constructor Failed!"

        # All other sources... needs work!
        else:
            self.status = "Unknown 'source' type in Constructor"

    
    # Method
    def add_radius(self, r):
        self.radius = self.radius + r
        return(self.radius)
    

class GPXList( ):
    
    # Constructor
    def __init__(self):
        self.list = dict( )

    # Methods
    # --------------------------------------------------------------------

    def append(self, object):
        self.list[object.alias] = object
        count = len(self.list)
        return count
    