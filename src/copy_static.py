import os
import shutil

def copy_static(source_dir: str, target_path: str) -> None:
    print(f"Does {target_path} exist?: {os.path.exists(target_path)}")
    if os.path.exists(target_path):

        print(f"Removing {target_path}") 
        shutil.rmtree(target_path)

    print(f"Making a new directory: {target_path}")
    os.mkdir(target_path)

    print(f"Calling copy_static_helper function with source: {source_dir} and target: {target_path}")
    copy_static_helper(source_dir, target_path)
    
  



def copy_static_helper(file_path: str, target_path: str):
    print(f"Checking items in: {file_path}")
    for item_name in os.listdir(file_path):
        print(f"Checking item: {item_name}")
        full_path = os.path.join(file_path, item_name)
        print(f"Full path: {full_path}")
        print(f"Checking if {full_path} is a file: {os.path.isfile(full_path)}")
        if os.path.isfile(full_path):
            print(f"Copying {full_path} to directory:{target_path}")
            shutil.copy(full_path, target_path)
        print(f"Checking if {full_path} is a directory: {os.path.isdir(full_path)}")
        if os.path.isdir(full_path):
            new_target_path = os.path.join(target_path, item_name)
            print(f"New target path: {new_target_path}")
            os.mkdir(new_target_path)
            print(f"Making new directory: {new_target_path}")
            print(f"Recursively calling copy_static_helper with source: {full_path} and target: {new_target_path}")
            copy_static_helper(full_path, new_target_path)
