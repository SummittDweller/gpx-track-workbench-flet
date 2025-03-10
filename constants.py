# constants.py

APP_TITLE = 'GPX-Track-Workbench'

SELECT = "Select GPX Tracks"
UPLOAD = 'Upload GPX Data'
EDIT = 'Edit a GPX Track'
MAP = 'Map a GPX Track'
SPEED = 'Add Speed Tags'
TRIM = 'Trim Speed'
POST = 'Post Tracks to Hikes'
RESET = 'Reset!'

RAW_GPX_DIR = '/GitHub/GPX-Track-Workbench/sample_data'
TEMP_DIR = '/tmp/'
DF_CSV = '/tmp/dataframe.csv'

# RAW_GPX_DIR = '/Users/mark/Downloads/'

CONTENT_HIKES_DIR = '/GitHub/hikes/content/hikes/'
STATIC_GPX_DIR = '/GitHub/hikes/static/gpx/'

FILENAME_PATTERN = '*king 20*.gpx'
SELECT_ONLY = '.gpx'

TIME_ZONE = 'America/Chicago'
MAP_CENTER = [42, -92.5]

TEMP_DIR = '/tmp/'
TEMP_FILE = 'temporary.gpx'

TIME_DELTA_THRESHOLD = 2             # 2 hours
HDOP_THRESHOLD = 5.0                 # a random selection for now

SPEED_THRESHOLD = 5            # mph ~ note that 1 m/s = 2.2321 MPH
BIKE_SPEED_THRESHOLD = 25      # 25 mph ~ 11.2 m/s... for cycling
HIKE_POINTS_THRESHOLD = 180    # minimum points to be saved... 180=3 minutes

COLOR_PALETTE = [ '#0b2274', '#562aae', '#6d2ba2', '#c838d1', '#fe30b7', '#b2d8d8', '#66b2b2', '#008080', '#006666', '#004c4c' ] 
# 'Lolli2' from https://www.color-hex.com/color-palette/1036641 plus 'Shades of Teal' https://www.color-hex.com/color-palette/4666

OPEN_WEATHER_CALL = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={}&lon={}&dt={}&appid={}&units=imperial'
