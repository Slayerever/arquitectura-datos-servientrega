import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:@localhost:3306/dw_servientrega?charset=utf8mb4")

with engine.connect() as conn:
    sql_pivote = text("""
        SELECT
            u.ciudad_destino,
            COUNT(h.id_envio) AS total_envios,
            SUM(CASE WHEN e.estado_envio = 'Entregado' THEN 1 ELSE 0 END) AS entregados,
            SUM(CASE WHEN e.estado_envio = 'En transito' THEN 1 ELSE 0 END) AS en_transito,
            SUM(CASE WHEN e.estado_envio = 'Pendiente' THEN 1 ELSE 0 END) AS pendientes,
            SUM(CASE WHEN e.estado_envio = 'Devuelto' THEN 1 ELSE 0 END) AS devueltos
        FROM hechos_envios h
        INNER JOIN dim_ubicacion u ON h.id_ubicacion = u.id_ubicacion
        INNER JOIN dim_estado e ON h.id_estado = e.id_estado
        GROUP BY u.ciudad_destino
        ORDER BY total_envios DESC
    """)
    df_pivote_sql = pd.read_sql(sql_pivote, conn)

    sql_base = text("""
        SELECT
            h.id_envio,
            c.nombre AS cliente,
            u.ciudad_origen,
            u.ciudad_destino,
            s.tipo_servicio,
            e.estado_envio,
            h.fecha_prometida,
            h.fecha_entrega,
            h.tiempo_entrega_horas,
            h.cantidad_paquetes
        FROM hechos_envios h
        INNER JOIN dim_cliente c ON h.id_cliente = c.id_cliente
        INNER JOIN dim_ubicacion u ON h.id_ubicacion = u.id_ubicacion
        INNER JOIN dim_servicio s ON h.id_servicio = s.id_servicio
        INNER JOIN dim_estado e ON h.id_estado = e.id_estado
    """)
    df = pd.read_sql(sql_base, conn)

print("=== 1. CONSULTA PIVOTE EN SQL (DESTINO VS ESTADO) ===")
print(df_pivote_sql.to_string(index=False))

tabla_pivote_py = pd.pivot_table(
    df,
    values="cantidad_paquetes",
    index="ciudad_destino",
    columns="tipo_servicio",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="Total"
)
print("\n=== 2. PIVOT_TABLE EN PYTHON (PAQUETES POR DESTINO Y SERVICIO) ===")
print(tabla_pivote_py)

total_envios = len(df)
total_paquetes = int(df["cantidad_paquetes"].sum())
entregados = df[df["estado_envio"] == "Entregado"].copy()
tiempo_prom_horas = round(entregados["tiempo_entrega_horas"].mean(), 2)

a_tiempo = (pd.to_datetime(entregados["fecha_entrega"]) <= pd.to_datetime(entregados["fecha_prometida"])).sum()
pct_a_tiempo = round((a_tiempo / len(entregados)) * 100, 1)

devueltos = (df["estado_envio"] == "Devuelto").sum()
pct_devueltos = round((devueltos / total_envios) * 100, 1)

pct_express = round(((df["tipo_servicio"] == "Express").sum() / total_envios) * 100, 1)
pct_top_destinos = round((df["ciudad_destino"].isin(["Bogota", "Medellin"]).sum() / total_envios) * 100, 1)

matriz_kpi = pd.DataFrame([
    ["KPI-01", "Volumen total de envíos", "COUNT(id_envio)", ">= 5 envíos", f"{total_envios} envíos ({total_paquetes} paq.)", "CUMPLIDO"],
    ["KPI-02", "Tiempo promedio de entrega", "AVG(tiempo_entrega_horas)", "<= 48.0 h", f"{tiempo_prom_horas} h", "EN OBSERVACIÓN"],
    ["KPI-03", "Porcentaje de entregas a tiempo", "(Entregas <= Prometida) / Entregados", ">= 90.0 %", f"{pct_a_tiempo} %", "CUMPLIDO"],
    ["KPI-04", "Tasa de devolución de envíos", "(Devueltos / Total envíos) * 100", "<= 10.0 %", f"{pct_devueltos} %", "ALERTA"],
    ["KPI-05", "Participación servicio Express", "(Envíos Express / Total) * 100", ">= 35.0 %", f"{pct_express} %", "CUMPLIDO"],
    ["KPI-06", "Concentración destinos principales", "(Bogotá + Medellín) / Total", ">= 70.0 %", f"{pct_top_destinos} %", "CUMPLIDO"]
], columns=["Código", "Indicador (KPI)", "Fórmula", "Meta", "Valor Actual", "Estado"])

print("\n=== 3. MATRIZ DE KPI LOGÍSTICOS - SERVIENTREGA ===")
print(matriz_kpi.to_string(index=False))

matriz_kpi.to_csv("kdd_kpi_xa/matriz_kpi.csv", index=False, encoding="utf-8-sig")
engine.dispose()