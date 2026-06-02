import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        #print(working_dir_abs)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if os.path.isdir(target_dir):
            print(f'Success: "{directory}" is within the working directory')
        else:
            raise Exception(f'Error: "{directory}" is not a directory')
    except Exception as e:
        return f'Error: "{e}"'

    content_rep = ""
    try:
        with os.scandir(path=target_dir) as entries:
            for entry in sorted(entries, key=lambda e: e.name):
                is_dir = True if entry.is_dir() else False
                size = entry.stat().st_size if entry.is_file() else "-"
                content_rep += f"{entry.name}: file_size={str(size)} bytes, is_dir={str(is_dir)} \n"
        return content_rep
    except Exception as e:
        return f"Error: {e}"

#def main():
#    absopath = os.path.abspath("")
#    get_files_info(absopath)

#ömain()
