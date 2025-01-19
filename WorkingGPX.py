# Create the WorkingGPX and GPXList classes 

import streamlit as st
import functions as f
import gpxpy

# get_track_center - Calculate map center (lat, lon) from a gpxpy track object
# --------------------------------------------------------------------------------
def get_track_center(gpx):
    lats = []
    lons = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lats.append(point.latitude)
                lons.append(point.longitude)
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    return center_lat, center_lon


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
            (df, gpx) = f.uploaded_to_working(st, source)
            if df.info and gpx:
                self.df = df
                self.gpx = gpx
                self.fullname = f.save_temp_gpx(st, gpx, self.alias)
                self.center = get_track_center(gpx)
                self.status = "Constructed from UploadedFile"
            else:
                self.status = "Constructor Failed!"

        # All other sources... needs work!
        else:
            self.status = "Unknown 'source' type in Constructor"

    
    # Methods

    # update_from_df(df) - Given a GPX dataframe, update the corresponding WorkingGPX object
    # --------------------------------------------------------------------------------
    def update_from_df(self, df):
        self.df = df
        g = self.gpx = f.dataframe_to_gpx(df)
        self.center = get_track_center(g)
        with open(self.fullname, 'w') as wf:
            wf.write(g.to_xml( ))
        msg = f"WorkingGPX.update_from_df( ) has updated object '{self.alias}' as '{self.fullname}'."
        f.state('logger').info(msg)
        # Store the new object in our GPXdict
        d = f.state('GPXdict')
        d[self.alias] = self
        st.session_state.GPXdict = d
        return self


    # update_from_file(alias) - Given a GPX file, update the corresponding WorkingGPX object
    # --------------------------------------------------------------------------------
    def update_from_file(self, fullname):
        try:
            with open(fullname) as g:
                gpx_contents = g.read( )
                gpx = gpxpy.parse(gpx_contents)
        except Exception as e:
            st.exception(f"Exception: {e}")
            return False
        df = f.gpx_to_dataframe(st, gpx)
        if df and gpx:
            self.fullname = fullname
            self.df = df
            self.gpx = gpx
            self.center = get_track_center(gpx)
            self.status = "Updated from GPX file {fullname}"
            # Store the new object in our GPXdict
            d = f.state('GPXdict')
            d[self.alias] = self
            st.session_state.GPXdict = d
            return self
        else:
            st.error(f"Unable to update WorkingGPX[{self.alias}] from file {fullname}")
        return False



# def load_working(st, workingGPX):
#     gpx = False
#     working_path = workingGPX.fullname
#     try:
#         with open(working_path) as w:
#             gpx_contents = w.read( )
#             gpx = gpxpy.parse(gpx_contents)
#     except Exception as e:
#         st.exception(f"Exception: {e}")
#         return False
#     df = gpx_to_dataframe(st, gpx, working_path)
#     return (df, gpx)





        g = self.gpx = f.dataframe_to_gpx(df)
        self.center = get_track_center(g)
        with open(self.fullname, 'w') as wf:
            wf.write(g.to_xml( ))
        msg = f"WorkingGPX.update_from_df( ) has updated object '{self.alias}' as '{self.fullname}'."
        f.state('logger').info(msg)
        # Store the new object in our GPXdict
        d = f.state('GPXdict')
        d[self.alias] = self
        st.session_state.GPXdict = d
        return self


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
    
    # print_GPXdict(st) - Print datafraes of all gox_list objects
    # ------------------------------------------------------------------------------------
    def print_GPXdict(self, st):
        Gd = f.state('GPXdict')
        if Gd:
            for key, WG in Gd.list.items( ):
                heading = f"{key} is {WG.fullname}"
                st.header(heading)
                st.write(WG.df)
        else:
            st.warning(f"print_GPXdict( ) called but there is no list to print")
