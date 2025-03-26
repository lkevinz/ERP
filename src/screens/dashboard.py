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

       