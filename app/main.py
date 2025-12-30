import os
import time
import shutil
from parsers.parser import Parser

CONSUME_PATH = os.getenv("CONSUME_PATH", "/app/consume") # Get consume path from environment or default
LOOKUP_INTERVAL = int(os.getenv("LOOKUP_INTERVAL", "5")) # default 5 seconds

print(f"App started. Watching folder {CONSUME_PATH}")

parser = Parser()
processed_files = set() # Keep track of already seen files

def move_file(file_path, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    destination = os.path.join(target_dir, os.path.basename(file_name))
    shutil.move(file_path, destination)

while True:
    if os.path.exists(CONSUME_PATH):
        for file_name in os.listdir(CONSUME_PATH):
            file_path = os.path.join(CONSUME_PATH, file_name)

            # Skip directories
            if not os.path.isfile(file_path):
                continue

            if file_name in processed_files:
                # moved to processed folder CONSUME_PATH/processed but it should not be processed
                continue

            try:
                parsed_data = parser.parse(file_path)
                print(f"Parsed data from {file_name}")
                processed_files.add(file_name)

            except ValueError as e:
                print(e)
            
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

        print("Looking")

    time.sleep(LOOKUP_INTERVAL)
