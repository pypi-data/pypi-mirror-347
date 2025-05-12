# src/clima.py

import requests
import pandas as pd

def obtener_clima() -> pd.DataFrame:
    # …tu lógica de requests y DataFrame…
    datos = requests.get("https://api.clima.example/30dias").json()
    return pd.DataFrame(datos)
