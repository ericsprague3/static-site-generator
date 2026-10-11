import os
import shutil
import sys

from gencontent import generate_pages_recursive
    
dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def clear_public():
    # If the public directory doesn't exist yet, there is nothing to clear
    if not os.path.exists(dir_path_public):
        return

    for root, dirs, files in os.walk(dir_path_public, topdown=False):
        # Delete all files in the subfolders
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        
        # Delete the subfolders themselves
        for target_dir in dirs:
            dir_path = os.path.join(root, target_dir)
            os.rmdir(dir_path)

def copy_static_to_public():
    # Verify the source folder exists before trying to copy it
    if not os.path.exists(dir_path_static):
        raise FileNotFoundError(f"Source directory not found: {dir_path_static}")

    # Use copytree to copy entire directories.
    # dirs_exist_ok=True allows copying into the existing empty public folder.
    shutil.copytree(dir_path_static, dir_path_public, dirs_exist_ok=True)

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        
    try:
        clear_public()
        copy_static_to_public()
        print("Success: Static directory synced to public directory!")
        print("Generating pages...")
        # generate_page(
        #     os.path.join(dir_path_content, "index.md"),
        #     template_path,
        #     os.path.join(public_path, "index.html"),
        # )

        generate_pages_recursive(
            os.path.join(dir_path_content),
            template_path,
            dir_path_public,
            basepath,
        )
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()