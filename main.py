# Import libraries
import shutil, os, ctypes, time, json, random, string
import tkinter as tk
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Import own libraries 
import constants


root = tk.Tk()
global_drive_info = []
drive_enablement = dict({})

def GetConnectedDrives():
    drive_info = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()

    DRIVE_REMOVABLE = 2
    DRIVE_FIXED = 3

    for i in range(26):
        if not bitmask & (1 << i):
            continue
    
        letter = chr(65 + i)
        root = f"{letter}:\\"

        drive_type = ctypes.windll.kernel32.GetDriveTypeW(root)

        if drive_type not in (DRIVE_REMOVABLE, DRIVE_FIXED):
            continue

        volume_name = ctypes.create_unicode_buffer(261)

        start = time.perf_counter()
        success = ctypes.windll.kernel32.GetVolumeInformationW(root, volume_name, len(volume_name), None, None, None, None, 0)
        elapsed = time.perf_counter() - start

        print(f"{letter}: volume query took {elapsed:.3f}s")

        if success:
            drive_info.append((letter, volume_name.value))

    return drive_info

def GetToolDrives(connected_drives):
    tool_drives = []
    for drive in connected_drives:
        if constants.DDRTOOLS_DRIVE_NAME_MULTI.upper() == drive[1].upper() or constants.DDRTOOLS_DRIVE_NAME_SINGLE.upper() == drive[1].upper():
            tool_drives.append(drive)
    return tool_drives


def ModifyRats(drive_letter:str):
    if not constants.MODIFY_RAT_LIST:
        print("Modify rat list is disabled.")
        return 0

    rat_modification_count = 0
    for each_rat_path in constants.RAT_PATHS:
        current_rat_path = Path(drive_letter + ":" + each_rat_path)

        if current_rat_path.exists():
            with open(current_rat_path, 'r') as rat_list_file:
                existing_lines = set(rat_list_file.read().splitlines())

                new_lines = [
                    line for line in constants.NEW_RAT_LIST
                    if line.rstrip("\n") not in existing_lines
                ]

                if new_lines:
                    with open(current_rat_path, 'a') as rat_list_file:
                        rat_list_file.writelines(new_lines)
                    print(f"Successfully updated RAT list at {current_rat_path}")
                    rat_modification_count += 1
                else:
                    print(f"RAT list already contains the new entries.")
        else:
            print(f"There is no longer a RAT file at {current_rat_path}")
    return rat_modification_count


            
def AddSerialScript(drive_letter:str):
    if not constants.ADD_SERIAL_SCRIPT:
        print("Adding serial script is disabled")
        return 0

    current_extras_path = Path(drive_letter + ":" + constants.EXTRAS_PATH)
    if current_extras_path.is_dir():
        source_file = os.getcwd() + "\\" + constants.SOURCE_TOOL_PATH + "\\" + constants.GRAB_SERIALS_SCRIPT_NAME
        if (current_extras_path / constants.GRAB_SERIALS_SCRIPT_NAME).is_file():
            shutil.copy2(source_file, current_extras_path)
            print(f"Re-copied Grab Serial script on drive letter {drive_letter}.")
        else:
            shutil.copy2(source_file, current_extras_path)
            print(f"Successfully added Grab Serial script on drive letter {drive_letter}.")
        return 1
    else:
        print(f"There was a problem accessing the extras folder on drive letter {drive_letter}.")
        return 0

def PerformUpdate(drive):
    operation_start = time.perf_counter()
    total_modifications = 0

    print(f"=== Attempting to Modify {drive[1]} on drive letter {drive[0]}: ...")

    total_modifications += ModifyRats(drive[0])
    total_modifications += AddSerialScript(drive[0])

    print(f"Operations took {time.perf_counter() - operation_start:.3f} seconds")
    print(f"= Made {total_modifications} total modifications to {drive[1]}!!!")
    
def SetGlobalDrives(drive):
    global global_drive_info
    global_drive_info = drive

def ProduceWindow():
    root.title("Zools GUI")
    root.geometry("800x700")
    root.configure(bg="#7f8385") 


    top_label = tk.Label(root, text="ZOOLS", font=("Arial", 18))
    top_label.pack(pady=15)

    AddConfigurationOptions()

    root.mainloop()

