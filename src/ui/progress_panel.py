from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QPlainTextEdit, QLabel
from PyQt6.QtCore import Qt


class ProgressPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._bar = QProgressBar()
        self._bar.setValue(0)
        self._bar.setTextVisible(True)
        self._bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._status = QLabel("Ready")

        self._log = QPlainTextEdit()
        self._log.setReadOnly(True)
        self._log.setMaximumBlockCount(5000)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._status)
        layout.addWidget(self._bar)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self._log)

    def set_progress(self, value: int) -> None:
        self._bar.setValue(value)

    def append_log(self, text: str) -> None:
        self._log.appendPlainText(text)

    def set_status(self, text: str) -> None:
        self._status.setText(text)

    def clear(self) -> None:
        self._bar.reset()
        self._status.setText("Running...")
        self._log.clear()
