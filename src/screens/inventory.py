from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class InventoryScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Inventory Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 4, self)
        self.table.setHorizontalHeaderLabels(
            ["Product ID", "Product Name", "Stock", "Location"]
        )
        layout.addWidget(self.table)

        load_btn = QPushButton("Load Inventory Data", self)
        load_btn.clicked.connect(self.load_inventory)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_inventory(self):
        self.table.setRowCount(0)
        sample_inventory = [
            (1, "Product A", 100, "Warehouse 1"),
            (2, "Product B", 50, "Warehouse 2"),
        ]
        for product in sample_inventory:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(product):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
