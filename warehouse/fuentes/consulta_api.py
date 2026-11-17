import requests
import json
from pathlib import Path

url = "https://www.datos.gov.co/resource/gdxc-w37w.json"

try:
    respuesta = requests.get(
        url,
        params={"$limit": 1500},
        timeout=30
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    print("CONEXION CON API EXITOSA")
    print("Total de registros:", len(datos))

    print("\nMUNICIPIOS CONSULTADOS:")

    for municipio in datos:
        print(
            municipio.get("nom_mpio"),
            "-",
            municipio.get("dpto")
        )

    # Guardar respuesta para utilizarla posteriormente
    ruta = Path(__file__).with_name("municipios_dane.json")

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    print("\nArchivo municipios_dane.json guardado correctamente")

except requests.exceptions.RequestException as error:
    print("Error al consultar la API:", error)

except ValueError:
    print("La respuesta recibida no tiene formato JSON válido")
