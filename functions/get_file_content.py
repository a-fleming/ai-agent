import os

from functions.config import MAX_FILE_READ_CHARACTERS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_path, 'r') as file:
            content = file.read()
            if len(content) > MAX_FILE_READ_CHARACTERS:
                content = content[:MAX_FILE_READ_CHARACTERS] + f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARACTERS} characters]'
            return content
    except Exception as e:
        return f"Error reading file: {e}"

if __name__ == "__main__":
    working_directory = os.getcwd()
    file_path = input("Enter file path to read: ")
    print(get_file_content(working_directory, file_path))