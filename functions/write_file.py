import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        #Workpath validation
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_path):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
        os.makedirs(os.path.dirname(target_path),exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return e