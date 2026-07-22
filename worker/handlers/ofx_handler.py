import os
import time
from watchdog.events import FileSystemEventHandler

class OFXHandler(FileSystemEventHandler):
    def __init__(self, process_file):
        self.process_file = process_file

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        if os.path.basename(file_path).startswith("."):
            return

        time.sleep(1)

        self.process_file(file_path)