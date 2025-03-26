from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class FinanceScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Finance Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 4, self)
        self.table.setHorizontalHeaderLabels(
            ["Transaction ID", "Date", "Description", "Amount"]
        )
        layout.addWidget(self.table)

        load_btn = QPushButton("Load Finance Data", self)
        load_btn.clicked.connect(self.load_finance)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_finance(self):
        self.table.setRowCount(0)
        sample_transactions = [
            (1, "2023-03-01", "Invoice Payment", "$250"),
            (2, "2023-03-02", "Expense Reimbursement", "$350"),
        ]
        for trans in sample_transactions:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(trans):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
