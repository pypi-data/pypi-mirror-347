import os
import pandas as pd
import pytest
from src.main import cargar_datos_ventas, cargar_tiendas, cargar_productos

@pytest.fixture(autouse=True)
def ensure_data_folder(tmp_path, monkeypatch):
    # Redirigir CARPETA_DATOS a un directorio temporal con CSV de ejemplo
    sample = tmp_path / "datos"
    sample.mkdir()
    # Crear archivos de ejemplo
    (sample / "ventas.csv").write_text(
        "Fecha,Tienda,Producto,Cantidad vendida\n"
        "2025-04-01,Centro,Croissant,80"
    )
    (sample / "tiendas.csv").write_text(
        "Tienda,Ciudad,Provincia\n"
        "Centro,Madrid,MD"
    )
    (sample / "productos.csv").write_text(
        "Producto,Categoría\n"
        "Croissant,Bollería"
    )
    # Forzar getcwd() al tmp_path para leer desde tests/datos
    monkeypatch.chdir(tmp_path)


def test_cargar_datos_ventas():
    df = cargar_datos_ventas()
    assert isinstance(df, pd.DataFrame)
    assert 'Fecha' in df.columns
    assert df['Cantidad vendida'].iloc[0] == 80


def test_cargar_tiendas():
    df = cargar_tiendas()
    assert 'Tienda' in df.columns
    assert df['Ciudad'].iloc[0] == 'Madrid'


def test_cargar_productos():
    df = cargar_productos()
    assert df['Producto'].iloc[0] == 'Croissant'