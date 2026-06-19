import sys

from PyQt6.QtWidgets import QApplication

from .core.theme import DarkTheme
from .ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Rsync GUI")
    app.setApplicationDisplayName("Rsync GUI")
    DarkTheme.apply(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
