# Import libraries
import shutil, os, ctypes, time, json, random, string
import tkinter as tk
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Import own libraries 
import constants
from utils.checkbtn import CustomCheckbutton 

# Global variables
root = tk.Tk()

paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
left_pane = tk.Frame(paned_window, width=200, relief=tk.SUNKEN, bg="#ffc5c5")
drive_list_frame = tk.Frame(left_pane, bg="#ffc5c5")
right_pane = tk.Frame(paned_window, width=400, relief=tk.SUNKEN)

text_frame = tk.Frame(right_pane)
scrollbar = tk.Scrollbar(text_frame)
text_box = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Sitka Text", 11), padx=10, pady=10)

global_drive_info = []
drive_enablement = dict({})
currently_updating = False
current_blog_version = constants.CURRENT_VERSION


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#   Performing Operations on Tools
# # # # # # # # # # # # # # # # # # # # 

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

def RevertRats(drive_letter:str):
    rat_revert_count = 0
    lines_to_remove = {line.rstrip("\r\n") for line in constants.NEW_RAT_LIST}
    for each_rat_path in constants.RAT_PATHS:
        current_rat_path = Path(drive_letter + ":" + each_rat_path)

        if not current_rat_path.exists():
            print(f"There is no longer a rat file at {current_rat_path}")
        
        with open(current_rat_path, 'r', newline="") as rat_list_file:
            existing_lines = rat_list_file.readlines()

        filtered_lines = [line for line in existing_lines if line.rstrip("\r\n") not in lines_to_remove]

        removed_count = len(existing_lines) - len(filtered_lines)

        if removed_count > 0:
            with open(current_rat_path, 'w', newline="") as rat_list_file:
                rat_list_file.writelines(filtered_lines)
            print(f"Reverted {removed_count} entries at {current_rat_path}")
            rat_revert_count += 1
        else:
            print(f"No entries to revert at {current_rat_path}")

    return rat_revert_count



def RemoveSerialScript(drive_letter:str):
    current_extras_path = Path(drive_letter + ":" + constants.EXTRAS_PATH)
    if current_extras_path.is_dir():
        if (current_extras_path / constants.GRAB_SERIALS_SCRIPT_NAME).is_file():
            try:
                Path(current_extras_path, constants.GRAB_SERIALS_SCRIPT_NAME).unlink()
                print(f"Successfully removed Grab Serial script on drive {drive_letter}.")
                return 1
            except:
                print(f"There was an error removing the Grab Serials script on drive {drive_letter}.")
        else:
            print(f"There is no Grab Serials file to remove on drive {drive_letter}.")
    else:
        print(f"There was an issue finding the extras directory on drive {drive_letter}.")
    return 0
            
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

def RemoveUpdates(drive):
    operation_start = time.perf_counter()
    total_modifications = 0

    print(f"=== Attempting to Uninstall {drive[1]} on drive letter {drive[0]}: ...")

    total_modifications += RevertRats(drive[0])
    total_modifications += RemoveSerialScript(drive[0])

    print(f"Operations took {time.perf_counter() - operation_start:.3f} seconds")
    print(f"= Removed {total_modifications} total updates to {drive[1]}.")


def PerformUpdate(drive):
    operation_start = time.perf_counter()
    total_modifications = 0

    print(f"=== Attempting to Modify {drive[1]} on drive letter {drive[0]}: ...")

    total_modifications += ModifyRats(drive[0])
    total_modifications += AddSerialScript(drive[0])

    print(f"Operations took {time.perf_counter() - operation_start:.3f} seconds")
    print(f"= Made {total_modifications} total modifications to {drive[1]}!!!")


def PerformUpdateGUI():
    global global_drive_info, currently_updating
    if currently_updating:
            return -1
    currently_updating = True
    for each_drive in global_drive_info:
        if each_drive[0] in drive_enablement.keys():
            if drive_enablement[each_drive[0]].get():
                PerformUpdate(each_drive)
                SetLastModifiedDateOnDrive(each_drive[0], str(datetime.now(timezone(timedelta(hours=-7)))))
    currently_updating = False
    RefreshDriveList(drive_list_frame, detect_drives=True, run_function_again=False)

def RemoveUpdateGUI():
    global global_drive_info, currently_updating
    if currently_updating:
        return -1
    currently_updating = True
    for each_drive in global_drive_info:
        if each_drive[0] in drive_enablement.keys():
            if drive_enablement[each_drive[0]].get():
                RemoveUpdates(each_drive)
                DeleteZoolsDataFileOnDrive(each_drive[0])
    currently_updating = False
    RefreshDriveList(drive_list_frame, detect_drives=True, run_function_again=False)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#     GUI Tkinter Functions
