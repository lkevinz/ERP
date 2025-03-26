from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class SalesScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Sales Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Tabla para mostrar datos de ventas (facturas, pedidos, etc.)
        self.table = QTableWidget(0, 5, self)
        self.table.setHorizontalHeaderLabels(
            ["Invoice ID", "Client", "Date", "Amount", "Status"]
        )
        layout.addWidget(self.table)

        load_btn = QPushButton("Load Sales Data", self)
        load_btn.clicked.connect(self.load_sales)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_sales(self):
        # Aquí se conectarían consultas reales a la base de datos
        self.table.setRowCount(0)
        sample_sales = [
            (1001, "Client A", "2023-03-01", "$500", "Paid"),
            (1002, "Client B", "2023-03-02", "$750", "Pending"),
        ]
        for sale in sample_sales:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(sale):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
