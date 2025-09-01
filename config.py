import os

def detect_source_directory(selected_directory):
    current_directory = selected_directory
    while True:
        if "angular" in os.listdir(current_directory):
            return os.path.abspath(current_directory)
        parent_directory = os.path.dirname(current_directory)
        if current_directory == parent_directory:
            # Return the absolute path
            return os.path.abspath(current_directory)
        current_directory = parent_directory
        if "GitHub" in os.listdir(current_directory):
            return None
    return None

