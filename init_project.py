import os
from tkinter import Tk, filedialog

DIRECTORY_STRUCTURE = {
    "angular": [
        "assets/images/favicon",
        "assets/images/icon",
        "assets/images/logo",
        "components/animations/models",
        "components/app",
        "components/elements",
        "components/events/models",
        "components/pages",
        "directives",
        "environments",
        "models",
        "modules/routing",
        "services/guard",
        "services/server",
        "services/websocket",
        "services/http",
        "server",
        "styles",
        "test"
    ]
}

def create_directory_structure(base_path, structure):
    for root, subdirs in structure.items():
        root_path = os.path.join(base_path, root)
        for subdir in subdirs:
            dir_path = os.path.join(root_path, subdir)
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created: {dir_path}")

def main():
    root = Tk()
    root.withdraw()
    target_directory = filedialog.askdirectory(title="Select Directory to Initialize Project")
    if not target_directory:
        print("No directory selected. Exiting.")
        return
    angular_directory = os.path.join(target_directory, "angular")
    if os.path.exists(angular_directory):
        print(f"The directory '{angular_directory}' already exists. Cannot initialize project structure.")
        return
    create_directory_structure(target_directory, DIRECTORY_STRUCTURE)
    print("Project structure initialized successfully.")

if __name__ == "__main__":
    main()
