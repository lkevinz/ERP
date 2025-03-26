import sys
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


from screens.dashboard import DashboardScreen
from screens.sales import SalesScreen
from screens.inventory import InventoryScreen
from screens.finance import FinanceScreen
from screens.hr import HRScreen
from screens.production import ProductionScreen
from screens.projects import ProjectsScreen
from screens.purchasing import PurchasingScreen
from screens.documents import DocumentsScreen


import os
from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP - Integrated System (PyQt6)")
        self.setGeometry(50, 50, 1400, 900)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "icon", "icon_erp.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)

        # Navigation panel
        nav_panel = QFrame(main_widget)
        nav_panel.setFrameShape(QFrame.Shape.StyledPanel)
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setSpacing(10)

        # Navigation buttons
        self.dashboard_btn = QPushButton("Dashboard", nav_panel)
        self.sales_btn = QPushButton("Sales", nav_panel)
        self.inventory_btn = QPushButton("Inventory", nav_panel)
        self.finance_btn = QPushButton("Finance", nav_panel)
        self.hr_btn = QPushButton("HR", nav_panel)
        self.production_btn = QPushButton("Production", nav_panel)
        self.projects_btn = QPushButton("Projects", nav_panel)
        self.purchasing_btn = QPushButton("Purchasing", nav_panel)
        self.documents_btn = QPushButton("Documents", nav_panel)

        self.dashboard_btn.clicked.connect(lambda: self.switch_screen(0))
        self.sales_btn.clicked.connect(lambda: self.switch_screen(1))
        self.inventory_btn.clicked.connect(lambda: self.switch_screen(2))
        self.finance_btn.clicked.connect(lambda: self.switch_screen(3))
        self.hr_btn.clicked.connect(lambda: self.switch_screen(4))
        self.production_btn.clicked.connect(lambda: self.switch_screen(5))
        self.projects_btn.clicked.connect(lambda: self.switch_screen(6))
        self.purchasing_btn.clicked.connect(lambda: self.switch_screen(7))
        self.documents_btn.clicked.connect(lambda: self.switch_screen(8))

        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.sales_btn)
        nav_layout.addWidget(self.inventory_btn)
        nav_layout.addWidget(self.finance_btn)
        nav_layout.addWidget(self.hr_btn)
        nav_layout.addWidget(self.production_btn)
        nav_layout.addWidget(self.projects_btn)
        nav_layout.addWidget(self.purchasing_btn)
        nav_layout.addWidget(self.documents_btn)
        nav_layout.addStretch()

        # Stacked widget to hold each screen
        self.stack = QStackedWidget(main_widget)
        self.stack.addWidget(DashboardScreen())
        self.stack.addWidget(SalesScreen())
        self.stack.addWidget(InventoryScreen())
        self.stack.addWidget(FinanceScreen())
        self.stack.addWidget(HRScreen())
        self.stack.addWidget(ProductionScreen())
        self.stack.addWidget(ProjectsScreen())
        self.stack.addWidget(PurchasingScreen())
        self.stack.addWidget(DocumentsScreen())

        main_layout.addWidget(nav_panel)
        main_layout.addWidget(self.stack)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 8)

        self.setCentralWidget(main_widget)

    def switch_screen(self, index: int):
        self.stack.setCurrentIndex(index)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
