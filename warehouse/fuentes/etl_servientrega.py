import mysql.connector
import pandas as pd
import json
from pathlib import Path

# Carpeta donde se encuentran las fuentes
CARPETA = Path(__file__).resolve().parent

try:
    # ==================================
    # 1. EXTRACCION DE MARIA DB
    # ==================================

    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="dw_servientrega"
    )

    consulta = """
    SELECT
        h.id_envio,
        c.nombre AS cliente,
        t.fecha AS fecha_envio,
        u.ciudad_origen,
        u.ciudad_destino,
        s.tipo_servicio,
        e.estado_envio,
        h.tiempo_entrega_horas,
        h.cantidad_paquetes
    FROM hechos_envios h
    INNER JOIN dim_cliente c
        ON h.id_cliente = c.id_cliente
    INNER JOIN dim_tiempo t
        ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_ubicacion u
        ON h.id_ubicacion = u.id_ubicacion
    INNER JOIN dim_servicio s
        ON h.id_servicio = s.id_servicio
    INNER JOIN dim_estado e
        ON h.id_estado = e.id_estado
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(consulta)

    datos_bd = pd.DataFrame(cursor.fetchall())

    cursor.close()
    conexion.close()

    print("Extraccion MariaDB:", len(datos_bd), "registros")

    # ==================================
    # 2. EXTRACCION DEL ARCHIVO CSV
    # ==================================

    datos_csv = pd.read_csv(
        CARPETA / "envios_adicionales.csv"
    )

    print("Extraccion CSV:", len(datos_csv), "registros")

    # ==================================
    # 3. EXTRACCION DE LA API
    # ==================================

    with open(
        CARPETA / "municipios_dane.json",
        "r",
        encoding="utf-8"
    ) as archivo:
        datos_api = json.load(archivo)

    municipios = pd.DataFrame(datos_api)

    print("Extraccion API:", len(municipios), "registros")

    # ==================================
    # 4. TRANSFORMACION DE LOS DATOS
    # ==================================

    columnas_texto_csv = [
        "ciudad_origen",
        "ciudad_destino",
        "tipo_servicio",
        "estado"
    ]

    for columna in columnas_texto_csv:
        datos_csv[columna] = (
            datos_csv[columna].astype("string").str.strip().str.title()
        )

    datos_csv["fecha_envio"] = pd.to_datetime(
        datos_csv["fecha_envio"], errors="coerce"
    )

    datos_csv["peso_kg"] = pd.to_numeric(
        datos_csv["peso_kg"], errors="coerce"
    )

    if not datos_bd.empty:
        for columna in [
            "cliente", "ciudad_origen", "ciudad_destino",
            "tipo_servicio", "estado_envio"
        ]:
            datos_bd[columna] = (
                datos_bd[columna].astype("string").str.strip().str.title()
            )

        datos_bd["fecha_envio"] = pd.to_datetime(
            datos_bd["fecha_envio"], errors="coerce"
        )

    municipios["nom_mpio"] = (
        municipios["nom_mpio"].astype("string").str.strip().str.upper()
    )

    municipios["dpto"] = (
        municipios["dpto"].astype("string").str.strip().str.upper()
    )

    print("Transformacion de datos completada")

    # ==================================
    # 5. CARGA DE RESULTADOS
    # ==================================

    datos_bd.to_csv(
        CARPETA / "envios_bd_transformados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    datos_csv.to_csv(
        CARPETA / "envios_csv_transformados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    municipios.to_csv(
        CARPETA / "municipios_dane_transformados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Carga de archivos transformados exitosa")
    print("PROCESO ETL FINALIZADO")

except Exception as error:
    print("Error durante el proceso ETL:", error)

finally:
    if "conexion" in locals() and conexion.is_connected():
        conexion.close()
