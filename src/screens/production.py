from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class ProductionScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Production Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 4, self)
        self.table.setHorizontalHeaderLabels(
            ["Order ID", "Order Name", "Status", "Date"]
        )
        layout.addWidget(self.table)

        load_btn = QPushButton("Load Production Data", self)
        load_btn.clicked.connect(self.load_production)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_production(self):
        self.table.setRowCount(0)
        sample_orders = [
            (1, "Production Order #001", "In Process", "2023-03-10"),
            (2, "Production Order #002", "Completed", "2023-03-11"),
        ]
        for order in sample_orders:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(order):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
