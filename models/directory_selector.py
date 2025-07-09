import os
from tkinter import Tk, filedialog

from component_generator import get_last_directory

LAST_DIRECTORY_FILE: str = "last_directory.txt"

class DirectorySelector:

    @staticmethod
    def get_last_directory():
        parent_dir = os.path.dirname(os.getcwd())
        parent_file_path = os.path.join(parent_dir, LAST_DIRECTORY_FILE)
        if os.path.exists(parent_file_path):
            with open(parent_file_path, 'r') as file:
                directory = file.read().strip()
                if os.path.isdir(directory):
                    return directory

        return os.getcwd()

    @staticmethod
    def save_last_directory(directory: str):
        parent_dir = os.path.dirname(os.getcwd())
        parent_file_path = os.path.join(parent_dir, LAST_DIRECTORY_FILE)
        with open(parent_file_path, 'w') as file:
            file.write(directory)
        print(f"Last directory saved: {directory}")

    @staticmethod
    def select_directory() -> str:
        target_directory: str = filedialog.askdirectory(
            title="Select Directory to Store New Component",
            initialdir=get_last_directory())
        if not target_directory:
            print("No directory selected! Exiting.")
            raise ValueError("No directory selected!")
        DirectorySelector.save_last_directory(target_directory)
        return target_directory