import json, time
from pathlib import Path

class JsonlLogger:
    def __init__(self, path: Path):
        self.path = path
    def log(self, **kv):
        kv.setdefault("ts", time.time())
        with open(self.path, "a") as f:
            f.write(json.dumps(kv) + "\n")
