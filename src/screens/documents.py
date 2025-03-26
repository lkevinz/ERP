from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


class DocumentsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Documents Module", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(["Document ID", "Title", "Type"])
        layout.addWidget(self.table)

        load_btn = QPushButton("Load Documents Data", self)
        load_btn.clicked.connect(self.load_documents)
        layout.addWidget(load_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_documents(self):
        self.table.setRowCount(0)
        sample_docs = [
            (4001, "Invoice Document", "Invoice"),
            (4002, "Delivery Note", "Delivery"),
        ]
        for doc in sample_docs:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(doc):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