# # # # # # # # # # # # # # # # # # # #            

def ProduceWindow():
    root.title("Zools GUI")
    root.geometry("1200x700")
    root.configure(bg="#d99b9b") 

    top_frame = tk.Frame(root, bg="#d99b9b")
    top_frame.pack(fill=tk.X)

    top_label = tk.Label(top_frame, text="ZOOLS", font=("Sitka Text", 30), bg="#d99b9b")
    top_label.pack(side=tk.TOP, pady=(15, 0))

    version_label = tk.Label(top_frame, text=f"Version {constants.CURRENT_VERSION}", font=("Sitka Text", 14), bg="#d99b9b")
    version_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=3)

    AddConfigurationOptions()

    EnsureLeftPaneFits()

    root.mainloop()

def AddConfigurationOptions():
    # Header stuff
    paned_window.pack(fill=tk.BOTH, expand=True)
    paned_window.add(left_pane)

    left_label = tk.Label(left_pane, text="Connected Drives", font=("Sitka Heading Semibold", 20, "bold", "underline"), bg="#ffc5c5")
    left_label.pack(pady=20, padx=10)

    # Drive Frame
    drive_list_frame.pack(fill=tk.BOTH, expand=True)

    global drive_enablement
    RefreshDriveList(drive_list_frame)

    # Bottom Frame (buttons)
    bottom_frame = tk.Frame(left_pane, bg="#d99b9b", height=100)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    bottom_frame.pack_propagate(False)

    refresh_button = tk.Button(bottom_frame, text="Refresh", command=lambda: RefreshDriveList(drive_list_frame, detect_drives=True, run_function_again=False), font=("Sitka Heading Semibold", 20))
    refresh_button.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

    remove_button = tk.Button(bottom_frame, text="Uninstall", command=RemoveUpdateGUI, font=("Sitka Heading Semibold", 20), bg="#FD6E6E")
    remove_button.grid(row=0, column=1, sticky="ew", padx=5, pady=10)

    update_button = tk.Button(bottom_frame, text="ZODIFY", command=PerformUpdateGUI, font=("Sitka Heading Semibold", 20), bg="#71EB61")
    update_button.grid(row=0, column=2, sticky="ew", padx=5, pady=10)

    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    # Main Text Section
    paned_window.add(right_pane)

    right_label = tk.Label(right_pane, text="Welcome to Zools!", font=("Sitka Heading Semibold", 20))
    right_label.pack(pady=20, padx=10)

    blog_nav_frame = tk.Frame(right_pane)
    blog_nav_frame.pack(side=tk.BOTTOM, pady=(0, 10))

    global current_blog_version
    previous_blog_button = tk.Button(blog_nav_frame, text="<-- Previous Version", command=lambda d=current_blog_version: SetBlog(GetPreviousBlog(d)), padx=10, pady=10, font=("Sitka Heading Semibold", 15), bg="#FFB0B0")
    previous_blog_button.pack(side=tk.LEFT, padx=5)

    current_blog_button = tk.Button(blog_nav_frame, text="Current Version", command=lambda: SetBlog(GetCurrentBlogContent()), padx=10, pady=10, font=("Sitka Heading Semibold", 15), bg="#FFB0B0")
    current_blog_button.pack(side=tk.LEFT, padx=5)

    next_blog_button = tk.Button(blog_nav_frame, text="Next Version -->", command=lambda d=current_blog_version: SetBlog(GetNextBlog(d)), padx=10, pady=10, font=("Sitka Heading Semibold", 15), bg="#FFB0B0")
    next_blog_button.pack(side=tk.LEFT, padx=5)


    text_frame.pack(fill="both", expand=True, padx=10, pady=(10, 10))

    scrollbar.pack(side="right", fill="y")
    text_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_box.yview)

    large_text = GetClosestBlog(constants.CURRENT_VERSION)
    text_box.insert("1.0", large_text)
    text_box.config(state="disabled")



