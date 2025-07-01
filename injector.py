import os
import json

def result_injection_directory(starting_directory):
    current_directory = os.path.abspath(starting_directory)
    while True:
        if "elements" in os.listdir(current_directory) or "pages" in os.listdir(current_directory):
            return current_directory
        parent_directory = os.path.dirname(current_directory)
        if current_directory == parent_directory:
            raise FileNotFoundError("Neither 'elements' nor 'pages' directories were found in the project structure.")
        current_directory = parent_directory


def inject_stylesheet_to_angular_json(root_directory, stylesheet_path):
    angular_json_path = os.path.join(root_directory, 'angular.json')
    try:
        with open(angular_json_path, 'r') as file:
            angular_data = json.load(file)
        for project_name, project_config in angular_data.get('projects', {}).items():
            styles_path = project_config.get('architect', {}).get('build', {}).get('options', {}).get('styles', [])
            if isinstance(styles_path, list):
                relative_path = os.path.relpath(stylesheet_path, os.path.dirname(angular_json_path)).replace("\\", "/")
                print(f"Relative path for stylesheet: {relative_path}")
                if relative_path not in styles_path:
                    styles_path.append(relative_path)
                    styles_path.sort()
                    project_config['architect']['build']['options']['styles'] = styles_path
                    print(f"Injected and alphabetized stylesheet: {relative_path} into project: {project_name}")
                else:
                    print(f"Stylesheet already exists in project: {project_name}")

        with open(angular_json_path, 'w') as file:
            json.dump(angular_data, file, indent=2)
        print("Updated angular.json successfully.")
    except FileNotFoundError:
        print(f"angular.json not found in {root_directory}")
    except json.JSONDecodeError:
        print("Error parsing angular.json!")
    except Exception as exception:
        print(f"An error occurred: {exception}")

def inject_component_to_file(root_directory,
                             target_file,
                             component_name,
                             pascal_case_name,
                             typescript_file,
                             array_name,
                             component_directory):
    target_file_path = os.path.join(root_directory, target_file)
    try:
        if not os.path.exists(target_file_path):
            print(f"Error: {target_file} not found at {target_file_path}.")
            return
        with open(target_file_path, 'r') as file:
            lines = file.readlines()
        print(component_directory)
        relative_import_path = component_directory.split(array_name)[1].replace('\\', '/')
        print(f"Relative import path: {relative_import_path}")
        relative_import_path = f".{relative_import_path}/{typescript_file}"
        import_statement = f'import {{{pascal_case_name}Component}} from "{relative_import_path}";\n'
        if len(import_statement.strip()) > 78:
            import_statement = (
                f'import {{\n    {pascal_case_name}Component\n}} '
                f'from "{relative_import_path}";\n'
            )
        component_entry = f"{pascal_case_name}Component"
        last_import_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("import "):
                last_import_index = i
                if not line.strip().endswith(";"):
                    last_import_index += 2
        if last_import_index is None:
            raise ValueError("Could not locate import statements in the file.")
        if import_statement not in lines:
            lines.insert(last_import_index + 1, import_statement)
        array_start = next(
            (i for i, line in enumerate(lines) if line.strip().startswith(f"export const {array_name} = [")),
            None
        )
        if array_start is None:
            raise ValueError(f"Could not locate 'export const {array_name}' declaration in {target_file}.")
        array_end = None
        open_brackets = 0
        for i, line in enumerate(lines[array_start:], array_start):
            open_brackets += line.count("[")
            open_brackets -= line.count("]")
            if open_brackets == 0:
                array_end = i
                break
        if array_end is None:
            raise ValueError(f"Could not locate the closing bracket of the {array_name} array in {target_file}.")
        current_elements = [
            line.strip().strip(",") for line in lines[array_start + 1 : array_end] if line.strip()
        ]
        if component_entry not in current_elements:
            current_elements.append(component_entry)
            current_elements = sorted(set(current_elements))
        updated_elements = ",\n".join(f"    {e}" for e in current_elements)
        new_content = "".join(lines[:array_start + 1])
        new_content += f"{updated_elements},\n" + "".join(lines[array_end:])
        with open(target_file_path, 'w') as file:
            file.write(new_content)
        print(f"Injected {pascal_case_name}Component into {array_name} in {target_file} successfully.")
    except Exception as exception:
        print(f"An error occurred while updating {target_file}: {exception}")