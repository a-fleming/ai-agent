import os
import argparse

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(target_path, 'w') as file:
            file.write(content + "\n")
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("file", type=str, help="File path to write to")
    parser.add_argument("content", type=str, help="Content to write to the file")
    args = parser.parse_args()

    working_directory = os.getcwd()
    file_path = args.file
    content = args.content
    print(write_file(working_directory, file_path, content))