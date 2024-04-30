import os
import shutil


def main_menu():
    print("started")
    while True:
        print("\nChoose an Option below to conintue:")
        print("1. Organise Desktop")
        print("2. Organise Documents")
        print("3. Organise Downloads")
        print("4. Delete Empty Folders")
        print("5. Exit")

        choice = input("Enter Choice (1-4): ")
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
        "PowerPoint_Folder":[".ppt", ".pptx"],
        "Excel_Files":[".xls", ".xlsx"]
    }

    other_folder = os.path.join(desktop_path, 'Pre_Folders')
    if not os.path.exists(other_folder):
        os.makedirs(other_folder)

    for folder in organiser:
        folder_path = os.path.join(desktop_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    #def log_movement(original_path, new_path):
    #  with open(log_file_path, 'a') as log_file:  # Open the log file in append mode
    #       log_file.write(f"{original_path} -> {new_path}\n")

    for item in os.listdir(desktop_path):
        full_path = os.path.join(desktop_path, item)
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(item)
            ext = ext.lower()
            moved = False
            for folder, extensions in organiser.items():
                if ext in extensions:
                    shutil.move(full_path, os.path.join(desktop_path, folder))
                    moved = True
                    break

        elif os.path.isdir(full_path) and not any(full_path == os.path.join(desktop_path, f) for f in organiser):
            if full_path != other_folder:  # Prevent moving the 'Pre_Folders' itself
                shutil.move(full_path, other_folder)

    print("Files have been organized by type on your desktop.")
if __name__ == "__main__":
    main_menu()