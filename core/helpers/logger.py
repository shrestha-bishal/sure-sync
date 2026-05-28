from datetime import datetime

def log(msg):
    print(f"{datetime.now().isoformat(timespec='seconds')} | {msg}", flush=True)