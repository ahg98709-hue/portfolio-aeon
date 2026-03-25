
import os
import shutil
from typing import Optional

def list_files(path: str = ".") -> str:
    """Lists files in the given directory."""
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing files: {e}"

def read_file(path: str) -> str:
    """Reads content of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path: str, content: str) -> str:
    """Writes content to a file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File written to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def delete_file(path: str) -> str:
    """Deletes a file."""
    try:
        os.remove(path)
        return f"Deleted {path}"
    except Exception as e:
        return f"Error deleting file: {e}"
