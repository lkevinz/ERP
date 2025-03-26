from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class PurchasingScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Purchasing Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 4, self)
        self.table.setHorizontalHeaderLabels(
            ["Order ID", "Supplier", "Date", "Total Amount"]
        )
        layout.addWidget(self.table)

        load_btn = QPushButton("Load Purchasing Data", self)
        load_btn.clicked.connect(self.load_purchasing)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_purchasing(self):
        self.table.setRowCount(0)
        sample_orders = [
            (2001, "Supplier X", "2023-03-05", "$1000"),
            (2002, "Supplier Y", "2023-03-06", "$1500"),
        ]
        for order in sample_orders:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(order):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
