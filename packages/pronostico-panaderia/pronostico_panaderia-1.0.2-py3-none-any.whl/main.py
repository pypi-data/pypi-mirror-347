# src/main.py

import os
import pandas as pd
import logging
from logging import Handler, StreamHandler
from datetime import date

from src.clima import obtener_clima
from src.prediccion import calcular_pronostico
from src.excel import guardar_pronostico

def cargar_datos_ventas() -> pd.DataFrame:
    path = os.path.join(os.getcwd(), "datos", "ventas.csv")
    return pd.read_csv(path)

def cargar_tiendas() -> pd.DataFrame:
    path = os.path.join(os.getcwd(), "datos", "tiendas.csv")
    return pd.read_csv(path)

def cargar_productos() -> pd.DataFrame:
    path = os.path.join(os.getcwd(), "datos", "productos.csv")
    return pd.read_csv(path)

def configure_logging() -> None:
    handlers: list[Handler] = [StreamHandler()]
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
        level=logging.INFO,
        handlers=handlers
    )

def main() -> None:
    configure_logging()
    log = logging.getLogger(__name__)
    log.info("🔄 Iniciando pronóstico de panadería")

    hoy = date.today()
    try:
        log.info("📥 Obteniendo datos de clima…")
        datos_clima = obtener_clima()

        log.info("⚙️ Calculando pronóstico…")
        df_pron = calcular_pronostico(datos_clima)

        salida = f"output/pronostico_{hoy}.xlsx"
        log.info(f"💾 Guardando en {salida}…")
        guardar_pronostico(df_pron, salida)

        log.info("✅ Pronóstico listo")
    except Exception:
        log.exception("❌ Error en el flujo principal")

if __name__ == "__main__":
    main()
