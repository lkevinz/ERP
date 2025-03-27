# src/reports/rentabilidad_informe.py

import os
import pandas as pd
from database.connectionSQL import conexionDB, cerrarConexion
from analysis.rentabilidad_calculos import calcular_rentabilidad


def generar_informe_rentabilidad():
    """
    Conecta a la base de datos, extrae las 5 tablas principales y genera un informe
    de rentabilidad en formato Excel en la carpeta Descargas del usuario.
    """
    miConexion, cur = conexionDB()
    if not miConexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        # 1. Extraer datos de las tablas
        df_proyectos = pd.read_sql("SELECT * FROM proyectos;", miConexion)
        df_clientes = pd.read_sql("SELECT * FROM clientes;", miConexion)
        df_facturas = pd.read_sql("SELECT * FROM facturaspro;", miConexion)
        df_albaranes = pd.read_sql("SELECT * FROM albaranespro;", miConexion)
        df_partes = pd.read_sql("SELECT * FROM partedetrabajo;", miConexion)

        # 2. Calcular la rentabilidad
        df_resultado = calcular_rentabilidad(
            df_proyectos, df_clientes, df_facturas, df_albaranes, df_partes
        )

        # 3. Guardar en carpeta Descargas
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(download_path, exist_ok=True)
        archivo_salida = os.path.join(download_path, "informe_rentabilidad.xlsx")

        df_resultado.to_excel(archivo_salida, index=False)
        print(f"Informe de rentabilidad generado en: {archivo_salida}")

    except Exception as e:
        raise Exception(f"Error al generar el informe: {e}")
    finally:
        cerrarConexion(miConexion)
