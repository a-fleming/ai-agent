import os
import subprocess

from functions.config import RUN_PYTHON_FILE_TIMEOUT_SECONDS

def run_python_file(working_directory, file_path, args=[]):
    print(f"args: {args}")
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File "{file_path}" not found.'
    try:
        result = subprocess.run(
            ['python3', target_path] + args,
            capture_output=True,
            text=True,
            cwd=abs_working_dir,
            timeout=RUN_PYTHON_FILE_TIMEOUT_SECONDS
        )
        output = ""
        if result.stdout:
            output += f"STDOUT: {result.stdout}\n"
        if result.stderr:
            output += f"STDERR: {result.stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}.\n"
        return output if output else "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"