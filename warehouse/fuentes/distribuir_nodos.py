import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Configuracion de los servidores
HOST = "127.0.0.1"
USUARIO = "root"

COLUMNAS = """
    id_envio, id_cliente, id_tiempo, id_ubicacion,
    id_servicio, id_estado, fecha_prometida,
    fecha_entrega, tiempo_entrega_horas, cantidad_paquetes
"""

SQL_CREAR_TABLA = """
CREATE TABLE IF NOT EXISTS envios (
    id_envio INT PRIMARY KEY,
    id_cliente INT,
    id_tiempo INT,
    id_ubicacion INT,
    id_servicio INT,
    id_estado INT,
    fecha_prometida DATE,
    fecha_entrega DATE,
    tiempo_entrega_horas DECIMAL(8,2),
    cantidad_paquetes INT
)
"""

def preparar_nodo(conexion, nombre_bd):
    cursor = conexion.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{nombre_bd}`")
    cursor.execute(f"USE `{nombre_bd}`")
    cursor.execute(SQL_CREAR_TABLA)
    conexion.commit()
    cursor.close()

def distribuir(origen, destino, tabla_fragmento, nombre_bd, nombre_nodo):
    preparar_nodo(destino, nombre_bd)

    cursor_origen = origen.cursor()
    cursor_origen.execute(
        f"SELECT {COLUMNAS} FROM `{tabla_fragmento}`"
    )
    registros = cursor_origen.fetchall()
    cursor_origen.close()

    cursor_destino = destino.cursor()
    cursor_destino.execute("DELETE FROM envios")

    sql = """
        INSERT INTO envios (
            id_envio, id_cliente, id_tiempo, id_ubicacion,
            id_servicio, id_estado, fecha_prometida,
            fecha_entrega, tiempo_entrega_horas, cantidad_paquetes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    if registros:
        cursor_destino.executemany(sql, registros)

    destino.commit()
    print(f"{nombre_nodo}: {len(registros)} registros distribuidos.")

    cursor_destino.close()

def main():
    origen = nodo1 = nodo2 = None

    try:
        print("DISTRIBUCION DE ENVIOS ENTRE DOS NODOS")

        clave_maria = getpass("Contrasena de MariaDB (3306): ")
        clave_mysql8 = getpass("Contrasena de MySQL 8.0 (3307): ")

        # Conexion a la base de datos original
        origen = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=USUARIO,
            password=clave_maria,
            database="dw_servientrega"
        )

        # Conexion al primer nodo: MariaDB
        nodo1 = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=USUARIO,
            password=clave_maria
        )

        # Conexion al segundo nodo: MySQL 8.0
        nodo2 = mysql.connector.connect(
            host=HOST,
            port=3307,
            user=USUARIO,
            password=clave_mysql8
        )

        distribuir(
            origen, nodo1,
            "fragmento_nodo1",
            "nodo1_servientrega",
            "Nodo 1"
        )

        distribuir(
            origen, nodo2,
            "fragmento_nodo2",
            "nodo2_servientrega",
            "Nodo 2"
        )

        print("\nDistribucion finalizada correctamente.")

    except Error as error:
        print(f"\nError durante la distribucion: {error}")

    finally:
        for conexion in (origen, nodo1, nodo2):
            if conexion is not None and conexion.is_connected():
                conexion.close()

if __name__ == "__main__":
    main()
