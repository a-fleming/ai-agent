import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory.",
            ),
        },
        required=["directory"],
    ),
)
available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)

def get_files_info(working_directory, directory):
    try:
        if directory == "":
            directory = "."
        
        if not isinstance(directory, (str, os.PathLike)):
            return (
                "Error: 'directory' must be a string or os.PathLike "
                f"object, not {type(directory).__name__!r}."
            )
        
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(abs_working_dir, directory))
        
        if not target_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        
        files_info = []
        for filename in os.listdir(target_path):
            if filename.startswith("."):
                # print("skipping hidden file or directory")
                # continue
                pass
            path_to_name = os.path.join(target_path, filename)
            file_size = os.path.getsize(path_to_name)
            is_dir = os.path.isdir(path_to_name)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

if __name__ == "__main__":
    working_directory = os.getcwd()
    directory = input("Enter directory to list (default is current directory): ") or "."
    print(get_files_info(working_directory, directory))