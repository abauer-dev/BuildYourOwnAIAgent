import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Executes a python-file in a specified directory relative to the working directory, returns the output and/or errors from execution",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to python-file to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.OBJECT,
                description="provides additional arguments as Strings to execute function",
            ),
        },
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        #Workpath validation
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_path):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')
        if not target_path.endswith(".py"):
            raise Exception(f'Error: "{file_path}" is not a Python file')
                

        command = ["python", target_path]
        if args:
            command.extend(args)
        exe_obj = subprocess.run(command, cwd=working_directory,capture_output=True, text=True, timeout=30)
        exe_str = ""
        if exe_obj.returncode != 0:
            exe_str += f"Process exited with code {exe_obj.returncode}"
        if exe_obj.stdout is None and exe_obj.stderr is None:
            exe_str += "No output produced "
        if exe_obj.stdout:
            exe_str += f"STDOUT: {exe_obj.stdout} "
        if exe_obj.stderr:
            exe_str += f"STDERR: {exe_obj.stderr} "

        return exe_str

    except Exception as e:
        return f"Error: executing Python file: {e}"
