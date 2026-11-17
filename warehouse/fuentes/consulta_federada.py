
import pandas as pd
import unicodedata
import re
from getpass import getpass
from sqlalchemy import create_engine, URL


# Funcion para normalizar nombres de ciudades
def normalizar(valor):
    if pd.isna(valor):
        return ""

    texto = unicodedata.normalize(
        "NFKD", str(valor)
    ).encode("ascii", "ignore").decode().lower()

    texto = re.sub(r"[^a-z0-9 ]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    equivalencias = {
        "bogota d c": "bogota",
        "bogota": "bogota",
        "cartagena": "cartagena de indias"
    }

    return equivalencias.get(texto, texto)


try:
    clave = getpass("Contrasena de MySQL 8.0: ")

    # SERVIDOR 1: MariaDB
    conexion_maria = create_engine(
        URL.create(
            "mysql+pymysql",
            username="root",
            password="",
            host="127.0.0.1",
            port=3306,
            database="dw_servientrega"
        )
    )

    # SERVIDOR 2: MySQL 8.0
    conexion_mysql8 = create_engine(
        URL.create(
            "mysql+pymysql",
            username="root",
            password=clave,
            host="127.0.0.1",
            port=3307,
            database="geografia_servientrega"
        )
    )

    # Consultar envios de MariaDB
    consulta_envios = """
        SELECT
            h.id_envio,
            u.ciudad_destino,
            e.estado_envio
        FROM hechos_envios h
        INNER JOIN dim_ubicacion u
            ON h.id_ubicacion = u.id_ubicacion
        INNER JOIN dim_estado e
            ON h.id_estado = e.id_estado
    """

    envios = pd.read_sql(
        consulta_envios, conexion_maria
    )

    # Consultar municipios de MySQL 8.0
    consulta_municipios = """
        SELECT
            cod_mpio,
            dpto,
            nom_mpio,
            longitud,
            latitud
        FROM municipios_dane
    """

    municipios = pd.read_sql(
        consulta_municipios, conexion_mysql8
    )

    # Normalizar nombres
    envios["ciudad_key"] = (
        envios["ciudad_destino"].apply(normalizar)
    )

    municipios["ciudad_key"] = (
        municipios["nom_mpio"].apply(normalizar)
    )

    municipios = municipios.drop_duplicates(
        subset="ciudad_key"
    )

    # Unir la informacion de los dos servidores
    resultado = pd.merge(
        envios,
        municipios,
        on="ciudad_key",
        how="left"
    )

    columnas = [
        "id_envio",
        "ciudad_destino",
        "estado_envio",
        "nom_mpio",
        "dpto",
        "cod_mpio",
        "latitud",
        "longitud"
    ]

    print("\nCONSULTA FEDERADA EXITOSA")
    print("\nRESULTADO DE LOS ENVIOS:")
    print(resultado[columnas].to_string(index=False))

    coincidencias = resultado["cod_mpio"].notna().sum()

    print("\nTotal de envios:", len(resultado))
    print("Municipios relacionados:", coincidencias)

    resultado.to_csv(
        "resultado_consulta_federada.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nArchivo de consulta federada generado")

except Exception as error:
    print("ERROR EN LA CONSULTA FEDERADA:", error)

finally:
    if "conexion_maria" in locals():
        conexion_maria.dispose()

    if "conexion_mysql8" in locals():
        conexion_mysql8.dispose()
