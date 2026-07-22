import os
import shutil
import json
from core.helpers.logger import log
from datetime import datetime

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

def archive_file(base_dir, bank_name, account_name, file_name, from_date, to_date):
    now = datetime.now()

    archive_dir = os.path.join(
        base_dir,
        bank_name or "unknown",
        account_name or "unknown",
        str(now.year),
        now.strftime("%B")
    )

    os.makedirs(archive_dir, exist_ok=True)

    date_range = (
        f"{from_date.strftime('%d%b%Y')}-"
        f"{to_date.strftime('%d%b%Y')}"
    )

    name, ext = os.path.splitext(file_name)
    new_file_name = f"Transactions {date_range}{ext}"

    return os.path.join(
        archive_dir,
        new_file_name
    )
