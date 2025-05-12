import pandas as pd
from src.festivos import marcar_festivos


def test_marcar_festivos_sin_provincia():
    df_ventas = pd.DataFrame({
        'Fecha': [pd.Timestamp('2025-05-01')],
        'Tienda': ['Centro'],
        'Producto': ['Croissant'],
        'Cantidad vendida': [80]
    })
    df_tiendas = pd.DataFrame({
        'Tienda': ['Centro'],
        'Provincia': ['MD']
    })
    df_out = marcar_festivos(df_ventas, df_tiendas)
    assert 'EsFestivo' in df_out.columns
    assert isinstance(df_out['EsFestivo'].iloc[0], bool)