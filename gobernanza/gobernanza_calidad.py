import mysql.connector
from mysql.connector import Error
import pandas as pd

def ejecutar_reglas_calidad():
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="dw_servientrega"
    )
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_calidad_datos (
            id_validacion INT AUTO_INCREMENT PRIMARY KEY,
            fecha_ejecucion DATETIME DEFAULT CURRENT_TIMESTAMP,
            regla VARCHAR(120),
            tabla_evaluada VARCHAR(80),
            registros_evaluados INT,
            registros_fallidos INT,
            estado VARCHAR(20),
            detalle VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("TRUNCATE TABLE log_calidad_datos")

    reglas = [
        ("R1 - Unicidad de clave primaria id_envio", "hechos_envios",
         "SELECT COUNT(*) FROM hechos_envios",
         "SELECT COUNT(*) - COUNT(DISTINCT id_envio) FROM hechos_envios",
         "Verifica ausencia de envíos duplicados"),
        ("R2 - Integridad referencial con dim_cliente", "hechos_envios",
         "SELECT COUNT(*) FROM hechos_envios",
         "SELECT COUNT(*) FROM hechos_envios h LEFT JOIN dim_cliente c ON h.id_cliente = c.id_cliente WHERE c.id_cliente IS NULL",
         "Todo envío debe pertenecer a un cliente válido"),
        ("R3 - Cantidad de paquetes mayor a cero", "hechos_envios",
         "SELECT COUNT(*) FROM hechos_envios",
         "SELECT COUNT(*) FROM hechos_envios WHERE cantidad_paquetes IS NULL OR cantidad_paquetes <= 0",
         "No se admiten envíos con 0 o menos paquetes"),
        ("R4 - Coherencia fecha_entrega vs estado Entregado", "hechos_envios",
         "SELECT COUNT(*) FROM hechos_envios WHERE id_estado = 1",
         "SELECT COUNT(*) FROM hechos_envios WHERE id_estado = 1 AND (fecha_entrega IS NULL OR tiempo_entrega_horas IS NULL)",
         "Todo envío Entregado debe registrar fecha y horas reales"),
        ("R5 - Tiempos de entrega no negativos", "hechos_envios",
         "SELECT COUNT(*) FROM hechos_envios WHERE tiempo_entrega_horas IS NOT NULL",
         "SELECT COUNT(*) FROM hechos_envios WHERE tiempo_entrega_horas < 0",
         "El tiempo de tránsito no puede ser negativo"),
        ("R6 - Completitud de ciudad_destino en dim_ubicacion", "dim_ubicacion",
         "SELECT COUNT(*) FROM dim_ubicacion",
         "SELECT COUNT(*) FROM dim_ubicacion WHERE ciudad_destino IS NULL OR TRIM(ciudad_destino) = ''",
         "Toda ruta requiere ciudad de destino normalizada")
    ]

    print("=== EJECUCIÓN DE REGLAS DE CALIDAD DE DATOS ===")
    for nombre_regla, tabla, sql_total, sql_fallos, detalle in reglas:
        cursor.execute(sql_total)
        total = cursor.fetchone()[0]
        cursor.execute(sql_fallos)
        fallidos = cursor.fetchone()[0]
        estado = "APROBADA" if fallidos == 0 else "CON_ALERTAS"

        cursor.execute("""
            INSERT INTO log_calidad_datos
            (regla, tabla_evaluada, registros_evaluados, registros_fallidos, estado, detalle)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_regla, tabla, total, fallidos, estado, detalle))

    conexion.commit()

    df_logs = pd.read_sql(
        "SELECT id_validacion, regla, registros_evaluados, registros_fallidos, estado FROM log_calidad_datos",
        conexion
    )
    print(df_logs.to_string(index=False))
    cursor.close()
    conexion.close()

def demostrar_control_acceso():
    print("\n=== DEMOSTRACIÓN EN VIVO: ROLES Y MÍNIMO PRIVILEGIO ===")
    try:
        conn_bloqueado = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="usuario_sin_permisos",
            password="Bloqueado2026*",
            database="dw_servientrega"
        )
        cur = conn_bloqueado.cursor()
        cur.execute("SELECT * FROM hechos_envios")
        cur.fetchall()
    except Error as err:
        print(f"[OK - BLOQUEO VERIFICADO] usuario_sin_permisos rechazado: {err}")

    try:
        conn_analista = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="analista_servi",
            password="Analista2026*",
            database="dw_servientrega"
        )
        cur = conn_analista.cursor()
        cur.execute("SELECT id_envio, codigo_cliente_anonimo, ciudad_destino, estado_envio FROM vw_envios_anonimizados LIMIT 3")
        filas = cur.fetchall()
        print(f"[OK - ACCESO PERMITIDO A VISTA ANONIMIZADA] Filas leídas por analista_servi: {len(filas)}")

        cur.execute("SELECT * FROM dim_cliente")
        cur.fetchall()
    except Error as err:
        print(f"[OK - PROTECCIÓN LEY 1581 VERIFICADA] analista_servi bloqueado en dim_cliente: {err}")
    finally:
        if 'conn_analista' in locals() and conn_analista.is_connected():
            conn_analista.close()

if __name__ == "__main__":
    ejecutar_reglas_calidad()
    demostrar_control_acceso()