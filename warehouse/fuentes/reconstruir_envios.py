import mysql.connector
from getpass import getpass

clave_maria = getpass("Contrasena MariaDB: ")
clave_mysql8 = getpass("Contrasena MySQL 8.0: ")

maria = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=clave_maria,
    database="dw_servientrega"
)

mysql8 = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password=clave_mysql8,
    database="nodo2_servientrega"
)

columnas = """
id_envio, id_cliente, id_tiempo, id_ubicacion,
id_servicio, id_estado, fecha_prometida,
fecha_entrega, tiempo_entrega_horas, cantidad_paquetes
"""

cursor8 = mysql8.cursor()
cursor8.execute(f"SELECT {columnas} FROM envios")
registros = cursor8.fetchall()

cursor = maria.cursor()

# Tabla auxiliar para recibir los datos del Nodo 2
cursor.execute("""
CREATE TABLE IF NOT EXISTS fragmento_nodo2_recon
LIKE nodo1_servientrega.envios
""")

cursor.execute("DELETE FROM fragmento_nodo2_recon")

sql = """
INSERT INTO fragmento_nodo2_recon (
id_envio, id_cliente, id_tiempo, id_ubicacion,
id_servicio, id_estado, fecha_prometida,
fecha_entrega, tiempo_entrega_horas, cantidad_paquetes
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

if registros:
    cursor.executemany(sql, registros)

maria.commit()

# Reconstruccion mediante UNION ALL
cursor.execute("DROP TABLE IF EXISTS envios_reconstruidos")

cursor.execute("""
CREATE TABLE envios_reconstruidos AS
SELECT * FROM nodo1_servientrega.envios
UNION ALL
SELECT * FROM fragmento_nodo2_recon
""")

maria.commit()

cursor.execute("SELECT COUNT(*) FROM envios_reconstruidos")
total = cursor.fetchone()[0]

print("RECONSTRUCCION COMPLETADA")
print("Registros reconstruidos:", total)

cursor.close()
cursor8.close()
maria.close()
mysql8.close()
