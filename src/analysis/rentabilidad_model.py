# src/analysis/rentabilidad_model.py

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from database.connectionSQL import conexionDB, cerrarConexion
from analysis.rentabilidad_calculos import calcular_rentabilidad


class RentabilidadNN(nn.Module):
    def __init__(self, input_dim):
        super(RentabilidadNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)  # Salida: rentabilidad en euros

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x


def entrenar_modelo_neuronal(epochs=50, batch_size=32, learning_rate=0.001):
    """
    Entrena una red neuronal (MLP) con PyTorch para predecir la rentabilidad en euros.

    Parámetros:
      - epochs: número de épocas de entrenamiento.
      - batch_size: tamaño del lote (batch) para cada iteración.
      - learning_rate: tasa de aprendizaje para el optimizador.

    Retorna:
      - model: el modelo PyTorch entrenado.
      - scaler: objeto StandardScaler usado para normalizar las características.
      - train_losses: lista con la pérdida promedio de cada época.
    """
    miConexion, cur = conexionDB()
    if not miConexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        # 1. Extraer datos desde las 5 tablas
        df_proyectos = pd.read_sql("SELECT * FROM proyectos;", miConexion)
        df_clientes = pd.read_sql("SELECT * FROM clientes;", miConexion)
        df_facturas = pd.read_sql("SELECT * FROM facturaspro;", miConexion)
        df_albaranes = pd.read_sql("SELECT * FROM albaranespro;", miConexion)
        df_partes = pd.read_sql("SELECT * FROM partedetrabajo;", miConexion)

        # 2. Calcular la rentabilidad uniendo las tablas
        df = calcular_rentabilidad(
            df_proyectos, df_clientes, df_facturas, df_albaranes, df_partes
        )

        # 3. Definir características (features) y objetivo (target)
        # Se asumen las siguientes columnas:
        #   - total_facturas, total_albaranes, total_mano_obra y Ingresos
        # El objetivo es predecir "rentabilidad_euros"
        features = ["total_facturas", "total_albaranes", "total_mano_obra", "Ingresos"]
        target = "rentabilidad_euros"

        # Asegurarse de eliminar filas con valores faltantes
        df_modelo = df.dropna(subset=features + [target])
        X = df_modelo[features].values.astype(np.float32)
        y = df_modelo[target].values.astype(np.float32).reshape(-1, 1)

        # 4. Escalar las características
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 5. Dividir en conjuntos de entrenamiento y test
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        # Convertir a tensores de PyTorch
        X_train = torch.tensor(X_train)
        y_train = torch.tensor(y_train)
        X_test = torch.tensor(X_test)
        y_test = torch.tensor(y_test)

        input_dim = X_train.shape[1]
        model = RentabilidadNN(input_dim)

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        train_losses = []
        for epoch in range(epochs):
            model.train()
            permutation = torch.randperm(X_train.size()[0])
            epoch_loss = 0
            for i in range(0, X_train.size()[0], batch_size):
                indices = permutation[i : i + batch_size]
                batch_x, batch_y = X_train[indices], y_train[indices]

                optimizer.zero_grad()
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            avg_loss = epoch_loss / (X_train.size()[0] / batch_size)
            train_losses.append(avg_loss)
            print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")

        # Evaluar en el conjunto de test
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test)
            test_loss = criterion(test_outputs, y_test)
        print(f"Test Loss: {test_loss.item():.4f}")

        return model, scaler, train_losses

    except Exception as e:
        raise Exception(f"Error en el modelo neuronal con PyTorch: {e}")

    finally:
        cerrarConexion(miConexion)


def predecir_rentabilidad_neuronal(model, scaler, df_nuevos):
    """
    Predice la rentabilidad en euros para nuevos proyectos usando el modelo entrenado.

    df_nuevos: DataFrame con las columnas [total_facturas, total_albaranes, total_mano_obra, Ingresos]
    Retorna df_nuevos con una columna 'rentabilidad_euros_pred'
    """
    required_cols = ["total_facturas", "total_albaranes", "total_mano_obra", "Ingresos"]
    for col in required_cols:
        if col not in df_nuevos.columns:
            df_nuevos[col] = 0

    X_new = df_nuevos[required_cols].values.astype(np.float32)
    X_new_scaled = scaler.transform(X_new)
    X_new_tensor = torch.tensor(X_new_scaled)

    model.eval()
    with torch.no_grad():
        predictions = model(X_new_tensor).numpy().flatten()
    df_nuevos["rentabilidad_euros_pred"] = predictions
    return df_nuevos
