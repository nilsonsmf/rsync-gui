from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal


class DirectorySelector(QWidget):
    path_changed = pyqtSignal(str)

    def __init__(
        self,
        placeholder: str = "",
        dialog_title: str = "Select Directory",
        show_browse: bool = True,
    ):
        super().__init__()
        self._dialog_title = dialog_title
        self._path = QLineEdit()
        self._path.setPlaceholderText(placeholder)
        self._path.textChanged.connect(self.path_changed.emit)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._path)

        if show_browse:
            self._browse_btn = QPushButton("Browse...")
            self._browse_btn.clicked.connect(self._browse)
            layout.addWidget(self._browse_btn)

    def _browse(self) -> None:
        path = QFileDialog.getExistingDirectory(self, self._dialog_title)
        if path:
            self._path.setText(path)

    @property
    def path(self) -> str:
        return self._path.text()

    @path.setter
    def path(self, value: str) -> None:
        self._path.setText(value)
