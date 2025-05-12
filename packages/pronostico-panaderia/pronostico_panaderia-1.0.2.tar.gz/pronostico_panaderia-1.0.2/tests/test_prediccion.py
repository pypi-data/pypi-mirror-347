import pandas as pd
from src.prediccion import generar_pronosticos


def test_generar_pronosticos_minimos():
    ventas = pd.DataFrame({
        'Fecha': pd.to_datetime(['2025-04-01'] * 5),
        'Tienda': ['Centro'] * 5,
        'Producto': ['Croissant'] * 5,
        'Cantidad vendida': [80, 82, 78, 85, 83],
        'EsFestivo': [False] * 5
    })
    clima = pd.DataFrame({
        'Fecha': pd.to_datetime(['2025-04-01'] * 5),
        'Tienda': ['Centro'] * 5,
        'Temp (°C)': [10, 10, 10, 10, 10],
        'Humedad (%)': [50, 50, 50, 50, 50],
        'Lluvia (mm)': [0, 0, 0, 0, 0]
    })
    df_pred = generar_pronosticos(ventas, clima)
    assert not df_pred.empty
    assert 'Prediccion' in df_pred.columns
