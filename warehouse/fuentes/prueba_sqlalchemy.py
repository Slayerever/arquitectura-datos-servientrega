from sqlalchemy import create_engine, text
import pandas as pd

try:
    # Crear conexion con MariaDB
    engine = create_engine(
        "mysql+pymysql://root:@localhost:3306/dw_servientrega?charset=utf8mb4"
    )

    # Consultar los envios
    with engine.connect() as conexion:
        consulta = text("SELECT * FROM hechos_envios")

        datos = pd.read_sql(consulta, conexion)

        print("CONEXION CON SQLALCHEMY EXITOSA")
        print("\nREGISTROS DE ENVIOS:")
        print(datos)

        print("\nTOTAL DE ENVIOS:", len(datos))

    engine.dispose()

except Exception as error:
    print("ERROR:", error)
