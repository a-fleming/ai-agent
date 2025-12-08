import argparse
import os

from config import MAX_FILE_READ_CHARACTERS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

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
    parser = argparse.ArgumentParser(description="Read content of a file within the working directory")
    parser.add_argument("file_path", type=str, help="Path of the file to read")
    args = parser.parse_args()
    print(get_file_content(working_directory, args.file_path))