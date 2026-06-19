import os
from dataclasses import dataclass, asdict
from datetime import datetime

import yaml


CONFIG_DIR = os.path.expanduser("~/.config/rsync-gui")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")


@dataclass
class JobRecord:
    timestamp: str = ""
    source: str = ""
    destination: str = ""
    options: str = ""
    bytes_sent: int = 0
    bytes_received: int = 0
    elapsed_seconds: int = 0
    status: str = ""


class Storage:
    def __init__(self, path: str = CONFIG_PATH) -> None:
        self._path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def _load(self) -> dict:
        if not os.path.exists(self._path):
            return {}
        with open(self._path) as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}

    def _save(self, data: dict) -> None:
        with open(self._path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def get_recent_destinations(self) -> list[str]:
        return self._load().get("recent_destinations", [])

    def add_destination(self, dest: str) -> None:
        data = self._load()
        dests = data.get("recent_destinations", [])
        if dest in dests:
            dests.remove(dest)
        dests.insert(0, dest)
        data["recent_destinations"] = dests[:10]
        self._save(data)

    def get_job_history(self) -> list[JobRecord]:
        return [
            JobRecord(**j)
            for j in self._load().get("job_history", [])
        ]

    def add_job(self, record: JobRecord) -> None:
        data = self._load()
        history = data.get("job_history", [])
        history.insert(0, asdict(record))
        data["job_history"] = history[:5]
        self._save(data)

    @staticmethod
    def make_record(
        source: str,
        destination: str,
        options: str,
        bytes_sent: int,
        bytes_received: int,
        elapsed_seconds: int,
        status: str,
    ) -> JobRecord:
        return JobRecord(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source=source,
            destination=destination,
            options=options,
            bytes_sent=bytes_sent,
            bytes_received=bytes_received,
            elapsed_seconds=elapsed_seconds,
            status=status,
        )
