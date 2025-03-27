from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from database.ConexionSQL import conexionDB, cerrarConexion
from datetime import datetime, timedelta
import pymysql


class ProjectsScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal vertical
        main_layout = QVBoxLayout(self)

        # Título
        title_label = QLabel("PROJECTS", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 15px;"
        )
        main_layout.addWidget(title_label)

        # Layout superior para los botones (horizontal)
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # Botón para ver proyectos de la semana actual
        filter_month_button = QPushButton("Ver últimos proyectos del ultimo mes", self)
        filter_month_button.clicked.connect(self.filter_current_month_projects)
        top_layout.addWidget(filter_month_button)

        # Botón para cargar todos los proyectos
        all_projects_button = QPushButton("Ver todos los proyectos", self)
        all_projects_button.clicked.connect(self.load_table_data)
        top_layout.addWidget(all_projects_button)

        # Alinear los botones a la esquina superior derecha
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Tabla de proyectos
        self.table = QTableWidget(self)
        main_layout.addWidget(self.table)

        # Configurar el layout principal
        self.setLayout(main_layout)

        # Llenar la tabla con todos los datos inicialmente
        self.load_table_data()

    def load_table_data(self, filter_query=None):
        """Llena la tabla con los datos de la base de datos."""
        try:
            miConexion, cursor = conexionDB()
            if not miConexion or not cursor:
                print("No se pudo establecer conexión con la base de datos.")
                return

            # Ejecutar consulta con o sin filtro
            query = (
                filter_query
                if filter_query
                else "SELECT IdProyecto, NProyecto, NombreObra, Direccion, Localidad, Telefono1, Email, Fecha, IdCliente FROM proyectos"
            )
            cursor.execute(query)
            rows = cursor.fetchall()

            # Configurar número de filas y columnas
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(
                [
                    "IdProyecto",
                    "NProyecto",
                    "NombreObra",
                    "Direccion",
                    "Localidad",
                    "Telefono1",
                    "Email",
                    "Fecha",
                    "IdCliente",
                ]
            )

            # Llenar la tabla con los datos
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except pymysql.Error as e:
            print(f"Error al cargar los datos: {e}")
        finally:
            cerrarConexion(miConexion)

    # Filtra y muestra los proyectos del mes actual
    def filter_current_month_projects(self):
        today = datetime.now()
        current_year = today.year
        current_month = today.month

        query = f"""
            SELECT IdProyecto, NProyecto, NombreObra, Direccion, Localidad, 
               Telefono1, Email, Fecha, IdCliente
            FROM proyectos
            WHERE YEAR(Fecha) = {current_year} AND MONTH(Fecha) = {current_month}
            """
        self.load_table_data(filter_query=query)
