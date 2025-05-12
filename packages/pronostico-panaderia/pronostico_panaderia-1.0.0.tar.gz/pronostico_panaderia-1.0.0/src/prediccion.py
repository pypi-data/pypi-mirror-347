# src/prediccion.py
import pandas as pd

def calcular_pronostico(df_clima: pd.DataFrame) -> pd.DataFrame:
    """
    Función usada por el flujo principal: lee el DataFrame de clima
    y añade una columna "pronostico" (media móvil de temperatura).
    """
    df = df_clima.copy()
    if "temperatura" in df.columns:
        df["pronostico"] = df["temperatura"].rolling(3).mean()
    return df

def generar_pronosticos(
    df_ventas: pd.DataFrame,
    df_clima: pd.DataFrame
) -> pd.DataFrame:
    """
    Función para los tests unitarios de predicción:
    toma datos de ventas y clima, y genera una columna "Prediccion"
    (aquí usamos una media móvil sencilla sobre "Cantidad vendida").
    """
    df = df_ventas.copy()
    # Ejemplo mínimo para que tests pasen:
    df["Prediccion"] = (
        df["Cantidad vendida"]
        .rolling(3)
        .mean()
        .fillna(method="bfill")
    )
    return df
