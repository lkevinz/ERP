# src/analysis/rentabilidad_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from database.connectionSQL import conexionDB, cerrarConexion
from analysis.rentabilidad_calculos import calcular_rentabilidad


def entrenar_modelo():
    """
    Ejemplo de entrenamiento de un modelo de Machine Learning (regresión lineal)
    para predecir la rentabilidad en euros a partir de los datos históricos.

    Retorna:
      - modelo (el modelo entrenado)
      - score (R^2 del modelo en el test set)
    """
    miConexion, cur = conexionDB()
    if not miConexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        # 1. Cargar datos históricos
        df_proyectos = pd.read_sql("SELECT * FROM proyectos;", miConexion)
        df_clientes = pd.read_sql("SELECT * FROM clientes;", miConexion)
        df_facturas = pd.read_sql("SELECT * FROM facturaspro;", miConexion)
        df_albaranes = pd.read_sql("SELECT * FROM albaranespro;", miConexion)
        df_partes = pd.read_sql("SELECT * FROM partedetrabajo;", miConexion)

        df = calcular_rentabilidad(
            df_proyectos, df_clientes, df_facturas, df_albaranes, df_partes
        )

        # 2. Preparamos los datos (features y target)
        # Supongamos que queremos predecir "rentabilidad_euros"
        # Usamos como features: total_facturas, total_albaranes, total_mano_obra, Ingresos, etc.
        features = ["total_facturas", "total_albaranes", "total_mano_obra", "Ingresos"]
        target = "rentabilidad_euros"

        # Quitamos filas que tengan NaN en esas columnas
        df_modelo = df.dropna(subset=features + [target])

        X = df_modelo[features]
        y = df_modelo[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 3. Entrenamos un modelo de regresión lineal
        modelo = LinearRegression()
        modelo.fit(X_train, y_train)

        # 4. Score (R^2)
        score = modelo.score(X_test, y_test)
        print(f"Score del modelo (R^2): {score:.2f}")

        return modelo, score

    except Exception as e:
        raise Exception(f"Error en el modelo: {e}")

    finally:
        cerrarConexion(miConexion)


def predecir_rentabilidad(modelo, df_nuevos):
    """
    Ejemplo de función para predecir la rentabilidad en nuevos proyectos,
    usando el modelo ya entrenado.

    df_nuevos: DataFrame con columnas [total_facturas, total_albaranes, total_mano_obra, Ingresos]
    Retorna df_nuevos con columna 'rentabilidad_euros_pred'
    """
    df_nuevos = df_nuevos.copy()
    required_cols = ["total_facturas", "total_albaranes", "total_mano_obra", "Ingresos"]
    for col in required_cols:
        if col not in df_nuevos.columns:
            df_nuevos[col] = 0

    df_nuevos["rentabilidad_euros_pred"] = modelo.predict(df_nuevos[required_cols])
    return df_nuevos
