from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)

from ..core.storage import Storage, JobRecord


class HistoryPanel(QGroupBox):
    def __init__(self, storage: Storage, parent=None):
        super().__init__("Recent Jobs", parent)
        self._storage = storage

        layout = QVBoxLayout(self)
        self._table = QTableWidget(0, 5)
        self._table.setHorizontalHeaderLabels(
            ["Time", "Source", "Destination", "Data", "Duration"]
        )
        self._table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self._table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self._table.verticalHeader().setVisible(False)
        self._table.setAlternatingRowColors(True)

        h = self._table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self._table)
        for job in self._storage.get_job_history():
            self._add_row(job)

    def add_job(self, job: JobRecord) -> None:
        self._table.insertRow(0)
        self._set_row(0, job)
        while self._table.rowCount() > 5:
            self._table.removeRow(self._table.rowCount() - 1)

    def _add_row(self, job: JobRecord) -> None:
        row = self._table.rowCount()
        self._table.insertRow(row)
        self._set_row(row, job)

    def _set_row(self, row: int, job: JobRecord) -> None:
        self._table.setItem(row, 0, QTableWidgetItem(job.timestamp))
        self._table.setItem(row, 1, QTableWidgetItem(job.source))
        self._table.setItem(row, 2, QTableWidgetItem(job.destination))
        total = job.bytes_sent + job.bytes_received
        self._table.setItem(row, 3, QTableWidgetItem(self._format_size(total)))
        self._table.setItem(row, 4, QTableWidgetItem(self._format_time(job.elapsed_seconds)))

    @staticmethod
    def _format_size(b: int) -> str:
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if b < 1024:
                return f"{b:.1f}{unit}"
            b //= 1024
        return f"{b:.1f}PB"

    @staticmethod
    def _format_time(s: int) -> str:
        if s < 60:
            return f"{s}s"
        m, s = divmod(s, 60)
        return f"{m}m{s}s" if m < 60 else f"{m // 60}h{m % 60}m"
