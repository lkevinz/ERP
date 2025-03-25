from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class InventoryScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Módulo de Inventario", self)
        layout.addWidget(label)
        self.setLayout(layout)
