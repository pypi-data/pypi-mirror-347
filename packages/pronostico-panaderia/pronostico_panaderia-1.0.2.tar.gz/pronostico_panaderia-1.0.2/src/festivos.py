import pandas as pd
from holidays.countries.spain import Spain
from datetime import date
from typing import Dict, List, Optional, Tuple

def marcar_festivos(df_ventas: pd.DataFrame, df_tiendas: pd.DataFrame) -> pd.DataFrame:
    if 'Provincia' not in df_tiendas.columns:
        raise KeyError("La tabla 'tiendas.csv' debe incluir la columna 'Provincia' con el código de subdivisión válido.")
    df = df_ventas.merge(
        df_tiendas[['Tienda', 'Provincia']],
        on='Tienda',
        how='left'
    )
    provincias_unicas = df['Provincia'].dropna().unique()
    calendarios: Dict[str, Spain] = {}
    for prov in provincias_unicas:
        try:
            calendarios[prov] = Spain(subdiv=prov)
        except NotImplementedError:
            continue
    es_list: List[bool] = []
    nombre_list: List[str] = []
    def check(prov: Optional[str], fecha: date) -> Tuple[bool, str]:
        cal = calendarios.get(prov) if prov is not None else None
        if cal is None:
            return False, ''
        nombre = cal.get(fecha, None)
        if nombre is not None:
            return True, nombre
        return False, ''
    for _, row in df.iterrows():
        fecha = row['Fecha']
        if hasattr(fecha, 'date'):
            fecha = fecha.date()
        prov = row['Provincia']
        es, nombre = check(prov, fecha)
        es_list.append(es)
        nombre_list.append(nombre)
    df['EsFestivo'] = pd.Series(es_list, index=df.index, dtype=object)
    df['NombreFestivo'] = nombre_list
    return df
