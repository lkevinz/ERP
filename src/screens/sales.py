from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QGroupBox,
)
from PyQt6.QtCore import Qt
from database.ConexionSQL import conexionDB, cerrarConexion
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

        # --- SECCIÓN DE TABLAS (CLIENTES Y PROVEEDORES) ---
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(20)

        # --- GRUPO DE CLIENTES ---
        clientes_group = QGroupBox("CLIENTES")
        clientes_group.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 16px; }"
        )
        clientes_group_layout = QVBoxLayout()
        clientes_group_layout.setSpacing(10)

        # Layout para botón de carga
        clientes_toolbar = QHBoxLayout()

        # Botón de carga
        self.load_clientes_btn = QPushButton("Cargar Clientes", self)
        self.load_clientes_btn.clicked.connect(self.load_clientes)
        self.load_clientes_btn.setFixedWidth(200)
        clientes_toolbar.addWidget(self.load_clientes_btn)

        # Espaciador
        clientes_toolbar.addStretch()

        clientes_group_layout.addLayout(clientes_toolbar)

        # Tabla de clientes
        self.clientes_table = QTableWidget(0, 14, self)
        self.clientes_table.setHorizontalHeaderLabels(
            [
                "IdCliente",
                "NCliente",
                "Nombre",
                "Apellidos",
                "DNI",
                "Contacto",
                "Dirección",
                "Localidad",
                "Provincia",
                "Código Postal",
                "Teléfono",
                "Email",
                "Forma de Pago",
                "Firma Digital",
            ]
        )
        self.clientes_table.horizontalHeader().setStretchLastSection(True)
        clientes_group_layout.addWidget(self.clientes_table)

        clientes_group.setLayout(clientes_group_layout)
        tables_layout.addWidget(clientes_group)

        # --- GRUPO DE PROVEEDORES ---
        proveedores_group = QGroupBox("PROVEEDORES")
        proveedores_group.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 16px; }"
        )
        proveedores_group_layout = QVBoxLayout()
        proveedores_group_layout.setSpacing(10)

        # Layout para botón de carga
        proveedores_toolbar = QHBoxLayout()

        # Botón de carga
        self.load_proveedores_btn = QPushButton("Cargar Proveedores", self)
        self.load_proveedores_btn.clicked.connect(self.load_proveedores)
        self.load_proveedores_btn.setFixedWidth(200)
        proveedores_toolbar.addWidget(self.load_proveedores_btn)

        # Espaciador
        proveedores_toolbar.addStretch()

        proveedores_group_layout.addLayout(proveedores_toolbar)

        # Tabla de proveedores
        self.proveedores_table = QTableWidget(0, 11, self)
        self.proveedores_table.setHorizontalHeaderLabels(
            [
                "IdProveedor",
                "NProveedor",
                "FechaAlta",
                "Proveedor",
                "CIF",
                "Contacto",
                "Dirección",
                "Localidad",
                "Código Postal",
                "Provincia",
                "Teléfono",
                "Email",
            ]
        )
        self.proveedores_table.horizontalHeader().setStretchLastSection(True)
        proveedores_group_layout.addWidget(self.proveedores_table)

        proveedores_group.setLayout(proveedores_group_layout)
        tables_layout.addWidget(proveedores_group)

        main_layout.addLayout(tables_layout)

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
            self.clientes_table.setRowCount(0)

            # Configurar el número de filas según los resultados
            self.clientes_table.setRowCount(len(resultados))

            # Llenar la tabla con los datos
            for row_idx, row_data in enumerate(resultados):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(
                        str(col_data) if col_data is not None else ""
                    )
                    self.clientes_table.setItem(row_idx, col_idx, item)

        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            # Cerrar la conexión
            if conexion:
                cerrarConexion(conexion)

    def load_proveedores(self):
        # Establecer conexión y obtener conexión y cursor
        conexion, cursor = conexionDB()

        if not conexion or not cursor:
            print("Error al conectar a la base de datos")
            return

        try:
            # Consulta SQL para obtener los datos de proveedores
            sql = """
            SELECT IdProveedor, NProveedor, FechaAlta, Proveedor, CIF, 
                   Contacto, Direccion, Localidad, CodigoPostal, 
                   Provincia, Telefono, Email
            FROM proveedores
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()

            # Limpiar la tabla antes de cargar nuevos datos
            self.proveedores_table.setRowCount(0)

            # Configurar el número de filas según los resultados
            self.proveedores_table.setRowCount(len(resultados))

            # Llenar la tabla con los datos
            for row_idx, row_data in enumerate(resultados):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(
                        str(col_data) if col_data is not None else ""
                    )
                    self.proveedores_table.setItem(row_idx, col_idx, item)

        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            # Cerrar la conexión
            if conexion:
                cerrarConexion(conexion)
