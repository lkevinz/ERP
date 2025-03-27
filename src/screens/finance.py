from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QGroupBox,
)
from PyQt6.QtCore import Qt
from database.connectionSQL import conexionDB, cerrarConexion


class FinanceScreen(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)  # Añade espacio entre secciones
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Título
        title_label = QLabel("FINANCE", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 15px;"
        )
        main_layout.addWidget(title_label)

        # --- SECCIÓN FACTURAS ---
        facturas_group = QGroupBox("FACTURAS")
        facturas_group.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 16px; }"
        )
        facturas_layout = QVBoxLayout()

        # Botones de facturas
        buttons_facturas_layout = QHBoxLayout()
        view_month_btn = QPushButton("Facturas de este mes", self)
        view_month_btn.clicked.connect(self.load_month_facturas)
        view_month_btn.setFixedWidth(200)
        buttons_facturas_layout.addWidget(view_month_btn)

        load_facturas_btn = QPushButton("Cargar todas las facturas", self)
        load_facturas_btn.clicked.connect(self.load_facturas)
        load_facturas_btn.setFixedWidth(200)
        buttons_facturas_layout.addWidget(load_facturas_btn)

        buttons_facturas_layout.addStretch()  # Empuja los botones a la izquierda
        facturas_layout.addLayout(buttons_facturas_layout)

        # Tabla de facturaspro
        self.facturas_table = QTableWidget(0, 18, self)
        self.facturas_table.setHorizontalHeaderLabels(
            [
                "IdFacturaPro",
                "IdSerie",
                "IdProyecto",
                "IdCliente",
                "IdProveedor",
                "NRegistro",
                "NFacturaPro",
                "FechaFacturaPro",
                "Subtotal",
                "IVA",
                "Base1",
                "Base2",
                "IVA1",
                "IVA2",
                "Total",
                "RutaArchivo",
                "IdFormaDePago",
                "IdCuenta1",
            ]
        )
        self.facturas_table.horizontalHeader().setStretchLastSection(True)
        self.facturas_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        facturas_layout.addWidget(self.facturas_table)

        facturas_group.setLayout(facturas_layout)
        main_layout.addWidget(facturas_group)

        # --- SECCIÓN ALBARANES ---
        albaranes_group = QGroupBox("ALBARANES")
        albaranes_group.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 16px; }"
        )
        albaranes_layout = QVBoxLayout()

        # Botón para cargar los datos de albaranespro
        buttons_albaranes_layout = QHBoxLayout()
        load_albaranes_btn = QPushButton("Cargar albaranes", self)
        load_albaranes_btn.clicked.connect(self.load_albaranes)
        load_albaranes_btn.setFixedWidth(200)
        buttons_albaranes_layout.addWidget(load_albaranes_btn)
        buttons_albaranes_layout.addStretch()  # Empuja el botón a la izquierda
        albaranes_layout.addLayout(buttons_albaranes_layout)

        # Tabla de albaranespro
        self.albaranes_table = QTableWidget(0, 17, self)
        self.albaranes_table.setHorizontalHeaderLabels(
            [
                "IdAlbaranPro",
                "IdProyecto",
                "IdCliente",
                "IdProveedor",
                "NRegistro",
                "NAlbaranPro",
                "Fecha",
                "Subtotal",
                "IVA",
                "Base1",
                "Base2",
                "IVA1",
                "IVA2",
                "TipoIVA1",
                "Total",
                "RutaArchivo",
                "IdFacturaPro",
            ]
        )
        self.albaranes_table.horizontalHeader().setStretchLastSection(True)
        self.albaranes_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        albaranes_layout.addWidget(self.albaranes_table)

        albaranes_group.setLayout(albaranes_layout)
        main_layout.addWidget(albaranes_group)

        # --- SECCIÓN INGRESOS ---
        ingresos_group = QGroupBox("INGRESOS")
        ingresos_group.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 16px; }"
        )
        ingresos_layout = QVBoxLayout()

        # Botón para cargar datos de ingresos
        buttons_ingresos_layout = QHBoxLayout()
        load_ingresos_btn = QPushButton("Cargar ingresos", self)
        load_ingresos_btn.clicked.connect(self.load_ingresos)
        load_ingresos_btn.setFixedWidth(200)
        buttons_ingresos_layout.addWidget(load_ingresos_btn)
        buttons_ingresos_layout.addStretch()  # Empuja el botón a la izquierda
        ingresos_layout.addLayout(buttons_ingresos_layout)

        # Tabla de ingresos
        self.ingresos_table = QTableWidget(0, 22, self)
        self.ingresos_table.setHorizontalHeaderLabels(
            [
                "IdFactura",
                "IdCliente",
                "NFactura",
                "FechaFactura",
                "FechaCobrada",
                "TotalTotal",
                "CertificacionAnterior",
                "Subtotal",
                "IVA",
                "Base1",
                "Base2",
                "IVA1",
                "IVA2",
                "TipoIVA1",
                "TipoIVA2",
                "Total",
                "IdProyecto",
                "IdFormaDePago",
                "Vencimientos",
                "Direccion",
                "Localidad",
                "DireccionTelefono",
            ]
        )
        self.ingresos_table.horizontalHeader().setStretchLastSection(True)
        self.ingresos_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        ingresos_layout.addWidget(self.ingresos_table)

        ingresos_group.setLayout(ingresos_layout)
        main_layout.addWidget(ingresos_group)

        # Añadir espacio al final para evitar que todo quede pegado abajo
        main_layout.addStretch()

    # MÉTODOS DE CARGA (se mantienen igual que en tu código original)
    def load_month_facturas(self):
        """Carga las facturas del mes actual ordenadas por fecha."""
        self.facturas_table.setRowCount(0)
        conexion, cursor = conexionDB()
        if not conexion:
            return

        try:
            query = """
            SELECT * FROM facturaspro
            WHERE MONTH(FechaFacturaPro) = MONTH(CURDATE())
            AND YEAR(FechaFacturaPro) = YEAR(CURDATE())
            ORDER BY FechaFacturaPro ASC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            for row_data in results:
                row = self.facturas_table.rowCount()
                self.facturas_table.insertRow(row)
                for col, value in enumerate(row_data):
                    self.facturas_table.setItem(row, col, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error al cargar las facturas de este mes: {e}")
        finally:
            cerrarConexion(conexion)

    def load_facturas(self):
        """Carga todos los datos desde la tabla facturaspro."""
        self.facturas_table.setRowCount(0)
        conexion, cursor = conexionDB()
        if not conexion:
            return

        try:
            query = (
                "SELECT IdFacturaPro, IdSerie, IdProyecto, IdCliente, IdProveedor,"
                "NRegistro, NFacturaPro, FechaFacturaPro, Subtotal, IVA,"
                "Base1, Base2, IVA1, IVA2, Total, RutaArchivo, IdFormaDePago, IdCuenta1 FROM facturaspro"
            )
            cursor.execute(query)
            results = cursor.fetchall()

            for row_data in results:
                row = self.facturas_table.rowCount()
                self.facturas_table.insertRow(row)
                for col, value in enumerate(row_data):
                    self.facturas_table.setItem(row, col, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error al cargar los datos de facturaspro: {e}")
        finally:
            cerrarConexion(conexion)

    def load_albaranes(self):
        """Carga todos los datos desde la tabla albaranespro."""
        self.albaranes_table.setRowCount(0)
        conexion, cursor = conexionDB()
        if not conexion:
            return

        try:
            query = (
                "SELECT IdAlbaranPro, IdProyecto, IdCliente, IdProveedor, NRegistro, NAlbaranPro, "
                "Fecha, Subtotal, IVA, Base1, Base2, IVA1, IVA2, TipoIVA1, Total, RutaArchivo, IdFacturaPro FROM albaranespro"
            )
            cursor.execute(query)
            results = cursor.fetchall()

            for row_data in results:
                row = self.albaranes_table.rowCount()
                self.albaranes_table.insertRow(row)
                for col, value in enumerate(row_data):
                    self.albaranes_table.setItem(row, col, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error al cargar los datos de albaranespro: {e}")
        finally:
            cerrarConexion(conexion)

    def load_ingresos(self):
        """Carga todos los datos desde la tabla ingresos."""
        self.ingresos_table.setRowCount(0)
        conexion, cursor = conexionDB()
        if not conexion:
            return

        try:
            query = """
            SELECT IdFactura, IdCliente, NFactura, FechaFactura, FechaCobrada,
            TotalTotal, CertificacionAnterior, Subtotal, IVA, Base1, Base2,
            IVA1, IVA2, TipoIVA1, TipoIVA2, Total, IdProyecto, IdFormaDePago,
            Vencimientos, Direccion, Localidad, DireccionTelefono 
            FROM facturas
            """
            cursor.execute(query)
            results = cursor.fetchall()

            for row_data in results:
                row = self.ingresos_table.rowCount()
                self.ingresos_table.insertRow(row)
                for col, value in enumerate(row_data):
                    self.ingresos_table.setItem(row, col, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error al cargar los datos de ingresos: {e}")
        finally:
            cerrarConexion(conexion)
