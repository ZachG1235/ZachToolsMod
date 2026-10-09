from pathlib import Path
import shutil, os, ctypes, time
import constants

drives = []

def GetConnectedDrives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()

    for i in range(26):
        if bitmask & (1 << i):
            letter = chr(65 + i)
            drives.append(f"{letter}")

    drive_info = []

    for drive in drives:
        volume_name = ctypes.create_unicode_buffer(261)
        ctypes.windll.kernel32.GetVolumeInformationW(f"{drive}:\\", volume_name, 261, None, None, None, None, 0)

        drive_info.append((drive, volume_name.value))

    return drive_info



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
    


def main():
    start = time.perf_counter()

    drive_info = GetConnectedDrives()
    print(f"Drive detection took: {time.perf_counter() - start:.3f} seconds")

    modified_drive = False
    for drive in drive_info:
        if constants.DDRTOOLS_DRIVE_NAME_MULTI.upper() == drive[1].upper() or constants.DDRTOOLS_DRIVE_NAME_SINGLE.upper() == drive[1].upper():
            operation_start = time.perf_counter()

            total_modifications = 0
            modified_drive = True
            
            print(f"=== Attempting to Modify {drive[1]} on drive letter {drive[0]}: ...")
            
            total_modifications += ModifyRats(drive[0])
            total_modifications += AddSerialScript(drive[0])

            print(
                f"Operations took "
                f"{time.perf_counter() - operation_start:.3f} seconds"
            )
            print(f"= Made {total_modifications} total modifications to {drive[1]}!!!")

    if not modified_drive:
        print("There were no tool drives detected. Please insert new drives and run this program again.")


main()