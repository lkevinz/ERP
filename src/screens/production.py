from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ProductionScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Módulo de Producción", self)
        layout.addWidget(label)
        self.setLayout(layout)
