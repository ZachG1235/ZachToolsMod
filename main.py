from pathlib import Path
import shutil, os, ctypes, time
import constants
import tkinter as tk

root = tk.Tk()

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

def ProduceWindow(drive_info):
    root.title("Zools GUI")
    root.geometry("600x600")

    top_label = tk.Label(root, text="ZOOLS", font=("Arial", 18))
    top_label.pack(pady=15)

    AddConfigurationOptions(drive_info)

    root.mainloop()

def AddConfigurationOptions(drive_info):
    print(drive_info)
    paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    left_pane = tk.Frame(paned_window, width=200, relief=tk.SUNKEN)
    paned_window.add(left_pane)

    left_label = tk.Label(left_pane, text="Left Sidebar / Menu", font=("Arial", 12))
    left_label.pack(pady=20, padx=10)

    for each_drive in drive_info:
        lbl = tk.Label(left_pane, text=f"{each_drive[1]} ({each_drive[0]}:)", font=("Arial", 12))
        lbl.pack(pady=(5, 0), padx=10)

        lbl_subtitle = tk.Label(left_pane, text="Subtitle", font=("Arial", 10))
        lbl_subtitle.pack(pady=(0, 20), padx=10)


    right_pane = tk.Frame(paned_window, width=400, relief=tk.SUNKEN)
    paned_window.add(right_pane)

    right_label = tk.Label(right_pane, text="Main Content Window", font=("Arial", 14))
    right_label.pack(pady=20, padx=10)


def main():
    start = time.perf_counter()

    drive_info = GetConnectedDrives()
    print(f"Drive detection took: {time.perf_counter() - start:.3f} seconds")
    # filter by only tools
    tool_drives = GetToolDrives(drive_info)

    if constants.DO_GUI:
        ProduceWindow(tool_drives)
        return
    
    for drive in tool_drives:
        PerformUpdate(drive)

    if len(tool_drives) < 1:
        print("There were no tool drives detected. Please insert new drives and run this program again.")


main()