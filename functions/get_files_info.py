import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
        
    abs_working = os.path.abspath(working_directory)
    
    # Key fix: if directory is relative, make it relative to working_directory
    if os.path.isabs(directory):
        target_path = directory
    else:
        target_path = os.path.join(working_directory, directory)
    
    abs_dir = os.path.abspath(target_path)

    if not abs_dir.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isdir(abs_dir) == False:
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(abs_dir)

        formatted_items = []

        for content in contents:
            combined = os.path.join(abs_dir, content)
            if os.path.isdir(combined) == True:
                dir_file_size = os.path.getsize(combined)
                formatted_items.append(f"- {content}: file_size={dir_file_size} bytes, is_dir=True")
            else:
                file_file_size = os.path.getsize(combined)
                formatted_items.append(f"- {content}: file_size={file_file_size} bytes, is_dir=False")
    
        return "\n".join(formatted_items)
    except Exception as e:
        return f"Error: Something unexpected occured: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
             type=types.Type.STRING,
             description="The file path to the file you are getting the content of, relative to the working directory."
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description= "Allows the LLM to run code within the working directory, with a 30 second time limit to prevent it running indefinitely.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory."
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description= "Allows the LLM to write and overwrite files within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content to write to the file."
            ),
        },
    ),
)