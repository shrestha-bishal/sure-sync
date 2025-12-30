import os
import shutil
from helpers.logger import log

def move(file_path, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    destination = os.path.join(target_dir, os.path.basename(file_path))
    shutil.move(file_path, destination)
    log(f"Moved {os.path.basename(file_path)} to {target_dir}")
