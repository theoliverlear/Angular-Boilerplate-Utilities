import os

from models.directory_selector import DirectorySelector

def get_directory() -> str:
    return DirectorySelector.select_directory()

def is_scss_file(file_path: str) -> bool:
    return file_path.endswith('.scss')

def get_all_sub_directories(directory: str) -> list[str]:
    sub_directories = []
    for root, dirs, files in os.walk(directory):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        for dir_name in dirs:
            sub_directories.append(os.path.join(root, dir_name))
    print(f"Found {len(sub_directories)} subdirectories in {directory}.")
    return sub_directories

def get_number_nested_by_import(file_path: str) -> int:
    with open(file_path, 'r') as file:
        content = file.read()
    import_lines = [line for line in content.splitlines() if line.strip().startswith('@import')]
    number_of_relative_jumps = import_lines[0].count('../') if import_lines else 0
    return number_of_relative_jumps

def get_use_replacement(number_of_nests: int) -> str:
    if number_of_nests == 0:
        return ''
    return f"@use \"{'../' * number_of_nests}styles/globals\" as *;\n"

def delete_all_imports_with_global(file_path: str) -> None:
    with open(file_path, 'r') as file:
        content = file.readlines()
    new_content = []
    for line in content:
        if line.strip().startswith('@import') and 'global' in line:
            continue
        new_content.append(line)
    with open(file_path, 'w') as file:
        file.writelines(new_content)

def insert_new_use(file_path: str, use_replacement: str) -> None:
    # Inserts on line 2
    with open(file_path, 'r') as file:
        content = file.readlines()

    if len(content) < 2:
        content.insert(1, use_replacement)
    else:
        content.insert(1, use_replacement + '\n')

    with open(file_path, 'w') as file:
        file.writelines(content)

def replace_imports_with_use(initial_directory: str) -> None:
    sub_directories = get_all_sub_directories(initial_directory)
    for directory in sub_directories:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if is_scss_file(file_path):
                number_of_nests = get_number_nested_by_import(file_path)
                use_replacement = get_use_replacement(number_of_nests)
                delete_all_imports_with_global(file_path)
                insert_new_use(file_path, use_replacement)
                print(f"Updated {file_path} with @use statement.")
            else:
                print(f"Skipped non-SCSS file: {file_path}")

def migrate_scss_imports():
    initial_directory = get_directory()
    print(f"Starting migration in directory: {initial_directory}")
    replace_imports_with_use(initial_directory)
    print("Migration completed successfully.")

def main():
    try:
        migrate_scss_imports()
    except Exception as e:
        print(f"An error occurred during migration: {e}")

if __name__ == "__main__":
    main()