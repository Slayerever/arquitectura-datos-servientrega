import mysql.connector
from mysql.connector import Error
from getpass import getpass

try:
    clave = getpass("Contrasena de MySQL Server 8.0: ")

    conexion = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password=clave
    )

    if conexion.is_connected():
        print("CONEXION EXITOSA CON MYSQL SERVER 8.0")
        print("Segundo servidor disponible")

except Error as error:
    print("ERROR DE CONEXION:", error)

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
