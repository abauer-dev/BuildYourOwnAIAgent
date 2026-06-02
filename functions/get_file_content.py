import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads the content of a file in a specified directory relative to the working directory, returns the first {MAX_CHARS} chars in the file and if truncated it adds that it was truncated",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file to read, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        #print(working_dir_abs)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            raise Exception(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_path):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    
    except Exception as e:
        return f'Error: "{e}"'

    