def RefreshDriveList(drive_list_frame, detect_drives=False, run_function_again=True):
    global global_drive_info, drive_enablement, currently_updating

    if currently_updating:
        if run_function_again:
            root.after(2_000, lambda: RefreshDriveList(drive_list_frame, detect_drives=True))
        return

    if detect_drives:
        if constants.DBG_USE_DUMMY_DRIVES:
            global_drive_info = GenerateDummyDriveList()
        else:
            global_drive_info = GetToolDrives(GetConnectedDrives())

    current_drives = {drive[0] for drive in global_drive_info}

    for letter in list(drive_enablement.keys()):
        if letter not in current_drives:
            del drive_enablement[letter]

    for widget in drive_list_frame.winfo_children():
        widget.destroy()

    for i, each_drive in enumerate(global_drive_info):
        letter = each_drive[0]
        row = i * 3

        if letter not in drive_enablement:
            drive_enablement[letter] = tk.BooleanVar(master=root, value=True)

        lbl = tk.Label(drive_list_frame, text=f"{each_drive[1]} ({letter}:)", font=("Cascadia Code", 12, "bold"), bg="#ffc5c5")
        lbl.grid(row=row, column=0, pady=(5, 0), padx=10, columnspan=2)

        if constants.DBG_DISPLAY_TIMESTAMP_AS_NOW:
            last_date_updated = datetime.now(timezone(timedelta(hours=-7)))
            last_date_zodded = datetime.now(timezone(timedelta(hours=-7)))
        else:
            last_date_updated = GetLastDateUpdatedFromDrive(letter)
            last_date_zodded = GetLastDateZoddedFromDrive(letter)

        if last_date_zodded is None:
            last_date_zodded = "Not Modified"
        else:
            last_date_zodded = datetime.fromisoformat(last_date_zodded)
            first_part = last_date_zodded.strftime("%a, %b %#d")
            last_part = last_date_zodded.strftime(" %Y (%#I:%M %p)").lower()
            day = int(last_date_zodded.strftime("%#d"))
            last_date_zodded = f"{first_part}{GetOrdinalSuffix(day)}{last_part}"

        if last_date_updated is None:
            last_date_updated = "Not Updated"
        else:
            last_date_updated = datetime.strptime(last_date_updated, "%Y%m%d")
            date_part = last_date_updated.strftime("%a, %b %#d")
            day = int(last_date_updated.strftime("%#d"))
            last_date_updated = (f"{date_part}{GetOrdinalSuffix(day)}{last_date_updated.strftime(' %Y')}")

            updated_subtitle = tk.Label(drive_list_frame, text=f"Last Updated: {last_date_updated}", font=("Cascadia Code", 10), bg="#ffc5c5")
            updated_subtitle.grid(row=row + 1, column=0, padx=10, sticky="w")

            zodded_subtitle = tk.Label(drive_list_frame, text=f"Last Zodded: {last_date_zodded}", font=("Cascadia Code", 10), bg="#ffc5c5")
            zodded_subtitle.grid(row=row + 2, column=0, pady=(0, 20), padx=10, sticky="w")

            # checkbox = tk.Checkbutton(drive_list_frame, variable=drive_enablement[letter], anchor="center", command=lambda d=letter: CheckButtonModified(d))
            checkbox = CustomCheckbutton(drive_list_frame, variable=drive_enablement[letter], command=lambda d=letter: CheckButtonModified(d), size=24)
            checkbox.grid(row=row, column=1, rowspan=3)
            
    drive_list_frame.columnconfigure((0, 1), weight=1)
    EnsureLeftPaneFits()
    if run_function_again:
        root.after(5_000, lambda: RefreshDriveList(drive_list_frame, detect_drives=True))
        
def EnsureLeftPaneFits():
    root.update_idletasks()

    # A sash only exists when the PanedWindow has multiple panes
    if len(paned_window.panes()) < 2:
        return

    required_width = left_pane.winfo_reqwidth() + 10

    try:
        current_width = paned_window.sash_coord(0)[0]
    except tk.TclError:
        return

    if required_width > current_width:
        paned_window.sash_place(0, required_width, 0)

def EnforceLeftPaneMinimum(event=None):
    root.update_idletasks()

    if len(paned_window.panes()) < 2:
        return

    min_width = left_pane.winfo_reqwidth() + 10
    current_width = paned_window.sash_coord(0)[0]

    if current_width < min_width:
        paned_window.sash_place(0, min_width, 0)

def CheckButtonModified(id):
    global drive_enablement
    print(f"Drive {id} is now {drive_enablement[id].get()}")

def GetCurrentBlogContent():
    # what i want here, is that if the last blog content was, let's say, 0.1.0, and it's currently version 0.1.1, i want it to display 0.1.0's content if there is no content for 0.1.1. 
    # however, if there's more recent content, like 0.2.0, i don't want it to display that if the current version is 0.1.1. 
    # basically, display the version's blog content. If there's none, display the last blog content available. 
    return GetBlogContent(constants.CURRENT_VERSION)

