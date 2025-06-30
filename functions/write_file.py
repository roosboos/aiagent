import os

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)

    if os.path.isabs(file_path):
        target_path = file_path
    else:
        target_path = os.path.join(working_directory, file_path)

    abs_file = os.path.abspath(target_path)

    if not abs_file.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        dir_name = os.path.dirname(abs_file)
        if os.path.exists(dir_name) == False and len(dir_name) > 0:
            os.makedirs(dir_name)
    except Exception as e:
        return f"Error: Something unexpected happened when trying to create file path: {e}"

    
    try:
        with open(abs_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Something unexpected happened when writing to file: {e}"


