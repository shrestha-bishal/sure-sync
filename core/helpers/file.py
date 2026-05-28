import os
import shutil
import json
from core.helpers.logger import log

def move(src_path, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.move(src_path, dest_path)
    log(f"Moved {os.path.basename(src_path)} to {dest_path}")

def write_json(file_path: str, data: dict):
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log(f"Error writing JSON to {file_path}: {e}")
        raise e

def read_json(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Error reading JSON from {file_path}: {e}")
        return {}
