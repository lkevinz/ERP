# src/analysis/rentabilidad_calculos.py

import pandas as pd


def calcular_rentabilidad(
    df_proyectos: pd.DataFrame,
    df_clientes: pd.DataFrame,
    df_facturas: pd.DataFrame,
    df_albaranes: pd.DataFrame,
    df_partes: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula la rentabilidad de cada proyecto, uniendo:
      - proyectos (PK: IdProyecto, FK: IdCliente)
      - clientes (PK: IdCliente)
      - facturaspro (PK: IdFacturaPro, FK: IdProyecto)
      - albaranespro (PK: IdAlbaranPro, FK: IdProyecto)
      - partedetrabajo (PK: IdParteDeTrabajo, FK: IdProyecto)

    Se asume que en 'proyectos' existe alguna columna 'Ingresos' (o define la tuya).
    Si no existe, podrías asignar 0 o usar otra lógica de ingresos.

    Columnas usadas como ejemplo:
      - facturaspro: 'Total' (gasto en facturas)
      - albaranespro: 'Total' (o 'TotalTotal') como gasto de albarán
      - partedetrabajo: 'SubtotalMOCoste' (coste de mano de obra) (ajusta según tu BD)
    """

    # 1. Unir proyectos con clientes (IdCliente)
    df_merged = pd.merge(df_proyectos, df_clientes, on="IdCliente", how="left")

    # 2. Agregar gastos de facturas por proyecto (ejemplo: sumar 'Total')
    if "Total" in df_facturas.columns:
        df_fact_agg = df_facturas.groupby("IdProyecto", as_index=False)["Total"].sum()
        df_fact_agg.rename(columns={"Total": "total_facturas"}, inplace=True)
    else:
        # Ajusta si tu columna se llama distinto
        df_fact_agg = df_facturas.groupby("IdProyecto", as_index=False).size()
        df_fact_agg.rename(columns={"size": "total_facturas"}, inplace=True)

    # 3. Agregar gastos de albaranes por proyecto (ejemplo: 'Total')
    if "Total" in df_albaranes.columns:
        df_alb_agg = df_albaranes.groupby("IdProyecto", as_index=False)["Total"].sum()
        df_alb_agg.rename(columns={"Total": "total_albaranes"}, inplace=True)
    elif "TotalTotal" in df_albaranes.columns:
        df_alb_agg = df_albaranes.groupby("IdProyecto", as_index=False)[
            "TotalTotal"
        ].sum()
        df_alb_agg.rename(columns={"TotalTotal": "total_albaranes"}, inplace=True)
    else:
        # Caso de fallback
        df_alb_agg = df_albaranes.groupby("IdProyecto", as_index=False).size()
        df_alb_agg.rename(columns={"size": "total_albaranes"}, inplace=True)

    # 4. Agregar coste de partes de trabajo (ejemplo: 'SubtotalMOCoste')
    if "SubtotalMOCoste" in df_partes.columns:
        df_par_agg = df_partes.groupby("IdProyecto", as_index=False)[
            "SubtotalMOCoste"
        ].sum()
        df_par_agg.rename(columns={"SubtotalMOCoste": "total_mano_obra"}, inplace=True)
    else:
        # Ajusta si tu columna se llama distinto
        df_par_agg = df_partes.groupby("IdProyecto", as_index=False).size()
        df_par_agg.rename(columns={"size": "total_mano_obra"}, inplace=True)

    # 5. Unir agregados al df_merged
    df_merged = pd.merge(df_merged, df_fact_agg, on="IdProyecto", how="left")
    df_merged = pd.merge(df_merged, df_alb_agg, on="IdProyecto", how="left")
    df_merged = pd.merge(df_merged, df_par_agg, on="IdProyecto", how="left")

    # 6. Rellenar NaN con 0
    df_merged["total_facturas"] = df_merged["total_facturas"].fillna(0)
    df_merged["total_albaranes"] = df_merged["total_albaranes"].fillna(0)
    df_merged["total_mano_obra"] = df_merged["total_mano_obra"].fillna(0)

    # 7. Calcular gastos totales
    df_merged["gastos_totales"] = (
        df_merged["total_facturas"]
        + df_merged["total_albaranes"]
        + df_merged["total_mano_obra"]
    )

    # 8. Verificar columna de Ingresos (si no existe, crearla en 0)
    if "Ingresos" not in df_merged.columns:
        df_merged["Ingresos"] = 0  # Ajusta según tu caso real

    # 9. Rentabilidad
    df_merged["rentabilidad_euros"] = (
        df_merged["Ingresos"] - df_merged["gastos_totales"]
    )

    def calc_pct(row):
        if row["Ingresos"] == 0:
            return 0
        return (row["rentabilidad_euros"] / row["Ingresos"]) * 100

    df_merged["rentabilidad_%_ingresos"] = df_merged.apply(calc_pct, axis=1)

    return df_merged
