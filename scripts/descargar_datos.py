"""Descarga el dataset Mice Protein Expression (UCI, id 342) en datos/crudos/."""

import io
import urllib.request
import zipfile

from mice_supervisado.config import ARCHIVO_CRUDO, RUTA_CRUDOS

URL = "https://archive.ics.uci.edu/static/public/342/mice+protein+expression.zip"


def main() -> None:
    if ARCHIVO_CRUDO.exists():
        print(f"Ya existe: {ARCHIVO_CRUDO}")
        return

    RUTA_CRUDOS.mkdir(parents=True, exist_ok=True)
    print(f"Descargando {URL} ...")
    with urllib.request.urlopen(URL) as respuesta:
        contenido = respuesta.read()

    # El zip se procesa en memoria, sin guardarlo en disco.
    with zipfile.ZipFile(io.BytesIO(contenido)) as comprimido:
        print("Archivos en el zip:", comprimido.namelist())
        comprimido.extractall(RUTA_CRUDOS)

    if ARCHIVO_CRUDO.exists():
        print(f"Listo: {ARCHIVO_CRUDO}")
    else:
        print("El zip no trae Data_Cortex_Nuclear.xls con ese nombre; revisar datos/crudos/.")


if __name__ == "__main__":
    main()