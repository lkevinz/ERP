from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class HRScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("HR Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 4, self)
        self.table.setHorizontalHeaderLabels(
            ["Employee ID", "Name", "Department", "Position"]
        )
        layout.addWidget(self.table)

        load_btn = QPushButton("Load HR Data", self)
        load_btn.clicked.connect(self.load_hr)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_hr(self):
        self.table.setRowCount(0)
        sample_employees = [
            (1, "John Doe", "Sales", "Manager"),
            (2, "Jane Smith", "Finance", "Analyst"),
        ]
        for emp in sample_employees:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(emp):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
