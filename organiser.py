import os
import shutil
import logging
import re
logging.basicConfig(filename='file_operations.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

   
def main_menu():
    print("started")
    while True:
        print("\nChoose an Option below to conintue:")
        print("1. Organise Desktop")
        print("2. Organise Documents")
        print("3. Organise Downloads")
        print("4. Delete Empty Folders")
        print("5. Exit")

        choice = input("Enter Choice (1-5): ")
        match choice:
            case '1':
                organise_files(os.path.join(os.path.expanduser('~'), 'Desktop'))
            case '2':
                organise_files(os.path.join(os.path.expanduser('~'), 'Downloads'))
            case '3':
                organise_files(os.path.join(os.path.expanduser('~'), 'Documents'))
            case '4':
                directory = input("Enter directory path to delete empty folders: ")
                delete_empty_folders(directory)
            case '5':
                print("Exiting program.")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 5.")

def delete_empty_folders(directory):
    # Walking through the directory tree, starting from the bottom
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        # Check if the directory is empty
        if not dirnames and not filenames:
            # Attempt to remove the empty directory
            try:
                os.rmdir(dirpath)
                print(f"Deleted empty folder: {dirpath}")
            except OSError as e:
                print(f"Error: {e} - {dirpath}")

def organise_files(desktop_path):
    organiser = {
        "Pictures_Folder": [".jpg", ".png", ".gif", ".jpeg"],
        "Pdf_Folder": [".pdf", ".html"],
        "Shortcuts": [".lnk", ".url", "Shortcut"],
        "Word_Folder": [".doc", ".docx"],
        "Zip_Files": [".rar", ".zip", ".7z"],
        "Text_Files": [".log", ".txt", ".oxps"],
        "Music_Folder": [".mp3", ".msv", ".wav", ".wma"],
        "Video_Folder": [".mp4"],
        "PowerPoint_Folder": [".ppt", ".pptx"],
        "Excel_Files": [".xls", ".xlsx"]
    }
    other_folder = os.path.join(desktop_path, 'Other_Folders')
    os.makedirs(other_folder, exist_ok=True)

    for folder in organiser:
        folder_path = os.path.join(desktop_path, folder)
        os.makedirs(folder_path, exist_ok=True)

    print(f"Checking items in {desktop_path}")
    for item in os.listdir(desktop_path):
        full_path = os.path.join(desktop_path, item)
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(item)
            ext = ext.lower()
            moved = False
            
            for folder, extensions in organiser.items():
                if ext in extensions:
                    new_path = os.path.join(desktop_path, folder, item)
                    if os.path.exists(new_path):  # Check if the file already exists
                        new_name = f"{os.path.splitext(item)[0]}_copy{ext}"
                        new_path = os.path.join(desktop_path, folder, new_name)
                        print(f"Renaming {item} to {new_name} to avoid overwrite")
                    
                    shutil.move(full_path, new_path)
                    logging.info(f"Moved {full_path} to {new_path}")
                    print(f"Moved {item} to {new_path}")
                    moved = True
                    break

            if not moved:
                print(f"No match for {item} with extension {ext}")

        elif os.path.isdir(full_path) and full_path not in [os.path.join(desktop_path, f) for f in organiser.keys()] and full_path != other_folder:
            shutil.move(full_path, other_folder)
            logging.info(f"Moved folder {full_path} to {other_folder}")
            print(f"Moved folder {item} to {other_folder}")

    print("Files have been organized by type on your desktop.")



def undo_last_changes(logfile='file_operations.log'):
    with open(logfile, 'r') as file:
        lines = file.readlines()

    move_regex = re.compile(r'Moved (.*?) to (.*?)$')

    for line in reversed(lines):
        if 'Moved' in line:
            match = move_regex.search(line)
            if match:
                src, dest = match.groups()
                print(f"Attempting to reverse move from '{dest}' to '{src}'")
                if os.path.exists(dest):
                    try:
                        shutil.move(dest, src)
                        logging.info(f"Reversed move from '{dest}' to '{src}'")
                        print(f"Reversed move from '{dest}' to '{src}'")
                    except Exception as e:
                        logging.error(f"Failed to reverse move from '{dest}' to '{src}': {e}")
                        print(f"Failed to reverse move from '{dest}' to '{src}': {e}")
                else:
                    logging.error(f"File not found: {dest}")
                    print(f"File not found: {dest}")
        elif 'Deleted' in line:
            path_match = re.search(r'Deleted empty folder: (.*)', line)
            if path_match:
                path = path_match.group(1)
                if not os.path.exists(path):
                    try:
                        os.makedirs(path)
                        logging.info(f"Restored deleted folder: {path}")
                        print(f"Restored deleted folder: {path}")
                    except Exception as e:
                        logging.error(f"Failed to restore deleted folder {path}: {e}")
                        print(f"Failed to restore deleted folder {path}: {e}")

if __name__ == "__main__":
    main_menu()
    if input("Undo changes? (y/n): ").lower() == 'y':
        undo_last_changes()