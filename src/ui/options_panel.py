from PyQt6.QtWidgets import (
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QCheckBox,
    QHBoxLayout,
    QLineEdit,
    QLabel,
)

from ..core.config import RsyncConfig


class OptionsPanel(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Rsync Options")
        self._dry_run = QCheckBox("Dry run (--dry-run)")
        self._delete = QCheckBox("Delete extras (--delete)")
        self._compress = QCheckBox("Compress (-z)")
        self._partial = QCheckBox("Keep partial (--partial)")

        bw_layout = QHBoxLayout()
        bw_layout.addWidget(QLabel("Bandwidth limit (KB/s):"))
        self._bwlimit = QLineEdit()
        self._bwlimit.setPlaceholderText("e.g. 1000")
        bw_layout.addWidget(self._bwlimit)
        bw_layout.addStretch()

        self._extra = QLineEdit()
        self._extra.setPlaceholderText("Extra rsync options...")

        layout = QVBoxLayout(self)
        layout.addWidget(self._dry_run)
        layout.addWidget(self._delete)
        layout.addWidget(self._compress)
        layout.addWidget(self._partial)
        layout.addLayout(bw_layout)
        layout.addWidget(QLabel("Extra options:"))
        layout.addWidget(self._extra)

    def to_config(self) -> RsyncConfig:
        return RsyncConfig(
            dry_run=self._dry_run.isChecked(),
            delete=self._delete.isChecked(),
            compress=self._compress.isChecked(),
            partial=self._partial.isChecked(),
            bwlimit=self._bwlimit.text().strip(),
            extra_options=self._extra.text().strip(),
        )

    def reset(self) -> None:
        self._dry_run.setChecked(False)
        self._delete.setChecked(False)
        self._compress.setChecked(False)
        self._partial.setChecked(False)
        self._bwlimit.clear()
        self._extra.clear()
