import sys

# Importaciones de PyQt6
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QFrame,
)

# Importación de las screens (módulos locales)
from screens.dashboard import DashboardScreen
from screens.finance import FinanceScreen
from screens.inventory import InventoryScreen
from screens.hr import HRScreen
from screens.production import ProductionScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP - Sistema Integral (PyQt6)")
        self.setGeometry(50, 50, 1200, 800)
        self.setup_ui()

    def setup_ui(self):
        # Widget principal y layout horizontal
        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)

        # Panel lateral para navegación
        nav_panel = QFrame(main_widget)
        nav_panel.setFrameShape(QFrame.Shape.StyledPanel)
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setSpacing(10)

        # Botones de navegación para cada módulo
        self.dashboard_btn = QPushButton("Dashboard", nav_panel)
        self.finance_btn = QPushButton("Finanzas", nav_panel)
        self.inventory_btn = QPushButton("Inventario", nav_panel)
        self.hr_btn = QPushButton("RRHH", nav_panel)
        self.production_btn = QPushButton("Producción", nav_panel)

        # Conectar botones a la función que cambia la pantalla
        self.dashboard_btn.clicked.connect(lambda: self.switch_screen(0))
        self.finance_btn.clicked.connect(lambda: self.switch_screen(1))
        self.inventory_btn.clicked.connect(lambda: self.switch_screen(2))
        self.hr_btn.clicked.connect(lambda: self.switch_screen(3))
        self.production_btn.clicked.connect(lambda: self.switch_screen(4))

        # Agregar botones al panel de navegación
        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.finance_btn)
        nav_layout.addWidget(self.inventory_btn)
        nav_layout.addWidget(self.hr_btn)
        nav_layout.addWidget(self.production_btn)
        nav_layout.addStretch()

        # Área principal: QStackedWidget para cambiar entre screens
        self.stack = QStackedWidget(main_widget)
        self.stack.addWidget(DashboardScreen())
        self.stack.addWidget(FinanceScreen())
        self.stack.addWidget(InventoryScreen())
        self.stack.addWidget(HRScreen())
        self.stack.addWidget(ProductionScreen())

        # Agregar panel de navegación y el stack al layout principal
        main_layout.addWidget(nav_panel)
        main_layout.addWidget(self.stack)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 4)

        self.setCentralWidget(main_widget)

    def switch_screen(self, index):
        """Cambia la pantalla actual según el índice."""
        self.stack.setCurrentIndex(index)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
