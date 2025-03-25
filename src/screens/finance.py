from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class FinanceScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Módulo de Finanzas", self)
        layout.addWidget(label)
        self.setLayout(layout)
