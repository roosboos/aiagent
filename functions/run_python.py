import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)

    if os.path.isabs(file_path):
        target_path = file_path
    else:
        target_path = os.path.join(working_directory, file_path)
    
    abs_file = os.path.abspath(target_path)

    if not abs_file.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    try:
        if os.path.exists(abs_file) == False:
            return f'Error: File "{file_path}" not found.'
    except Exception as e:
        return f"Error: Could not find file path: {e}"
    
    try:
        if abs_file.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f"Error: File type is not a .py file: {e}"
    
    try:
       result = subprocess.run(
            ["python3", abs_file],
            cwd= abs_working, 
            timeout = 30, 
            capture_output = True,
            text = True
        )
       
       stdout = result.stdout.rstrip()
       stderr = result.stderr.rstrip()

       output = f"STDOUT: {stdout}\nSTDERR: {stderr}\n"

       if result.returncode != 0:
           output += f"Process exited with code {result.returncode}"
       if not stdout and not stderr:
           output = "No output produced."
       return output 
    
    except Exception as e:
        return f"Error: executing Python file: {e}"