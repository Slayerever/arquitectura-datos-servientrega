import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="dw_servientrega"
    )

    if conexion.is_connected():
        print("Conexion exitosa con MariaDB")
        print("Base de datos: dw_servientrega")

except Error as error:
    print("Error de conexion:", error)

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("Conexion cerrada")
