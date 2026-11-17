import pandas as pd
from pathlib import Path

# Ubicar el archivo CSV
ruta = Path(__file__).with_name("envios_adicionales.csv")

try:
    # Leer el archivo
    datos = pd.read_csv(ruta, encoding="utf-8")

    print("CONEXION CON ARCHIVO CSV EXITOSA")
    print("\nREGISTROS DE ENVIOS:")
    print(datos)

    print("\nTOTAL DE REGISTROS:", len(datos))
    print("\nCOLUMNAS DEL ARCHIVO:")
    print(datos.columns.tolist())

except FileNotFoundError:
    print("ERROR: No se encuentra envios_adicionales.csv")

except Exception as error:
    print("ERROR:", error)
