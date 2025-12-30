import os
import time
from helpers.logger import log
from helpers.file import move
from parsers.parser import Parser

CONSUME_PATH = "/app/consume"
PROCESSED_DIR = os.path.join(CONSUME_PATH, "processed")
FAILED_DIR = os.path.join(CONSUME_PATH, "failed")
VOLUME_CONSUME_PATH = os.getenv("CONSUME_PATH", CONSUME_PATH)
LOOKUP_INTERVAL = int(os.getenv("LOOKUP_INTERVAL", "5")) # default 5 seconds

os.makedirs(CONSUME_PATH, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)

log("App started")
log(f"Consume directory   : {VOLUME_CONSUME_PATH}")
log(f"Processed directory : {VOLUME_CONSUME_PATH}/processed")
log(f"Failed directory    : {VOLUME_CONSUME_PATH}/failed")
log(f"Scan interval       : {LOOKUP_INTERVAL}s")

parser = Parser()

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
            log(f"{parsed_data}")
            log(f"Parsed data from {file_name}")
            move(file_path, PROCESSED_DIR)

        except ValueError as e:
            log(f"Unsupported file {file_name}: {e}")
            move(file_path, FAILED_DIR)
        
        except Exception as e:
            log(f"Error processing {file_name}: {e}")
            move(file_path, FAILED_DIR)

    time.sleep(LOOKUP_INTERVAL)
