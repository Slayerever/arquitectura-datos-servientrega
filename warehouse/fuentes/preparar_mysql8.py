import mysql.connector
import requests
from getpass import getpass

try:
    clave = getpass("Contrasena de MySQL Server 8.0: ")

    # Consultar municipios del DANE
    url = "https://www.datos.gov.co/resource/gdxc-w37w.json"

    respuesta = requests.get(
        url,
        params={"$limit": 1500},
        timeout=60
    )
    respuesta.raise_for_status()
    municipios = respuesta.json()

    # Conectar al segundo servidor
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password=clave
    )

    cursor = conexion.cursor()

    # Crear base de datos
    cursor.execute("""
        CREATE DATABASE IF NOT EXISTS geografia_servientrega
        CHARACTER SET utf8mb4
    """)

    cursor.close()
    conexion.close()

    # Conectar a la nueva base
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password=clave,
        database="geografia_servientrega"
    )

    cursor = conexion.cursor()

    # Crear tabla geográfica
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS municipios_dane (
            cod_mpio VARCHAR(10) PRIMARY KEY,
            cod_dpto VARCHAR(10),
            dpto VARCHAR(100),
            nom_mpio VARCHAR(150),
            tipo_municipio VARCHAR(50),
            longitud DECIMAL(12,8),
            latitud DECIMAL(12,8)
        ) ENGINE=InnoDB
    """)

    # Preparar registros
    sql = """
        INSERT INTO municipios_dane
        (cod_mpio, cod_dpto, dpto, nom_mpio,
         tipo_municipio, longitud, latitud)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        nom_mpio = VALUES(nom_mpio),
        dpto = VALUES(dpto),
        longitud = VALUES(longitud),
        latitud = VALUES(latitud)
    """

    registros = []

    for m in municipios:
        registros.append((
            str(m.get("cod_mpio", "")),
            str(m.get("cod_dpto", "")),
            m.get("dpto"),
            m.get("nom_mpio"),
            m.get("tipo_municipio"),
        float(str(m.get("longitud")).replace(",", ".")),
float(str(m.get("latitud")).replace(",", "."))
        ))

    cursor.executemany(sql, registros)
    conexion.commit()

    cursor.execute("SELECT COUNT(*) FROM municipios_dane")
    total = cursor.fetchone()[0]

    print("CONEXION CON SEGUNDO SERVIDOR EXITOSA")
    print("Municipios recibidos:", len(municipios))
    print("Municipios almacenados:", total)
    print("Base: geografia_servientrega")

    cursor.close()
    conexion.close()

except Exception as error:
    print("ERROR:", error)