def AddConfigurationOptions():
    paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    left_pane = tk.Frame(paned_window, width=200, relief=tk.SUNKEN, bg="#ffc5c5")
    paned_window.add(left_pane)

    left_label = tk.Label(left_pane, text="Connected Drives", font=("Arial", 12))
    left_label.grid(row=0, column=0, pady=20, padx=10, columnspan=2)

    global drive_enablement
    drive_enablement = {}
    i = 0
    for each_drive in global_drive_info:
        lbl = tk.Label(left_pane, text=f"{each_drive[1]} ({each_drive[0]}:)", font=("Arial", 12))
        lbl.grid(row=1+i, column=0, pady=(5, 0), padx=10)

        # get updated time
        last_date_modified = GetLastModifiedDateFromDrive(each_drive[0])
        if constants.DBG_DISPLAY_TIMESTAMP_AS_NOW:
            last_date_modified = datetime.now(timezone(timedelta(hours=-7)))

        if last_date_modified == None:
            last_date_modified = "Not Modified"
        else:
            # "Wed, Oct 3rd 2026 (12:45pm)"
            first_part = last_date_modified.strftime("%a, %b %#d")
            last_part = last_date_modified.strftime(" %Y (%#I:%M %p)").lower()
            last_date_modified = f"{first_part}{GetOrdinalSuffix(int(last_date_modified.strftime("%#d")))}{last_part}"

        lbl_subtitle = tk.Label(left_pane, text=last_date_modified, font=("Arial", 10))
        lbl_subtitle.grid(row=2+i, column=0, pady=(0, 20), padx=10)

        drive_enablement[each_drive[0]] = tk.BooleanVar(value=True)
        checkbox = tk.Checkbutton(left_pane, variable=drive_enablement[each_drive[0]], anchor="center", command=lambda drive_letter=each_drive[0]: CheckButtonModified(drive_letter))
        checkbox.grid(row=1+i, column=1, rowspan=2, padx=5)
        i += 2


    right_pane = tk.Frame(paned_window, width=400, relief=tk.SUNKEN)
    paned_window.add(right_pane)

    right_label = tk.Label(right_pane, text="Main Content Window", font=("Arial", 14))
    right_label.pack(pady=20, padx=10)

def CheckButtonModified(id):
    global drive_enablement
    print(f"Drive {id} is now {drive_enablement[id].get()}")

def GetLastModifiedDateFromDrive(letter):
    zools_data_path = Path(letter + ":\\" + constants.ZOOLS_DATA_FILE)
    data = {}
    if zools_data_path.is_file():
        with open(zools_data_path, 'r', encoding='utf-8') as file_raw:
            data = json.load(file_raw)
        if constants.ZKEY_LAST_DATE_UPDATED in data:
            return data[constants.ZKEY_LAST_DATE_UPDATED]
    return None

def SetLastModifiedDateOnDrive(letter, time_to_set):
    zools_data_path = Path(letter + ":\\" + constants.ZOOLS_DATA_FILE)
    data = {}
    if zools_data_path.is_file():
        with open(zools_data_path, 'r', encoding='utf-8') as file_raw:
            data = json.load(file_raw)
    data[constants.ZKEY_LAST_DATE_UPDATED] = time_to_set
    WriteToZoolsDataFile(zools_data_path, data)
    
def WriteToZoolsDataFile(pathToWriteTo, dataToWrite):
    with open(pathToWriteTo, 'w', encoding='utf-8') as filePointer:
        json.dump(dataToWrite, filePointer, indent=4, sort_keys=True)

    # Make file hidden on Windows system (this totally breaks on anything else lol)
    FILE_ATTRIBUTE_HIDDEN = 0x02
    success = ctypes.windll.kernel32.SetFileAttributesW(str(pathToWriteTo), FILE_ATTRIBUTE_HIDDEN)

def GetOrdinalSuffix(day):
    if day >= 11 and day <= 13:
        return "th"
    
    last_digit = day % 10
    if last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    else:
        return "th"

def GenerateDummyDriveList():
    # tool drive cant be C so add it to the pool of unavailable drive letters
    unavailable_letters = ['C']
    dummy_drives = []

    # Generate a random of 1 - 7 drives
    for j in range(0, random.randint(1, 7)):
        # randomly choose a drive letter that hasnt be chosen already
        letter_chosen = 'C'
        while letter_chosen in unavailable_letters:
            letter_chosen = random.choice(string.ascii_uppercase)

        # 50% chance to be named multi instead of single
        dummy_tool_name_source = constants.DDRTOOLS_DRIVE_NAME_SINGLE
        if random.randint(0, 1) % 2 == 0:
            dummy_tool_name_source = constants.DDRTOOLS_DRIVE_NAME_MULTI
        dummy_tool_name_source.upper()

        # randomize the capitalization of the drive name
        dummy_tool_name = ""
        for i in range(0, len(dummy_tool_name_source)):
            # 50% chance for each letter to be lowercase
            if random.randint(0, 1) % 2 == 0:
                dummy_tool_name += dummy_tool_name_source[i].lower()
            else:
                dummy_tool_name += dummy_tool_name_source[i]

        dummy_drives.append((letter_chosen, dummy_tool_name))
        unavailable_letters.append(letter_chosen)

    return dummy_drives


        




def main():
    start = time.perf_counter()

    drive_info = GetConnectedDrives()
    print(f"Drive detection took: {time.perf_counter() - start:.3f} seconds")
    # filter by only tools
    tool_drives = GetToolDrives(drive_info)

    # set the global drives
    SetGlobalDrives(tool_drives)

    if constants.DO_GUI:
        if constants.DBG_USE_DUMMY_DRIVES:
            dummy_drive_list = GenerateDummyDriveList()
            print(dummy_drive_list)
            SetGlobalDrives(dummy_drive_list)
        ProduceWindow()
        return
    
    for drive in tool_drives:
        PerformUpdate(drive)

    if len(tool_drives) < 1:
        print("There were no tool drives detected. Please insert new drives and run this program again.")


main()