import os
import shutil
import sys

from gencontent import generate_page, generate_pages_recursive

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    
public_path = os.path.join(PROJECT_ROOT, "public")
static_path = os.path.join(PROJECT_ROOT, "static")

dir_path_content = "./content"
template_path = "./template.html"

def clear_public():
    # If the public directory doesn't exist yet, there is nothing to clear
    if not os.path.exists(public_path):
        return

    for root, dirs, files in os.walk(public_path, topdown=False):
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
    if not os.path.exists(static_path):
        raise FileNotFoundError(f"Source directory not found: {static_path}")

    # Use copytree to copy entire directories.
    # dirs_exist_ok=True allows copying into the existing empty public folder.
    shutil.copytree(static_path, public_path, dirs_exist_ok=True)

def main():
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
            os.path.join(public_path),
        )
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()