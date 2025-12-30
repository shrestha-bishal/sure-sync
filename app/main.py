import os
import time

CONSUME_PATH = os.getenv("CONSUME_PATH", "/app/consume") # Get consume path from environment or default
LOOKUP_INTERVAL = int(os.getenv("LOOKUP_INTERVAL", "5")) # default 5 seconds

print(f"App started. Watching folder {CONSUME_PATH}")

# Keep track of already seen files
processed_files = set()

while True:
    print("Looking")
    time.sleep(LOOKUP_INTERVAL)
