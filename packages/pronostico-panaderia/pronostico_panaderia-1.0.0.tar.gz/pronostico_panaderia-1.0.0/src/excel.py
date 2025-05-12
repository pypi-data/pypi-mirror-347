# src/excel.py

import pandas as pd

def guardar_pronostico(df: pd.DataFrame, ruta: str) -> None:
    # …tu lógica para exportar con openpyxl…
    df.to_excel(ruta, index=False)
