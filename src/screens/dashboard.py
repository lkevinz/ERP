from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from screens.ConexionSQL import conexionDB, cerrarConexion
from datetime import datetime, timedelta
import pymysql  # Asegurarse de importar pymysql en este archivo también

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        
        # Título del dashboard
        label = QLabel("Bienvenido al Dashboard del ERP", self)
        main_layout.addWidget(label)

        # Subtítulo
        label2 = QLabel("Proyectos", self)
        main_layout.addWidget(label2)

        # Layout superior para los botones (horizontal)
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # Botón para ver proyectos de la semana actual
        filter_week_button = QPushButton("Ver últimos proyectos de la semana", self)
        filter_week_button.clicked.connect(self.filter_week_projects)
        top_layout.addWidget(filter_week_button)

        # Botón para ver todos los proyectos
        all_projects_button = QPushButton("Ver todos los proyectos", self)
        all_projects_button.clicked.connect(self.load_table_data)
        top_layout.addWidget(all_projects_button)

        # Alinear los botones a la esquina superior derecha
        top_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

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
            query = filter_query if filter_query else "SELECT IdProyecto, NProyecto, NombreObra, Direccion, Localidad, Telefono1, Email, Fecha, IdCliente FROM proyectos"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Configurar número de filas y columnas
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels([
                "IdProyecto", "NProyecto", "NombreObra", "Direccion",
                "Localidad", "Telefono1", "Email", "Fecha", "IdCliente"
            ])

            # Llenar la tabla con los datos
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except pymysql.Error as e:
            print(f"Error al cargar los datos: {e}")
        finally:
            cerrarConexion(miConexion)

    def filter_week_projects(self):
        """Filtra y muestra los proyectos de la semana actual."""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # Lunes de la semana
        query = f"""
            SELECT IdProyecto, NProyecto, NombreObra, Direccion, Localidad, Telefono1, Email, Fecha, IdCliente
            FROM proyectos
            WHERE Fecha >= '{start_of_week.strftime('%Y-%m-%d')}'
        """
        self.load_table_data(filter_query=query)
