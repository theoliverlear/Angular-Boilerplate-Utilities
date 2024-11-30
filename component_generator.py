import os
from tkinter import Tk, simpledialog, filedialog, font
from config import detect_source_directory
from injector import inject_stylesheet_to_angular_json, inject_component_to_file

LAST_DIRECTORY_FILE = "last_directory.txt"
ELEMENT_ARRAY_FILE_PATH = "angular/components/elements/elements.ts"
PAGES_ARRAY_FILE_PATH = "angular/components/pages/pages.ts"

def get_last_directory():
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, 'r') as file:
            directory = file.read().strip()
            if os.path.isdir(directory):
                return directory
    return None

def save_last_directory(directory):
    with open(LAST_DIRECTORY_FILE, 'w') as file:
        file.write(directory)
    print(f"Last directory saved: {directory}")

def create_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Created file: {file_path}")

def to_pascal_case(snake_string):
    return ''.join(word.capitalize() for word in snake_string.replace('-', '_').split('_'))

def main():
    while True:
        root = Tk()
        root.withdraw()
        root.option_add("*Font", "Arial 14")
        root.geometry("800x600")
        file_name_partial = simpledialog.askstring("Input",
                                                   "Enter the file name partial:")
        if not file_name_partial:
            print("File name partial is required!")
            return
        initial_directory = get_last_directory() or os.getcwd()
        print(f"Using initial directory: {initial_directory}")
        target_directory = filedialog.askdirectory(title="Select Directory to Store New Component",
                                                   initialdir=initial_directory)
        if not target_directory:
            print("No directory selected! Exiting.")
            return
        save_last_directory(target_directory)
        source_directory = detect_source_directory(target_directory)
        if not source_directory:
            print("Error: Could not detect source directory. Ensure the"
                  " selected path is within a valid GitHub project.")
            continue
        new_directory_path = os.path.join(target_directory, file_name_partial)
        os.makedirs(new_directory_path, exist_ok=True)
        print(f"Created directory: {new_directory_path}")
        typescript_component_name = f"{file_name_partial}.component.ts"
        html_component_name = f"{file_name_partial}.component.html"
        scss_component_name = f"{file_name_partial}-style.component.scss"
        css_component_name = f"{file_name_partial}-style.component.css"
        html_content = f"<!-- {html_component_name} -->"
        pascal_case_name = to_pascal_case(file_name_partial)
        typescript_content = f"""// {typescript_component_name} 
import {{ Component }} from "@angular/core";

@Component({{
    selector: '{file_name_partial}',
    templateUrl: './{html_component_name}',
    styleUrls: ['./{css_component_name}']
}})
export class {pascal_case_name}Component {{
    constructor() {{
        
    }}
}}
"""
        scss_content = f""" // {scss_component_name}
@import "../../../styles/global-variables";
@import "../../../styles/global-mixins";
@import "../../../styles/global-functions";
@import "../../../styles/global-placeholders";

{file_name_partial} {{

}}
"""
        typescript_file_path = os.path.join(new_directory_path, typescript_component_name)
        html_file_path = os.path.join(new_directory_path, html_component_name)
        scss_file_path = os.path.join(new_directory_path, scss_component_name)
        create_file(typescript_file_path, typescript_content)
        create_file(html_file_path, html_content)
        create_file(scss_file_path, scss_content)
        print("All files have been created successfully.")
        stylesheet_relative_path = os.path.relpath(os.path.join(new_directory_path, css_component_name), source_directory).replace("\\", "/")
        inject_stylesheet_to_angular_json(source_directory, stylesheet_relative_path)
        typescript_file_without_ts = typescript_component_name.replace(".ts", "")
        if "elements" in target_directory:
            inject_component_to_file(source_directory, ELEMENT_ARRAY_FILE_PATH, file_name_partial, pascal_case_name,
                                     typescript_file_without_ts, "elements")
        elif "pages" in target_directory:
            inject_component_to_file(source_directory, PAGES_ARRAY_FILE_PATH, file_name_partial, pascal_case_name,
                                     typescript_file_without_ts, "pages")

if __name__ == "__main__":
    main()