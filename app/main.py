import os
import time
import shutil
from datetime import datetime
from parsers.parser import Parser

CONSUME_PATH = "/app/consume"
PROCESSED_DIR = os.path.join(CONSUME_PATH, "processed")
FAILED_DIR = os.path.join(CONSUME_PATH, "failed")
VOLUME_CONSUME_PATH = os.getenv("CONSUME_PATH", CONSUME_PATH)
LOOKUP_INTERVAL = int(os.getenv("LOOKUP_INTERVAL", "5")) # default 5 seconds

os.makedirs(CONSUME_PATH, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)

def log(msg):
    print(f"{datetime.now().isoformat(timespec='seconds')} | {msg}", flush=True)

log("App started")
log(f"Consume directory   : {VOLUME_CONSUME_PATH}")
log(f"Processed directory : {VOLUME_CONSUME_PATH}/processed")
log(f"Failed directory    : {VOLUME_CONSUME_PATH}/failed")
log(f"Scan interval       : {LOOKUP_INTERVAL}s")

parser = Parser()

def move_file(file_path, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    destination = os.path.join(target_dir, os.path.basename(file_path))
    shutil.move(file_path, destination)
    log(f"Moved {os.path.basename(file_path)} to {target_dir}")

while True:
    if not os.path.exists(CONSUME_PATH):
        log(f"Consume path does not exist: {CONSUME_PATH}")
        time.sleep(LOOKUP_INTERVAL)
        continue

    for file_name in os.listdir(CONSUME_PATH):
        file_path = os.path.join(CONSUME_PATH, file_name)

        # Skip directories (processed/, failed/)
        if not os.path.isfile(file_path):
            continue

        try:
            parsed_data = parser.parse(file_path)
            log(f"Parsed data from {file_name}")
            move_file(file_path, PROCESSED_DIR)

        except ValueError as e:
            log(f"Unsupported file {file_name}: {e}")
            move_file(file_path, FAILED_DIR)
        
        except Exception as e:
            log(f"Error processing {file_name}: {e}")
            move_file(file_path, FAILED_DIR)

    log("Consuming")
    time.sleep(LOOKUP_INTERVAL)
