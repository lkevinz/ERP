import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QFrame,
    QMessageBox,
)
from PyQt6.QtGui import QIcon

# Pantallas existentes
from screens.dashboard import DashboardScreen
from screens.sales import SalesScreen
from screens.inventory import InventoryScreen
from screens.finance import FinanceScreen
from screens.hr import HRScreen
from screens.production import ProductionScreen
from screens.projects import ProjectsScreen
from screens.purchasing import PurchasingScreen
from screens.documents import DocumentsScreen

# Función para generar el informe
from reports.rentabilidad_informe import generar_informe_rentabilidad

# Funciones de modelo (opcional)
from analysis.rentabilidad_model import (
    entrenar_modelo_neuronal,
    predecir_rentabilidad_neuronal,
)


def resource_path(relative_path: str) -> str:
    # Si sys._MEIPASS existe, úsalo. Si no, usa la carpeta actual.
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP - Integrated System (PyQt6)")
        self.setGeometry(50, 50, 1400, 900)

        # Establecemos el ícono de la ventana
        icon_path = resource_path(os.path.join("icon", "icon_erp.ico"))
        self.setWindowIcon(QIcon(icon_path))

        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)

        # Panel de navegación
        nav_panel = QFrame(main_widget)
        nav_panel.setFrameShape(QFrame.Shape.StyledPanel)
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setSpacing(10)

        # Botones de navegación
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

        # Botón para generar informe de rentabilidad
        self.rentabilidad_btn = QPushButton("Generar Informe Rentabilidad", nav_panel)
        self.rentabilidad_btn.clicked.connect(self.on_rentabilidad_btn_clicked)

        # Botón para entrenar o predecir con el modelo (opcional)
        self.ia_btn = QPushButton("Entrenar Modelo IA (Ejemplo)", nav_panel)
        self.ia_btn.clicked.connect(self.on_ia_btn_clicked)

        # Agregar botones al layout de navegación
        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.sales_btn)
        nav_layout.addWidget(self.inventory_btn)
        nav_layout.addWidget(self.finance_btn)
        nav_layout.addWidget(self.hr_btn)
        nav_layout.addWidget(self.production_btn)
        nav_layout.addWidget(self.projects_btn)
        nav_layout.addWidget(self.purchasing_btn)
        nav_layout.addWidget(self.documents_btn)
        nav_layout.addWidget(self.rentabilidad_btn)
        nav_layout.addWidget(self.ia_btn)
        nav_layout.addStretch()

        # Stacked widget con las pantallas
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

    def on_rentabilidad_btn_clicked(self):
        """
        Genera el informe de rentabilidad y muestra un mensaje confirmando la operación.
        """
        try:
            generar_informe_rentabilidad()
            QMessageBox.information(
                self,
                "Informe de Rentabilidad",
                "Informe generado correctamente en la carpeta Descargas.",
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Ocurrió un error al generar el informe:\n{str(e)}"
            )

    def on_ia_btn_clicked(self):
        try:
            model, scaler, losses = entrenar_modelo_neuronal(
                epochs=50, batch_size=32, learning_rate=0.001
            )
            QMessageBox.information(
                self, "Entrenamiento IA", "Modelo neuronal entrenado con éxito."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error IA", f"Ocurrió un error:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    # Icono global para la barra de tareas
    app.setWindowIcon(QIcon(resource_path("icon/icon_erp.ico")))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
