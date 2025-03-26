from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class ProjectsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Projects Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 4, self)
        self.table.setHorizontalHeaderLabels(
            ["Project ID", "Project Name", "Start Date", "Status"]
        )
        layout.addWidget(self.table)

        load_btn = QPushButton("Load Projects Data", self)
        load_btn.clicked.connect(self.load_projects)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_projects(self):
        self.table.setRowCount(0)
        sample_projects = [
            (3001, "Project Alpha", "2023-01-15", "Active"),
            (3002, "Project Beta", "2023-02-20", "Completed"),
        ]
        for proj in sample_projects:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(proj):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
