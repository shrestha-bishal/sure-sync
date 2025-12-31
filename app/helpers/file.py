import os
import shutil
from helpers.logger import log

def move(src_path, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.move(src_path, dest_path)
    log(f"Moved {os.path.basename(src_path)} to {dest_path}")
