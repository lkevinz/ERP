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
from screens.ConexionSQL import conexionDB, cerrarConexion


class FinanceScreen(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        # Título
        title_label = QLabel("FINANZAS", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Subtítulo
        label2 = QLabel("Facturas", self)
        main_layout.addWidget(label2)

        # Botón para ver facturas de este mes
        top_layout = QHBoxLayout()
        view_month_btn = QPushButton("Facturas de este mes", self)
        view_month_btn.clicked.connect(self.load_current_month_invoices)
        top_layout.addWidget(view_month_btn)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        # Tabla de facturaspro
        self.facturas_table = QTableWidget(0, 18, self)
        self.facturas_table.setHorizontalHeaderLabels(
            [
                "IdFacturaPro", "IdSerie", "IdProyecto", "IdCliente", "IdProveedor",
                "NRegistro", "NFacturaPro", "FechaFacturaPro", "Subtotal", "IVA",
                "Base1", "Base2", "IVA1", "IVA2", "Total", "RutaArchivo",
                "IdFormaDePago", "IdCuenta1"
            ]
        )
        main_layout.addWidget(self.facturas_table)

        # Botón para cargar todas las facturas
        load_facturas_btn = QPushButton("Cargar datos de facturaspro", self)
        load_facturas_btn.clicked.connect(self.load_finance_data)
        main_layout.addWidget(load_facturas_btn)

        # Subtítulo Albaranes
        label3 = QLabel("Albaranes", self)
        main_layout.addWidget(label3)
        
        # Tabla de albaranespro
        self.albaranes_table = QTableWidget(0, 17, self)
        self.albaranes_table.setHorizontalHeaderLabels(
            [
                "IdAlbaranPro", "IdProyecto", "IdCliente", "IdProveedor",
                "NRegistro", "NAlbaranPro", "Fecha", "Subtotal", "IVA",
                "Base1", "Base2", "IVA1", "IVA2", "TipoIVA1", "Total",
                "RutaArchivo", "IdFacturaPro"
            ]
        )
        main_layout.addWidget(self.albaranes_table)

        # Botón para cargar los datos de albaranespro
        load_albaranes_btn = QPushButton("Cargar datos de albaranespro", self)
        load_albaranes_btn.clicked.connect(self.load_albaranes_data)
        main_layout.addWidget(load_albaranes_btn)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def load_finance_data(self):
        """Carga todos los datos desde la tabla facturaspro."""
        self.facturas_table.setRowCount(0)
        conexion, cursor = conexionDB()
        if not conexion:
            return

        try:
            query = "SELECT IdFacturaPro, IdSerie, IdProyecto, IdCliente, IdProveedor," \
            "NRegistro, NFacturaPro, FechaFacturaPro, Subtotal, IVA," \
            "Base1, Base2, IVA1, IVA2, Total, RutaArchivo, IdFormaDePago, IdCuenta1 FROM facturaspro"
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

    def load_albaranes_data(self):
        """Carga todos los datos desde la tabla albaranespro."""
        self.albaranes_table.setRowCount(0)
        conexion, cursor = conexionDB()
        if not conexion:
            return

        try:
            query = "SELECT IdAlbaranPro, IdProyecto, IdCliente, IdProveedor, NRegistro, NAlbaranPro, " \
            "Fecha, Subtotal, IVA, Base1, Base2, IVA1, IVA2, TipoIVA1, Total, RutaArchivo, IdFacturaPro FROM albaranespro"
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

    def load_current_month_invoices(self):
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
