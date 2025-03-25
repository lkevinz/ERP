from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Bienvenido al Dashboard del ERP", self)
        layout.addWidget(label)
        self.setLayout(layout)
