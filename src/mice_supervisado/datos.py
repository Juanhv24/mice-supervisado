"""Carga de datos crudos y depurados"""

import pandas as pd

from mice_supervisado.config import ARCHIVO_CRUDO, ARCHIVO_DEPURADO

def cargar_crudos () -> pd.DataFrame:
    """Lee el archivo original de UCI sin ninguna transformación."""
    if not ARCHIVO_CRUDO.exists():
        raise FileExistsError(
            f"No se encontró {ARCHIVO_CRUDO.name}. "
            "Ejecutar primero: uv run python scripts/descargar_datos.py"
        )
    return pd.read_excel(ARCHIVO_CRUDO)

def cargar_depurados() -> pd.DataFrame:
    """Lee la base depurada que produce el notebook de la Actividad 1."""
    if not ARCHIVO_DEPURADO.exists():
        raise FileNotFoundError(
            f"No se encontró {ARCHIVO_DEPURADO.name}. "
            "Se genera al final de notebooks/01_eda.ipynb"
        )
    return pd.read_parquet(ARCHIVO_DEPURADO)