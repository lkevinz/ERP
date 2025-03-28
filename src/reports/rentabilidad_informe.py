import os
import pandas as pd
from database.connectionSQL import conexionDB, cerrarConexion


def generar_informe_rentabilidad():
    """
    Genera un informe de rentabilidad que incluye las columnas solicitadas:
      ID Proyecto, Nproyecto, Nombre Proyecto, IdCliente, Nombre Cliente, Apellido Cliente,
      Mano de obra, Facturas Proveedores Base 1..4, Total Facturas Proveedores,
      Albaranes Proveedores, Facturas + Albaranes, Ingresos, Rentabilidad €,
      Rentabilidad % s/ingresos, Rentabilidad % s/gastos.

    Ajusta la lógica de 'Ingresos' y 'Mano de Obra' a partir de partedetrabajo,
    ya que no existe una columna 'Ingresos' en proyectos.
    """

    miConexion, cur = conexionDB()
    if not miConexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        # 1. Cargar los datos de proyectos (sin 'Ingresos')
        df_proyectos = pd.read_sql(
            """
            SELECT
                IdProyecto,
                NProyecto,
                NombreObra AS NombreProyecto,
                IdCliente
            FROM proyectos;
            """,
            miConexion,
        )

        # 2. Cargar los datos de clientes (para NombreCliente y ApellidoCliente)
        df_clientes = pd.read_sql(
            """
            SELECT
                IdCliente,
                Nombre AS NombreCliente,
                Apellidos AS ApellidoCliente
            FROM clientes;
            """,
            miConexion,
        )

        # 3. Obtener la mano de obra y los ingresos (o facturación) de partedetrabajo
        #    Supongamos que:
        #      - 'SubtotalMOCoste' = coste de mano de obra
        #      - 'SubtotalClienteConMO' = lo que se le cobra al cliente (ingresos)
        #    Ajusta si tu columna real es distinta.
        df_partes = pd.read_sql(
            """
            SELECT
                IdProyecto,
                SUM(SubtotalMOCoste) AS ManoDeObra,
                SUM(SubtotalClienteConMO) AS Ingresos
            FROM partedetrabajo
            GROUP BY IdProyecto;
            """,
            miConexion,
        )

        # 4. FacturasPro (proveedores), sumando Base1..4 => "Facturas Proveedores"
        df_facturas = pd.read_sql(
            """
            SELECT
                IdProyecto,
                SUM(Base1) AS FacturasProvBase1,
                SUM(Base2) AS FacturasProvBase2,
                SUM(Base3) AS FacturasProvBase3,
                SUM(Base4) AS FacturasProvBase4
            FROM facturaspro
            GROUP BY IdProyecto;
            """,
            miConexion,
        )

        # 5. AlbaranesPro (proveedores), sumando Base1..4 => "Albaranes Proveedores"
        df_albaranes = pd.read_sql(
            """
            SELECT
                IdProyecto,
                SUM(Base1 + Base2 + Base3 + Base4) AS AlbaranesProveedores
            FROM albaranespro
            GROUP BY IdProyecto;
            """,
            miConexion,
        )

        # -----------------------
        # UNIONES DE DATAFRAMES
        # -----------------------

        # a) Unir proyectos con clientes (por IdCliente)
        df_merged = pd.merge(df_proyectos, df_clientes, on="IdCliente", how="left")

        # b) Unir partedetrabajo (Mano de Obra e Ingresos)
        df_merged = pd.merge(df_merged, df_partes, on="IdProyecto", how="left")

        # c) Unir facturas pro
        df_merged = pd.merge(df_merged, df_facturas, on="IdProyecto", how="left")

        # d) Unir albaranes pro
        df_merged = pd.merge(df_merged, df_albaranes, on="IdProyecto", how="left")

        # Rellenar nulos con 0 en las columnas numéricas
        numeric_cols = [
            "ManoDeObra",
            "Ingresos",
            "FacturasProvBase1",
            "FacturasProvBase2",
            "FacturasProvBase3",
            "FacturasProvBase4",
            "AlbaranesProveedores",
        ]
        for col in numeric_cols:
            df_merged[col] = df_merged[col].fillna(0)

        # ---------------------------
        # CALCULOS DE RENTABILIDAD
        # ---------------------------

        # 1. Total Facturas Proveedores
        df_merged["TotalFacturasProveedores"] = (
            df_merged["FacturasProvBase1"]
            + df_merged["FacturasProvBase2"]
            + df_merged["FacturasProvBase3"]
            + df_merged["FacturasProvBase4"]
        )

        # 2. Facturas + Albaranes
        df_merged["FacturasMasAlbaranes"] = (
            df_merged["TotalFacturasProveedores"] + df_merged["AlbaranesProveedores"]
        )

        # 3. Rentabilidad € = Ingresos - (ManoDeObra + Facturas + Albaranes)
        df_merged["RentabilidadEuros"] = (
            df_merged["Ingresos"]
            - df_merged["ManoDeObra"]
            - df_merged["FacturasMasAlbaranes"]
        )

        # 4. Rentabilidad % s/ingresos
        df_merged["RentabilidadPctIngresos"] = df_merged.apply(
            lambda row: (
                (row["RentabilidadEuros"] / row["Ingresos"] * 100)
                if row["Ingresos"] != 0
                else 0
            ),
            axis=1,
        )

        # 5. Rentabilidad % s/gastos
        #    Gastos totales = ManoDeObra + Facturas + Albaranes
        df_merged["GastosTotales"] = (
            df_merged["ManoDeObra"] + df_merged["FacturasMasAlbaranes"]
        )
        df_merged["RentabilidadPctGastos"] = df_merged.apply(
            lambda row: (
                (row["RentabilidadEuros"] / row["GastosTotales"] * 100)
                if row["GastosTotales"] != 0
                else 0
            ),
            axis=1,
        )

        # ------------------------------
        # SELECCIONAR COLUMNAS FINALES
        # ------------------------------
        df_informe = df_merged[
            [
                "IdProyecto",
                "NProyecto",
                "NombreProyecto",
                "IdCliente",
                "NombreCliente",
                "ApellidoCliente",
                "ManoDeObra",
                "FacturasProvBase1",
                "FacturasProvBase2",
                "FacturasProvBase3",
                "FacturasProvBase4",
                "TotalFacturasProveedores",
                "AlbaranesProveedores",
                "FacturasMasAlbaranes",
                "Ingresos",
                "RentabilidadEuros",
                "RentabilidadPctIngresos",
                "RentabilidadPctGastos",
            ]
        ].copy()

        # Renombrar columnas para el informe
        df_informe.rename(
            columns={
                "ManoDeObra": "Mano de obra",
                "FacturasProvBase1": "Facturas Proveedores Base 1",
                "FacturasProvBase2": "Facturas Proveedores Base 2",
                "FacturasProvBase3": "Facturas Proveedores Base 3",
                "FacturasProvBase4": "Facturas Proveedores Base 4",
                "TotalFacturasProveedores": "Total Facturas Proveedores",
                "AlbaranesProveedores": "Albaranes Proveedores",
                "FacturasMasAlbaranes": "Facturas + Albaranes",
                "RentabilidadEuros": "Rentabilidad €",
                "RentabilidadPctIngresos": "Rentabilidad % s/ingresos",
                "RentabilidadPctGastos": "Rentabilidad % s/gastos",
            },
            inplace=True,
        )

        # ----------------------------
        # GUARDAR EN EXCEL (Descargas)
        # ----------------------------
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(download_path, exist_ok=True)
        archivo_salida = os.path.join(download_path, "Informe_Rentabilidad.xlsx")
        df_informe.to_excel(archivo_salida, index=False)

        print(f"Informe de rentabilidad generado: {archivo_salida}")

    except Exception as e:
        raise Exception(f"Error al generar el informe: {e}")
    finally:
        cerrarConexion(miConexion)
