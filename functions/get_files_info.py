import os

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