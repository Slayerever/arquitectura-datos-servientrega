import mysql.connector
import pandas as pd
from getpass import getpass

clave_maria = getpass("Contrasena MariaDB: ")
clave_mysql8 = getpass("Contrasena MySQL 8.0: ")

# Conexion Nodo 1
nodo1 = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=clave_maria,
    database="nodo1_servientrega"
)

# Conexion Nodo 2
nodo2 = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password=clave_mysql8,
    database="nodo2_servientrega"
)

# Leer registros de ambos nodos
df1 = pd.read_sql("SELECT * FROM envios", nodo1)
df2 = pd.read_sql("SELECT * FROM envios", nodo2)

# Unificar los fragmentos
datos = pd.concat([df1, df2], ignore_index=True)

# Guardar resultado
datos.to_csv("envios_segmentados_python.csv", index=False)

print("REGISTROS DEL NODO 1:", len(df1))
print("REGISTROS DEL NODO 2:", len(df2))
print("TOTAL DE REGISTROS:", len(datos))
print("Archivo generado: envios_segmentados_python.csv")

nodo1.close()
nodo2.close()
