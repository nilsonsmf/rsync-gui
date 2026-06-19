from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QMessageBox,
)

from .directory_selector import DirectorySelector
from .destination_selector import DestinationSelector
from .options_panel import OptionsPanel
from .progress_panel import ProgressPanel
from .history_panel import HistoryPanel
from ..core.rsync_worker import RsyncWorker, RsyncResult
from ..core.config import RsyncConfig
from ..core.storage import Storage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rsync GUI")
        self.setMinimumSize(780, 620)

        self._storage = Storage()
        self._worker: RsyncWorker | None = None
        self._last_config: RsyncConfig | None = None
        self._cancelled = False
        self._cleaned_up = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Source (local directory):"))
        self._source = DirectorySelector(
            placeholder="/path/to/local/directory"
        )
        layout.addWidget(self._source)

        layout.addWidget(QLabel("Destination:"))
        self._dest = DestinationSelector(self._storage)
        layout.addWidget(self._dest)

        self._options = OptionsPanel()
        layout.addWidget(self._options)

        btn_row = QHBoxLayout()
        self._run_btn = QPushButton("Run Rsync")
        self._run_btn.clicked.connect(self._run_rsync)
        self._stop_btn = QPushButton("Stop")
        self._stop_btn.clicked.connect(self._stop_rsync)
        self._stop_btn.setEnabled(False)
        btn_row.addStretch()
        btn_row.addWidget(self._run_btn)
        btn_row.addWidget(self._stop_btn)
        layout.addLayout(btn_row)

        self._progress = ProgressPanel()
        layout.addWidget(self._progress, 1)

        self._history = HistoryPanel(self._storage)
        layout.addWidget(self._history)

    def _run_rsync(self) -> None:
        source = self._source.path.strip()
        dest = self._dest.path.strip()

        if not source:
            QMessageBox.warning(self, "Validation", "Select a source directory.")
            return
        if not dest:
            QMessageBox.warning(self, "Validation", "Enter a destination.")
            return

        config = self._options.to_config()
        config.source = source
        config.destination = dest
        self._last_config = config

        self._cancelled = False
        self._cleaned_up = False
        self._progress.clear()
        self._progress.set_status("Starting rsync...")
        self._run_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)

        self._worker = RsyncWorker(config)
        self._worker.progress_updated.connect(self._progress.set_progress)
        self._worker.output_line.connect(self._progress.append_log)
        self._worker.finished.connect(self._on_finished)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()

    def _stop_rsync(self) -> None:
        if self._worker:
            self._cancelled = True
            self._worker.stop()
            self._progress.append_log("--- Cancelled by user ---")

    def _on_finished(self, result: RsyncResult) -> None:
        if self._cleaned_up:
            return

        rc = result.return_code

        if self._cancelled:
            status = "Cancelled"
        elif rc == 0:
            status = "Completed"
        else:
            self._progress.append_log(f"rsync exited with code {rc}")
            status = f"Failed (exit {rc})"

        self._progress.set_status(status)

        cfg = self._last_config
        if cfg and rc == 0 and not self._cancelled:
            record = self._storage.make_record(
                source=cfg.source,
                destination=cfg.destination,
                options=" ".join(cfg.build_args()),
                bytes_sent=result.bytes_sent,
                bytes_received=result.bytes_received,
                elapsed_seconds=int(result.elapsed_seconds),
                status=status,
            )
            self._storage.add_job(record)
            self._history.add_job(record)
            self._dest.add_destination(cfg.destination)

        self._cleanup_worker()

    def _on_error(self, message: str) -> None:
        if self._cleaned_up:
            return
        self._progress.append_log(f"ERROR: {message}")
        self._progress.set_status("Failed to start")
        self._cleanup_worker()

    def _cleanup_worker(self) -> None:
        if self._cleaned_up:
            return
        self._cleaned_up = True
        self._run_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._cancelled = False
        if self._worker:
            self._worker.progress_updated.disconnect()
            self._worker.output_line.disconnect()
            self._worker.finished.disconnect()
            self._worker.error_occurred.disconnect()
        self._worker = None
