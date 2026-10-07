from pathlib import Path
import shutil, os, ctypes

drives = []

def GetConnectedDrives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()

    for i in  range(26):
        if bitmask & (1 << i):
            letter = chr(65 + i)
            drives.append(f"{letter}")

    drive_info = []

    for drive in drives:
        volume_name = ctypes.create_unicode_buffer(261)
        ctypes.windll.kernel32.GetVolumeInformationW(f"{drive}:\\", volume_name, 261, None, None, None, None, 0)

        drive_info.append((drive, volume_name.value))

    return drive_info
    
SOURCE_TOOL_PATH = r"\CopyingSources"
modify_rat_list = True
RAT_PATHS = [
    r"\DDRTools\PC\service\app\misc\rat_list.txt",
    r"\DDRTools\PC\eval\win-x64\rats.txt",
    r"\DDRTools\PC\eval\win-arm64\rats.txt"
]
NEW_RAT_LIST = [
    "*HopToDesk*\n"
]

add_serial_script = True
EXTRAS_PATH = r"\_extras"


def ModifyRats(drive_letter:str):
    if not modify_rat_list:
        print("Modify rat list is disabled.")
        return

    for each_rat_path in RAT_PATHS:
        current_rat_path = Path(drive_letter + ":" + each_rat_path)

        if current_rat_path.exists():
            # with open(current_rat_path, 'a') as rat_list_file:
            #     rat_list_file.writelines(NEW_RAT_LIST)
            #     print(f"Successfully updated RAT list at {current_rat_path}")
            with open(current_rat_path, 'r') as rat_list_file:
                existing_lines = set(rat_list_file.read().splitlines())

                new_lines = [
                    line for line in NEW_RAT_LIST
                    if line.rstrip("\n") not in existing_lines
                ]

                if new_lines:
                    with open(current_rat_path, 'a') as rat_list_file:
                        rat_list_file.writelines(new_lines)
                    print(f"Successfully updated RAT list at {current_rat_path}")
                else:
                    print(f"RAT list already contains the new entries at {current_rat_path}")
        else:
            print(f"There is no longer a RAT file at {current_rat_path}")
            
def AddSerialScript(drive_letter:str):
    if not add_serial_script:
        print("Adding serial script is disabled")

    current_extras_path = Path(drive_letter + ":" + EXTRAS_PATH)
    if current_extras_path.is_dir():
        source_file = os.getcwd() + "\\" + SOURCE_TOOL_PATH + "\\" + r"ZMOD_Grab-Serial.bat"
        shutil.copy2(source_file, current_extras_path)
        print(f"Successfully added Grab Serial script on drive {drive_letter}")
    else:
        print(f"There was a problem accessing the extras folder on drive {drive_letter}")
    


def main():
    drive_info = GetConnectedDrives()

    for drive in drive_info:
        if ("DDRx" in drive[1]):
            ModifyRats(drive[0])
            AddSerialScript(drive[0])


main()