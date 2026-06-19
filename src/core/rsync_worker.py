import re
import subprocess
import time
from dataclasses import dataclass

from PyQt6.QtCore import QThread, pyqtSignal

from .config import RsyncConfig
from .progress_parser import RsyncProgressParser


@dataclass
class RsyncResult:
    return_code: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    elapsed_seconds: float = 0.0


_SENT_RE = re.compile(r"sent\s+([\d,]+)\s+bytes")
_RECV_RE = re.compile(r"received\s+([\d,]+)\s+bytes")


class RsyncWorker(QThread):
    progress_updated = pyqtSignal(int)
    output_line = pyqtSignal(str)
    finished = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(self, config: RsyncConfig):
        super().__init__()
        self._config = config
        self._process: subprocess.Popen | None = None

    def run(self) -> None:
        cmd = ["rsync"]
        cmd.extend(self._config.build_args())

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
            )
        except FileNotFoundError:
            self.error_occurred.emit(
                "rsync not found. Install it with: sudo apt install rsync"
            )
            return

        assert self._process.stdout is not None

        start = time.monotonic()
        bytes_sent = 0
        bytes_received = 0

        for line in iter(self._process.stdout.readline, ""):
            stripped = line.rstrip("\n\r")
            self.output_line.emit(stripped)

            progress = RsyncProgressParser.parse(stripped)
            if progress is not None:
                self.progress_updated.emit(progress)

            sent_m = _SENT_RE.search(stripped)
            if sent_m:
                bytes_sent = int(sent_m.group(1).replace(",", ""))
            recv_m = _RECV_RE.search(stripped)
            if recv_m:
                bytes_received = int(recv_m.group(1).replace(",", ""))

        elapsed = time.monotonic() - start
        self._process.stdout.close()
        return_code = self._process.wait()

        result = RsyncResult(
            return_code=return_code,
            bytes_sent=bytes_sent,
            bytes_received=bytes_received,
            elapsed_seconds=elapsed,
        )

        self.finished.emit(result)

    def stop(self) -> None:
        if self._process and self._process.returncode is None:
            self._process.kill()
