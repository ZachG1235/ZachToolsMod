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
DATE_MODIFIED_PATH = r"\DDRTools\PC\service\scripts\src\Logs"

# NAMING CONSTANTS 
GRAB_SERIALS_SCRIPT_NAME = "ZOOLS_Grab-Serial.bat"
DDRTOOLS_DRIVE_NAME_SINGLE = r"DDRX_PE"
DDRTOOLS_DRIVE_NAME_MULTI = r"DDRx_Multi"
ZOOLS_DATE_MODIFIED_TIMESTAMP_FILE = ".ZoolsTimestamp.txt"
ZOOLS_DATA_FILE = "ZoolsDataFile.txt"
DDRTOOLS_DATE_MODIFIED_TIMESTAMP_FILE = "ddrlog.txt"
BLOG_FILE_NAME = "blogs.json"


# BOOLS
MODIFY_RAT_LIST = True
ADD_SERIAL_SCRIPT = True
DO_GUI = True


# KEYS
ZKEY_LAST_DATE_UPDATED = "last_date_updated"
CURRENT_VERSION = "0.1.2"



# DEBUG CONSTANTS
DBG_USE_DUMMY_DRIVES = False
DBG_DISPLAY_TIMESTAMP_AS_NOW = False