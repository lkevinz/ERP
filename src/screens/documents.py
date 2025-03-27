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


class DocumentsScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal vertical
        main_layout = QVBoxLayout(self)

        # Título
        title_label = QLabel("DOCUMENTS", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 15px;"
        )
        main_layout.addWidget(title_label)

        # Layout superior para los botones (horizontal)
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # Botón para ver documentos recientes
        recent_button = QPushButton("Ver documentos recientes", self)
        recent_button.clicked.connect(self.filter_recent_documents)
        top_layout.addWidget(recent_button)

        # Botón para cargar todos los documentos
        all_documents_button = QPushButton("Ver todos los documentos", self)
        all_documents_button.clicked.connect(self.load_table_data)
        top_layout.addWidget(all_documents_button)

        # Alinear los botones a la esquina superior izquierda
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Tabla de documentos
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
                else "SELECT IdDocumento, Id, Tipo, Ruta, Titulo, IdCarpeta, Alta, IdUsuario, Dispositivo, IP, Hash FROM documentos"
            )
            cursor.execute(query)
            rows = cursor.fetchall()

            # Configurar número de filas y columnas
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(11)
            self.table.setHorizontalHeaderLabels(
                [
                    "IdDocumento",
                    "Id",
                    "Tipo",
                    "Ruta",
                    "Titulo",
                    "IdCarpeta",
                    "Alta",
                    "IdUsuario",
                    "Dispositivo",
                    "IP",
                    "Hash",
                ]
            )

            # Llenar la tabla con los datos
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Ajustar el tamaño de las columnas al contenido
            self.table.resizeColumnsToContents()

        except pymysql.Error as e:
            print(f"Error al cargar los datos: {e}")
        finally:
            if 'miConexion' in locals():
                cerrarConexion(miConexion)

    def filter_recent_documents(self):
        """Filtra y muestra los documentos de los últimos 30 días"""
        thirty_days_ago = datetime.now() - timedelta(days=30)
        date_str = thirty_days_ago.strftime('%Y-%m-%d')

        query = f"""
            SELECT IdDocumento, Id, Tipo, Ruta, Titulo, IdCarpeta, 
                   Alta, IdUsuario, Dispositivo, IP, Hash
            FROM documentos
            WHERE Alta >= '{date_str}'
            ORDER BY Alta DESC
            """
        self.load_table_data(filter_query=query)