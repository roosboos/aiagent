import os

def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)

    if os.path.isabs(file_path):
        target_path = file_path
    else:
        target_path = os.path.join(working_directory, file_path)
    
    abs_file = os.path.abspath(target_path)

    if not abs_file.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(abs_file) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    try:
        with open(abs_file, "r") as f:
            content = f.read(MAX_CHARS)
            extra = f.read(1)
            if extra:
                content = content + f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f"Error: Something unexpected occurred: {e}"