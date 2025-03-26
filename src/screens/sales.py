from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from screens.ConexionSQL import conexionDB, cerrarConexion
import pymysql 


class SalesScreen(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # --- SECCIÓN DE TÍTULO PRINCIPAL ---
        title_layout = QHBoxLayout()
        
        # Título principal "Sales"
        title_label = QLabel("Sales", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_label)

        main_layout.addLayout(title_layout)

        # --- SECCIÓN DE CLIENTES ---
        clientes_group_layout = QVBoxLayout()
        clientes_group_layout.setSpacing(10)

        # Subtítulo "CLIENTES"
        clientes_label = QLabel("CLIENTES", self)
        clientes_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        clientes_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 16px;
            padding: 5px;
            border-bottom: 2px solid #ccc;
        """)
        clientes_group_layout.addWidget(clientes_label)

        # Layout para botón y espacio
        clientes_toolbar = QHBoxLayout()
        
        # Botón de carga
        self.load_btn = QPushButton("Cargar Datos de Clientes", self)
        self.load_btn.clicked.connect(self.load_clientes)
        self.load_btn.setFixedWidth(200)
        clientes_toolbar.addWidget(self.load_btn)
        
        # Espaciador para empujar todo a la izquierda
        clientes_toolbar.addStretch()
        
        clientes_group_layout.addLayout(clientes_toolbar)

        # Tabla de clientes
        self.table = QTableWidget(0, 14, self)
        self.table.setHorizontalHeaderLabels(
            ["IdCliente", "NCliente", "Nombre", "Apellidos", "DNI", "Contacto", 
             "Dirección", "Localidad", "Provincia", "Código Postal", 
             "Teléfono", "Email", "Forma de Pago", "Firma Digital"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        clientes_group_layout.addWidget(self.table)

        main_layout.addLayout(clientes_group_layout)

    def load_clientes(self):
        # Establecer conexión y obtener conexión y cursor
        conexion, cursor = conexionDB()
        
        if not conexion or not cursor:
            print("Error al conectar a la base de datos")
            return
            
        try:
            # Consulta SQL para obtener los datos de clientes
            sql = """
            SELECT IdCliente, NCliente, Nombre, Apellidos, DNI, Contacto, 
                   Direccion, Localidad, Provincia, CodigoPostal, 
                   Telefono, Email, IdFormaDePago, URLFirmaDatos 
            FROM clientes
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            # Limpiar la tabla antes de cargar nuevos datos
            self.table.setRowCount(0)
            
            # Configurar el número de filas según los resultados
            self.table.setRowCount(len(resultados))
            
            # Llenar la tabla con los datos
            for row_idx, row_data in enumerate(resultados):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data) if col_data is not None else "")
                    self.table.setItem(row_idx, col_idx, item)
                    
        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            # Cerrar la conexión
            if conexion:
                cerrarConexion(conexion)