import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

# Ubicacion de los archivos
CARPETA = Path(__file__).resolve().parent

try:
    # 1. Crear la base de datos Staging
    conexion_admin = create_engine(
        "mysql+pymysql://root:@localhost:3306/"
    )

    with conexion_admin.begin() as conexion:
        conexion.execute(text("""
            CREATE DATABASE IF NOT EXISTS staging_servientrega
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_general_ci
        """))

    conexion_admin.dispose()

    # 2. Conectar con Staging
    engine = create_engine(
        "mysql+pymysql://root:@localhost:3306/staging_servientrega?charset=utf8mb4"
    )

    # 3. Definir las fuentes y tablas destino
    archivos = {
        "envios_bd_transformados.csv": "stg_envios_mariadb",
        "envios_csv_transformados.csv": "stg_envios_csv",
        "municipios_dane_transformados.csv": "stg_municipios_dane"
    }

    # 4. Cargar los archivos en Staging
    for archivo, tabla in archivos.items():

        ruta = CARPETA / archivo

        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encontro el archivo: {archivo}"
            )

        datos = pd.read_csv(ruta, encoding="utf-8-sig")

        datos.to_sql(
            name=tabla,
            con=engine,
            if_exists="replace",
            index=False
        )

        print(f"Tabla {tabla}: {len(datos)} registros cargados")

    # 5. Verificar los registros
    with engine.connect() as conexion:
        for tabla in archivos.values():
            total = conexion.execute(
                text(f"SELECT COUNT(*) FROM `{tabla}`")
            ).scalar_one()

            print(f"Verificacion {tabla}: {total} registros")

    print("\nCARGA EN STAGING COMPLETADA")

    engine.dispose()

except Exception as error:
    print("ERROR EN LA CARGA:", error)
