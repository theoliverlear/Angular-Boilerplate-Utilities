import os
from tkinter import Tk, simpledialog, filedialog, font
from config import detect_source_directory
from injector import inject_stylesheet_to_angular_json, \
    inject_component_to_file, result_injection_directory

LAST_DIRECTORY_FILE = "last_directory.txt"
ELEMENT_ARRAY_FILE_PATH = os.path.join("angular", "components", "elements", "elements.ts")
PAGES_ARRAY_FILE_PATH = os.path.join("angular", "components", "pages", "pages.ts")

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
        file_name_partial = simpledialog.askstring("Input",
                                                   "Enter the file name partial:")
        if not file_name_partial:
            print("File name partial is required!")
            return
        initial_directory = get_last_directory() or os.getcwd()
        print(f"Using initial directory: {initial_directory}")
        target_directory = filedialog.askdirectory(
            title="Select Directory to Store New Component",
            initialdir=initial_directory)
        if not target_directory:
            print("No directory selected! Exiting.")
            return
        save_last_directory(target_directory)
        validated_directory = result_injection_directory(
            target_directory)
        print(f"Valid directory found: {validated_directory}")
        source_directory = detect_source_directory(
            os.path.abspath(validated_directory))
        if not source_directory:
            print(
                "Error: Could not detect source directory. Ensure this is"
                " a valid Angular project directory.")
            continue
        component_directory = os.path.join(target_directory,
                                           file_name_partial)
        os.makedirs(component_directory, exist_ok=True)
        print(f"Created directory: {component_directory}")
        typescript_component_name = f"{file_name_partial}.component.ts"
        html_component_name = f"{file_name_partial}.component.html"
        scss_component_name = f"{file_name_partial}.component.scss"
        css_component_name = f"{file_name_partial}.component.css"
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
        scss_content = f"""// {scss_component_name}
@import "../../../styles/global-variables";
@import "../../../styles/global-mixins";
@import "../../../styles/global-functions";
@import "../../../styles/global-placeholders";

{file_name_partial} {{
    
}}
"""
        create_file(
            os.path.join(component_directory, typescript_component_name),
            typescript_content)
        create_file(os.path.join(component_directory, html_component_name),
                    html_content)
        create_file(os.path.join(component_directory, scss_component_name),
                    scss_content)
        print("All files have been created successfully.")
        stylesheet_relative_path = os.path.relpath(
            os.path.join(component_directory, css_component_name),
            source_directory
        ).replace("\\", "/")
        inject_stylesheet_to_angular_json(source_directory,
                                          stylesheet_relative_path)
        typescript_file_without_ts = typescript_component_name.replace(".ts",
                                                                       "")
        if "elements" in target_directory.lower():
            inject_component_to_file(source_directory,
                                     ELEMENT_ARRAY_FILE_PATH,
                                     file_name_partial, pascal_case_name,
                                     typescript_file_without_ts, "elements",
                                     component_directory)
        elif "pages" in target_directory.lower():
            inject_component_to_file(source_directory, PAGES_ARRAY_FILE_PATH,
                                     file_name_partial, pascal_case_name,
                                     typescript_file_without_ts, "pages",
                                     component_directory)

if __name__ == "__main__":
    main()