def GetBlogContent(version):
    data = GetAllBlogData()
    if version in data:
        return data[version]
    return f"No blog post found for Version {version}."

def GetClosestBlog(version):
    data = GetAllBlogData()
    versions = list(data.keys())
    sorted_versions = sorted(versions, key=ComparableSemVer)
    for i in range(len(sorted_versions)-1, -1, -1):
        if ComparableSemVer(version) >= ComparableSemVer(sorted_versions[i]):
            return data[sorted_versions[i]]
    return f"Version '{version}' either doesn't have a previous version or there is a parsing error."

def GetClosestVersion(version):
    data = GetAllBlogData()
    versions = list(data.keys())
    sorted_versions = sorted(versions, key=ComparableSemVer)
    for i in range(len(sorted_versions)-1, -1, -1):
        if ComparableSemVer(version) >= ComparableSemVer(sorted_versions[i]):
            return sorted_versions[i]
    return f"Version '{version}' either doesn't have a previous version or there is a parsing error."

def GetNextBlog(version):
    data = GetAllBlogData()
    versions = list(data.keys())
    sorted_versions = sorted(versions, key=ComparableSemVer)

    if not version in versions:
        version = GetClosestVersion(version)
    if (sorted_versions.index(version) + 1) >= len(sorted_versions):
        # cant go any higher
        return data[version]
    else:
        return data[sorted_versions[sorted_versions.index(version) + 1]]

def GetPreviousBlog(version):
    data = GetAllBlogData()
    versions = list(data.keys())
    sorted_versions = sorted(versions, key=ComparableSemVer)
    if not version in versions:
        version = GetClosestVersion(version)
    if (sorted_versions.index(version) - 1) < 0:
        # cant go any lower
        return data[version]
    else:
        return data[sorted_versions[sorted_versions.index(version) - 1]]

def SetBlog(text_to_set):
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert("1.0", text_to_set)
    text_box.config(state="disabled") 

def GetAllBlogData():
    blog_file_path = os.getcwd() + "\\" + constants.BLOG_FILE_NAME
    with open(blog_file_path, 'r') as blog_raw:
        data = json.load(blog_raw)
    return data
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#     Date Reading/Writing Utilities  
# # # # # # # # # # # # # # # # # # # # 

def GetLastDateZoddedFromDrive(letter):
    zools_data_path = Path(letter + ":\\" + constants.DATE_MODIFIED_PATH + "\\" + constants.ZOOLS_DATA_FILE)
    data = {}
    if zools_data_path.is_file():
        with open(zools_data_path, 'r', encoding='utf-8') as file_raw:
            data = json.load(file_raw)
        if constants.ZKEY_LAST_DATE_UPDATED in data:
            return data[constants.ZKEY_LAST_DATE_UPDATED]
    return None

def GetLastDateUpdatedFromDrive(letter):
    timestamp_updated_path = Path(letter + ":\\" + constants.DATE_MODIFIED_PATH + "\\" + constants.DDRTOOLS_DATE_MODIFIED_TIMESTAMP_FILE)
    data = {}
    if timestamp_updated_path.is_file():
        with open(timestamp_updated_path, 'r', encoding='utf-8') as file_raw:
            data = file_raw.readline().strip()
        return data
    return None

def SetLastModifiedDateOnDrive(letter, time_to_set):
    zools_data_path = Path(letter + ":\\" + constants.DATE_MODIFIED_PATH + "\\" + constants.ZOOLS_DATA_FILE)
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
    #FILE_ATTRIBUTE_HIDDEN = 0x02
    #success = ctypes.windll.kernel32.SetFileAttributesW(str(pathToWriteTo), FILE_ATTRIBUTE_HIDDEN)

def DeleteZoolsDataFileOnDrive(letter):
    zools_data_path = Path(letter + ":\\" + constants.DATE_MODIFIED_PATH + "\\" + constants.ZOOLS_DATA_FILE)
    if zools_data_path.is_file():
        try:
            zools_data_path.unlink()
        except:
            print(f"There was an error removing the zools data file at {zools_data_path}.")
    else:
        print(f"There was an error locating the zools data file at {zools_data_path}.")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#        Misc/Debug Functions         
# # # # # # # # # # # # # # # # # # # # 

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

def SetGlobalDrives(drive):
    global global_drive_info
    global_drive_info = drive

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

def ComparableSemVer(sem_ver:str):
    return_list = []
    for each_num in sem_ver.split("."):
        return_list.append(int(each_num))
    return return_list 

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


        


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#    MAIN PROGRAM 
# # # # # # # # # # # # # # # # # # # # 

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