"""Constante del proyecto: semilla y rutas relativas a la raiz del repositorio"""

from pathlib import Path

# Semilla única para toda función con azar (partición, CV, modelos, remuestreo).
SEMILLA = 42

# Raíz del proyecto calculada desde la ubicación de este archivo. 
# config.py -> mice_supervisado/ (0) -> src/ (1) -> raíz (2)
RAIZ = Path(__file__).resolve().parents[2]

RUTA_CRUDOS = RAIZ / "datos" / "crudos"
RUTA_PROCESADOS = RAIZ / "datos" / "procesados"
RUTA_INFORMES = RAIZ / "informes"

ARCHIVO_CRUDO = RUTA_CRUDOS / "Data_Cortex_Nuclear.xls"
ARCHIVO_DEPURADO = RUTA_PROCESADOS / "mice_depurado.parquet"

# Carpeta de informes asociada a cada actividad
CARPETAS_ACTIVIDAD = {
    1: "01_eda",
    2: "02_regresion",
    3: "03_clasificacion",
    4: "04_integrador",
}


def ruta_figuras(actividad: int) -> Path:
    """Devuelve la carpeta de figuras de una actividad y la crea si no existe."""
    ruta = RUTA_INFORMES / CARPETAS_ACTIVIDAD[actividad] / "figuras"
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta 