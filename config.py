import os

def detect_source_directory(selected_directory):
    absolute_path = os.path.abspath(selected_directory)
    path_parts = absolute_path.split(os.sep)
    if "GitHub" in path_parts:
        github_index = path_parts.index("GitHub")
        if github_index + 1 < len(path_parts):
            source_directory = os.sep.join(path_parts[:github_index + 2])
            print(f"Detected source directory: {source_directory}")
            return source_directory
    print("Error: Could not detect source directory. Ensure the selected path"
          " includes a 'GitHub' folder.")
    return None

