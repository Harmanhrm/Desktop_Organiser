import os
import shutil

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
organiser = {
    "Pictures_Folder": [".jpg", ".png", ".gif", ".jpeg"],
    "Pdf_Folder": [".pdf", ".html"],
    "Shortcuts": [".lnk", ".url", "Shortcut"],
    "Word_Folder": [".doc", ".docx"],
    "Zip_Files": [".rar", ".zip", ".7z"],
    "Text_Files": [".log", ".txt"],
    "Music_Folder": [".mp3", ".msv", ".wav", ".wma"],
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
