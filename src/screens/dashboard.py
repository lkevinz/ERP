from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel("Dashboard", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title_label)

        # Example KPI cards (you could later integrate charts and dynamic data)
        kpi_sales = QLabel("Daily Sales: $1000", self)
        kpi_profit = QLabel("Profit: $500", self)
        kpi_inventory = QLabel("Inventory: 150 units", self)
        layout.addWidget(kpi_sales)
        layout.addWidget(kpi_profit)
        layout.addWidget(kpi_inventory)

        refresh_btn = QPushButton("Refresh Dashboard", self)
        refresh_btn.clicked.connect(self.refresh_dashboard)
        layout.addWidget(refresh_btn)

        layout.addStretch()
        self.setLayout(layout)

    def refresh_dashboard(self):
        # Aquí se actualizarían los datos consultando la base de datos
        print("Dashboard refreshed.")
