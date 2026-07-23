import os
import time
from watchdog.events import FileSystemEventHandler

class OFXHandler(FileSystemEventHandler):
    def __init__(self, process_file):
        self.process_file = process_file

    def process_existing_files(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            if not os.path.isfile(file_path):
                continue

            self._process(file_path)

    def on_created(self, event):
        if event.is_directory:
            return

        self._process(event.src_path)

    def _process(self, file_path):
        filename = os.path.basename(file_path)

        if filename.startswith("."):
            return

        if not filename.lower().endswith(".ofx"):
            return

        time.sleep(1)

        self.process_file(file_path)