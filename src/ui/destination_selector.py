from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox
from PyQt6.QtCore import pyqtSignal

from ..core.storage import Storage


class DestinationSelector(QWidget):
    path_changed = pyqtSignal(str)

    def __init__(self, storage: Storage, parent=None):
        super().__init__(parent)
        self._storage = storage
        self._combo = QComboBox()
        self._combo.setEditable(True)
        self._combo.setPlaceholderText("user@host:/path or /local/path")
        self._combo.currentTextChanged.connect(self.path_changed.emit)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._combo)

        self._load()

    def _load(self) -> None:
        for dest in self._storage.get_recent_destinations():
            self._combo.addItem(dest)

    def add_destination(self, dest: str) -> None:
        if not dest:
            return
        idx = self._combo.findText(dest)
        if idx >= 0:
            self._combo.removeItem(idx)
        self._combo.insertItem(0, dest)
        self._combo.setCurrentIndex(0)
        self._storage.add_destination(dest)

    @property
    def path(self) -> str:
        return self._combo.currentText().strip()

    @path.setter
    def path(self, value: str) -> None:
        self._combo.setCurrentText(value)
