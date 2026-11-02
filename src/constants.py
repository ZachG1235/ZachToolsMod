# File Paths
SOURCE_TOOL_PATH = r"\CopyingSources"

RAT_PATHS = [
    r"\DDRTools\PC\service\app\misc\rat_list.txt",
    r"\DDRTools\PC\eval\win-x64\rats.txt",
    r"\DDRTools\PC\eval\win-arm64\rats.txt"
]
NEW_RAT_LIST = [
    "*HopToDesk*\n"
]
EXTRAS_PATH = r"\_extras"
DDR_DATE_MODIFIED_PATH = r""
ZOOLS_DATA_FILE_PATH = r"\_extras\src\Zools"
ZOOLS_NOTE_TEMPLATE_PATH = r"\_extras\src\Zools"

# NAMING CONSTANTS 
GRAB_SERIALS_SCRIPT_NAME = "ZOOLS_Grab-Serial.bat"
DDRTOOLS_DRIVE_NAME_SINGLE = r"DDRX_PE"
DDRTOOLS_DRIVE_NAME_MULTI = r"DDRx_Multi"
ZOOLS_DATA_FILE = "ZoolsDataFile.txt"
DDRTOOLS_DATE_MODIFIED_TIMESTAMP_FILE = ".timestamp"
BLOG_FILE_NAME = "blogs.json"
ZOOLS_NOTES_TEMPLATE_FILENAME = "Note_Template.txt"
ZOOLS_NOTES_TEMPLATE_BAT_FILENAME = "ZOOLS_Notes-Template-Insert.bat"
ZOOLS_NOTES_TEMPLATE_PS1_FILENAME = "ZOOLS_Notes-Template-Insert.ps1"
ZOOLS_NOTES_TEMPLATE_BAT_GUI_FILENAME = "ZOOLS_Notes-Template-GUI.bat"
ZOOLS_NOTES_TEMPLATE_PS1_GUI_FILENAME = "ZOOLS_Notes-Template-GUI.ps1"


# BOOLS
MODIFY_RAT_LIST = False
ADD_SERIAL_SCRIPT = True
DO_GUI = True
MODIFY_RAT_PATH = [
    True,
    True,
    True
]
ADD_NOTE_TEMPLATE_SCRIPT = False
ADD_NOTE_TEMPLATE_GUI_SCRIPT = True

# NUMBERS
#DDRTOOLS_DAYS_SINCE_UPDATED_GOOD = 0  # 0 - 1,    Good
DDRTOOLS_DAYS_SINCE_UPDATED_OKAY = 2  # 2 - 4,   ok
DDRTOOLS_DAYS_SINCE_UPDATED_BAD = 5   # 5 - inf, bad

#ZOOLS_DAYS_SINCE_UPDATED_GOOD = 0  # 0 - 1,    Good
ZOOLS_DAYS_SINCE_UPDATED_OKAY = 2  # 2 - 4,   ok
ZOOLS_DAYS_SINCE_UPDATED_BAD = 5   # 5 - inf, bad

REFRESH_DRIVE_LIST_TIMEOUT_MILLISECONDS = 8000


# KEYS
ZKEY_LAST_DATE_UPDATED = "last_date_updated"
ZKEY_LAST_DATE_UPDATED_VERSION = "last_date_updated_version"
CURRENT_VERSION = "1.1.0"
HOTFIX_VERSION_ZERO_NAME = "Release"

# # # GUI THINGS # # # 
# COLORS
COLOR_DDRTOOLS_DAYS_SINCE_UPDATED_GOOD = "#17a704"
COLOR_DDRTOOLS_DAYS_SINCE_UPDATED_OKAY = "#918700"
COLOR_DDRTOOLS_DAYS_SINCE_UPDATED_BAD = "#da0000"
COLOR_ZOOLS_DAYS_SINCE_UPDATED_GOOD = "#17a704"
COLOR_ZOOLS_DAYS_SINCE_UPDATED_OKAY = "#918700"
COLOR_ZOOLS_DAYS_SINCE_UPDATED_BAD = "#da0000"

GUI_THEME_COLORS = {
    "Red": {
        "HeaderBG": "#d99b9b",
        "LeftPanelBG" : "#ffc5c5",
        "LeftPanelButtonBG" : "#d99b9b",
        "MainPanelButton": "#FFB0B0"
    },
    "Blue": {
        "HeaderBG": "#a69bd9",
        "LeftPanelBG" : "#d9c5ff",
        "LeftPanelButtonBG" : "#9f9bd9",
        "MainPanelButton": "#B1B0FF"
    }
}

# VERSION NAMES
# major: Color
# minor: celestial body
# roman numeral
VERSION_NAMING_SCHEMES = {
    "0": {
        "NAME": "Red",
            "0" : "Mercury",
            "1" : "Venus",
            "2" : "Earth",
            "3" : "Mars",
            "4" : "Jupiter",
            "5" : "Saturn",
            "6" : "Uranus",
            "7" : "Neptune",
    },
    "1": {
        "NAME": "Blue",
            "0" : "Water",
            "1" : "Branch",
            "2" : "Cloud",
            "3" : "Soil",
            "4" : "Grass",
            "5" : "Weather",
            "6" : "Leaf",
            "7" : "Breeze",
            "8" : "Shrub",
            "9" : "Foliage",
    },
    "2": {}
}

# DEBUG CONSTANTS
DBG_USE_DUMMY_DRIVES = False
DBG_DISPLAY_TIMESTAMP_AS_NOW = False