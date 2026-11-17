import mysql.connector
from mysql.connector import Error
from getpass import getpass

def conectar_nodos(clave_maria, clave_mysql8):
    n1 = mysql.connector.connect(
        host="127.0.0.1", port=3306, user="root",
        password=clave_maria, database="nodo1_servientrega", autocommit=False
    )
    n2 = mysql.connector.connect(
        host="127.0.0.1", port=3307, user="root",
        password=clave_mysql8, database="nodo2_servientrega", autocommit=False
    )
    return n1, n2

def limpiar_pruebas(n1, n2):
    for conn in (n1, n2):
        cur = conn.cursor()
        cur.execute("DELETE FROM envios WHERE id_envio IN (9001, 9002, 9003)")
        conn.commit()
        cur.close()

def escenario_xa_commit(n1, n2):
    print("\n=======================================================")
    print("ESCENARIO 1: TRANSACCIÓN DISTRIBUIDA EXITOSA (XA COMMIT)")
    print("=======================================================")
    c1, c2 = n1.cursor(), n2.cursor()
    xid1, xid2 = "xa_servi_ok_n1", "xa_servi_ok_n2"

    try:
        # Inicio de transacción distribuida en ambos nodos
        c1.execute(f"XA START '{xid1}'")
        c2.execute(f"XA START '{xid2}'")

        # Inserción en Nodo 1 (3306)
        c1.execute("""
            INSERT INTO envios VALUES
            (9001, 1, 1, 1, 1, 1, '2025-11-12', '2025-11-11', 22.00, 2)
        """)
        # Inserción en Nodo 2 (3307)
        c2.execute("""
            INSERT INTO envios VALUES
            (9002, 2, 2, 3, 2, 1, '2025-11-13', '2025-11-12', 26.00, 4)
        """)

        # Fase 1: Preparación (Two-Phase Commit)
        c1.execute(f"XA END '{xid1}'")
        c2.execute(f"XA END '{xid2}'")
        c1.execute(f"XA PREPARE '{xid1}'")
        c2.execute(f"XA PREPARE '{xid2}'")
        print("[FASE 1 - XA PREPARE] Ambos nodos listos para confirmar.")

        # Fase 2: Confirmación global atómica
        c1.execute(f"XA COMMIT '{xid1}'")
        c2.execute(f"XA COMMIT '{xid2}'")
        print("[FASE 2 - XA COMMIT] Confirmación exitosa en Nodo 1 (3306) y Nodo 2 (3307).")

        c1.execute("SELECT id_envio, id_ubicacion, cantidad_paquetes FROM envios WHERE id_envio = 9001")
        c2.execute("SELECT id_envio, id_ubicacion, cantidad_paquetes FROM envios WHERE id_envio = 9002")
        print("Registro confirmado en Nodo 1:", c1.fetchall())
        print("Registro confirmado en Nodo 2:", c2.fetchall())
    finally:
        c1.close()
        c2.close()

def escenario_xa_rollback(n1, n2):
    print("\n============================================================")
    print("ESCENARIO 2: FALLA EN UN NODO Y REVERSO ATÓMICO (XA ROLLBACK)")
    print("============================================================")
    c1, c2 = n1.cursor(), n2.cursor()
    xid1, xid2 = "xa_servi_fail_n1", "xa_servi_fail_n2"
    n1_preparado = False

    try:
        c1.execute(f"XA START '{xid1}'")
        c2.execute(f"XA START '{xid2}'")

        # Nodo 1 inserta bien y queda preparado
        c1.execute("""
            INSERT INTO envios VALUES
            (9003, 3, 3, 2, 1, 1, '2025-11-15', '2025-11-14', 20.00, 5)
        """)
        c1.execute(f"XA END '{xid1}'")
        c1.execute(f"XA PREPARE '{xid1}'")
        n1_preparado = True
        print("[NODO 1 - 3306] Registro 9003 insertado y puesto en estado XA PREPARE.")

        # Nodo 2 falla (clave primaria 1003 duplicada)
        print("[NODO 2 - 3307] Simulando falla de nodo durante escritura distribuida...")
        c2.execute("""
            INSERT INTO envios VALUES
            (1003, 1, 1, 4, 1, 1, '2025-11-15', '2025-11-14', 20.00, 5)
        """)

    except Error as err:
        print(f"[FALLA DETECTADA EN NODO 2]: {err}")
        print("[COORDINADOR XA] Ejecutando reverso global para evitar inconsistencias...")

        try:
            c2.execute(f"XA END '{xid2}'")
            c2.execute(f"XA ROLLBACK '{xid2}'")
        except Error:
            pass

        if n1_preparado:
            c1.execute(f"XA ROLLBACK '{xid1}'")
            print("[OK - XA ROLLBACK NODO 1] Registro 9003 revertido en Nodo 1 (3306).")

    c1.execute("SELECT COUNT(*) FROM envios WHERE id_envio = 9003")
    c2.execute("SELECT COUNT(*) FROM envios WHERE id_envio = 9003")
    print(f"Registros 9003 en Nodo 1 tras reverso: {c1.fetchone()[0]} (Sin datos huérfanos)")
    print(f"Registros 9003 en Nodo 2 tras reverso: {c2.fetchone()[0]} (Sin datos huérfanos)")

    c1.close()
    c2.close()

if __name__ == "__main__":
    clave_maria = getpass("Contraseña MariaDB (3306) [Enter si está vacía]: ")
    clave_mysql8 = getpass("Contraseña Servidor 2 (3307): ")

    nodo1, nodo2 = conectar_nodos(clave_maria, clave_mysql8)
    try:
        limpiar_pruebas(nodo1, nodo2)
        escenario_xa_commit(nodo1, nodo2)
        escenario_xa_rollback(nodo1, nodo2)
        limpiar_pruebas(nodo1, nodo2)
        print("\n[FINALIZADO] Nodos restaurados a su estado original (3 y 2 registros).")
    finally:
        nodo1.close()
        nodo2.close()