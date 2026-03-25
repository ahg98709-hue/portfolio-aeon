
import os
import shutil
import glob
import time
import hashlib
import json
import zipfile
import tarfile
import pathlib
from typing import List, Optional, Dict, Union
from datetime import datetime

# --- Reading and Writing ---

def read_file(path: str) -> str:
    """Reads the content of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"

def write_file(path: str, content: str, append: bool = False) -> str:
    """Writes or appends content to a file."""
    try:
        mode = 'a' if append else 'w'
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to {path}: {e}"

def read_lines(path: str) -> List[str]:
    """Reads a file and returns a list of lines."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        return []

def write_lines(path: str, lines: List[str]) -> str:
    """Writes a list of lines to a file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return f"Successfully wrote lines to {path}"
    except Exception as e:
        return f"Error: {e}"

def read_json(path: str) -> Union[Dict, List, str]:
    """Reads a JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return f"Error reading JSON: {e}"

def write_json(path: str, data: Union[Dict, List]) -> str:
    """Writes data to a JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return f"Successfully wrote JSON to {path}"
    except Exception as e:
        return f"Error: {e}"

def read_binary(path: str) -> bytes:
    """Reads a file in binary mode."""
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception:
        return b""

def write_binary(path: str, data: bytes) -> str:
    """Writes binary data to a file."""
    try:
        with open(path, 'wb') as f:
            f.write(data)
        return "Success"
    except Exception as e:
        return str(e)

# --- File Management ---

def create_file(path: str) -> str:
    """Creates an empty file if it doesn't exist."""
    try:
        pathlib.Path(path).touch()
        return f"Created {path}"
    except Exception as e:
        return str(e)

def delete_file(path: str) -> str:
    """Deletes a file."""
    try:
        os.remove(path)
        return f"Deleted {path}"
    except Exception as e:
        return str(e)

def rename_file(old_path: str, new_path: str) -> str:
    """Renames a file."""
    try:
        os.rename(old_path, new_path)
        return f"Renamed {old_path} to {new_path}"
    except Exception as e:
        return str(e)

def move_file(src: str, dst: str) -> str:
    """Moves a file."""
    try:
        shutil.move(src, dst)
        return f"Moved {src} to {dst}"
    except Exception as e:
        return str(e)

def copy_file(src: str, dst: str) -> str:
    """Copies a file."""
    try:
        shutil.copy2(src, dst)
        return f"Copied {src} to {dst}"
    except Exception as e:
        return str(e)

def get_file_size(path: str) -> int:
    """Returns file size in bytes."""
    try:
        return os.path.getsize(path)
    except:
        return -1

def get_file_creation_time(path: str) -> str:
    """Returns formatted creation time."""
    try:
        return time.ctime(os.path.getctime(path))
    except:
        return ""

def get_file_modification_time(path: str) -> str:
    """Returns formatted modification time."""
    try:
        return time.ctime(os.path.getmtime(path))
    except:
        return ""

def exists(path: str) -> bool:
    """Checks if file or directory exists."""
    return os.path.exists(path)

def is_file(path: str) -> bool:
    """Checks if path is a file."""
    return os.path.isfile(path)

def is_dir(path: str) -> bool:
    """Checks if path is a directory."""
    return os.path.isdir(path)

# --- Directory Management ---

def create_directory(path: str) -> str:
    """Creates a directory."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Created directory {path}"
    except Exception as e:
        return str(e)

def delete_directory(path: str) -> str:
    """Deletes a directory and its contents."""
    try:
        shutil.rmtree(path)
        return f"Deleted directory {path}"
    except Exception as e:
        return str(e)

def list_files(directory: str, extension: str = "*") -> List[str]:
    """Lists files in a directory matching an extension."""
    try:
        return glob.glob(os.path.join(directory, f"*.{extension}")) if extension != "*" else glob.glob(os.path.join(directory, "*"))
    except:
        return []

def list_all_files_recursive(directory: str) -> List[str]:
    """Lists all files in a directory recursively."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def get_current_directory() -> str:
    """Returns current working directory."""
    return os.getcwd()

# --- Advanced Operations ---

def get_file_hash(path: str, algo: str = "sha256") -> str:
    """Calculates file hash."""
    try:
        hash_func = getattr(hashlib, algo)()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return str(e)

def compare_files(path1: str, path2: str) -> bool:
    """Compares two files by hash."""
    return get_file_hash(path1) == get_file_hash(path2)

def search_text_in_files(directory: str, text: str, extension: str = "txt") -> List[str]:
    """Searches for text content inside files."""
    matches = []
    files = list_files(directory, extension)
    for file in files:
        if text in read_file(file):
            matches.append(file)
    return matches

def batch_rename(directory: str, prefix: str, extension: str) -> str:
    """Renames all files of extension with a prefix and counter."""
    try:
        files = list_files(directory, extension)
        for i, file in enumerate(files):
            new_name = os.path.join(directory, f"{prefix}_{i+1}.{extension}")
            os.rename(file, new_name)
        return f"Renamed {len(files)} files."
    except Exception as e:
        return str(e)

def zip_directory(directory: str, output_path: str) -> str:
    """Compresses a directory into a zip file."""
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(directory):
                for file in files:
                    zipf.write(os.path.join(root, file), 
                               os.path.relpath(os.path.join(root, file), 
                               os.path.join(directory, '..')))
        return f"Zipped {directory} to {output_path}"
    except Exception as e:
        return str(e)

def unzip_file(zip_path: str, extract_to: str) -> str:
    """Extracts a zip file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return f"Extracted {zip_path} to {extract_to}"
    except Exception as e:
        return str(e)

def count_lines(path: str) -> int:
    """Counts lines in a file."""
    lines = read_lines(path)
    return len(lines)

def clear_file(path: str) -> str:
    """Clears file content."""
    return write_file(path, "")

def touch_file(path: str) -> str:
    """Updates file timestamp or creates it."""
    try:
        pathlib.Path(path).touch()
        return f"Touched {path}"
    except Exception as e:
        return str(e)

def get_file_extension(path: str) -> str:
    """Returns file extension."""
    return os.path.splitext(path)[1]

def get_filename_without_extension(path: str) -> str:
    """Returns filename without extension."""
    return os.path.splitext(os.path.basename(path))[0]

def secure_delete(path: str, passes: int = 3) -> str:
    """Overwrites file with random data before deleting."""
    try:
        length = os.path.getsize(path)
        with open(path, "wb") as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        os.remove(path)
        return "Securely deleted."
    except Exception as e:
        return str(e)

def duplicate_file(path: str) -> str:
    """Creates a copy of the file with _copy suffix."""
    try:
        root, ext = os.path.splitext(path)
        new_path = f"{root}_copy{ext}"
        return copy_file(path, new_path)
    except Exception as e:
        return str(e)
