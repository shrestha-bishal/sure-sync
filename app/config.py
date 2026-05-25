import os

consume_path = "/app/consume"
processed_dir = os.path.join(consume_path, "processed")
failed_dir = os.path.join(consume_path, "failed")
volume_consume_path = os.getenv("CONSUME_PATH", consume_path)
lookup_interval = int(os.getenv("LOOKUP_INTERVAL", "5")) # default 5 seconds
api_url = os.getenv("API_URL", None)
api_key = os.getenv("API_KEY", None)
data_path = os.getenv("DATA_PATH", "/app/data")