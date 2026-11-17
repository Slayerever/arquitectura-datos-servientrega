import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Dashboard Logístico - Servientrega S.A.", layout="wide")

st.title("📦 Dashboard Analítico de Operaciones Logísticas — Servientrega S.A.")
st.caption("Arquitectura de Datos | Data Warehouse, Gobernanza, KPI y Minería KDD")

engine = create_engine("mysql+pymysql://root:@localhost:3306/dw_servientrega?charset=utf8mb4")

with engine.connect() as conn:
    df = pd.read_sql(text("""
        SELECT
            h.id_envio,
            c.nombre AS cliente,
            c.tipo_cliente,
            t.fecha AS fecha_envio,
            u.ciudad_origen,
            u.ciudad_destino,
            s.tipo_servicio,
            e.estado_envio,
            h.id_ubicacion,
            h.fecha_prometida,
            h.fecha_entrega,
            h.tiempo_entrega_horas,
            h.cantidad_paquetes
        FROM hechos_envios h
        INNER JOIN dim_cliente c ON h.id_cliente = c.id_cliente
        INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
        INNER JOIN dim_ubicacion u ON h.id_ubicacion = u.id_ubicacion
        INNER JOIN dim_servicio s ON h.id_servicio = s.id_servicio
        INNER JOIN dim_estado e ON h.id_estado = e.id_estado
    """), conn)

    df_calidad = pd.read_sql(text("""
        SELECT id_validacion, regla, registros_evaluados, registros_fallidos, estado
        FROM log_calidad_datos
    """), conn)

engine.dispose()

# Filtro lateral
st.sidebar.header("Filtros operativos")
estados_sel = st.sidebar.multiselect(
    "Estado del envío:",
    options=df["estado_envio"].unique(),
    default=list(df["estado_envio"].unique())
)
df_filtrado = df[df["estado_envio"].isin(estados_sel)].copy()

# Tarjetas de KPI principales
entregados = df_filtrado[df_filtrado["estado_envio"] == "Entregado"]
tiempo_prom = round(entregados["tiempo_entrega_horas"].mean(), 1) if not entregados.empty else 0.0
a_tiempo = (pd.to_datetime(entregados["fecha_entrega"]) <= pd.to_datetime(entregados["fecha_prometida"])).sum()
pct_tiempo = round((a_tiempo / len(entregados)) * 100, 1) if not entregados.empty else 0.0
pct_devueltos = round(((df_filtrado["estado_envio"] == "Devuelto").sum() / len(df_filtrado)) * 100, 1) if not df_filtrado.empty else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Envíos", len(df_filtrado), f"{int(df_filtrado['cantidad_paquetes'].sum())} paquetes")
col2.metric("Tiempo Promedio Entrega", f"{tiempo_prom} h", "Meta: <= 48.0 h")
col3.metric("Entregas a Tiempo", f"{pct_tiempo} %", "Meta: >= 90.0 %")
col4.metric("Tasa de Devolución", f"{pct_devueltos} %", "Meta: <= 10.0 %")

st.divider()

# Sección 1: Gráficos y Tabla Pivote
c_izq, c_der = st.columns(2)

with c_izq:
    st.subheader("Envíos y Paquetes por Ciudad Destino")
    resumen_ciudad = df_filtrado.groupby("ciudad_destino")[["cantidad_paquetes"]].sum()
    st.bar_chart(resumen_ciudad)

with c_der:
    st.subheader("Tabla Pivote: Paquetes por Destino y Servicio")
    pivote = pd.pivot_table(
        df_filtrado,
        values="cantidad_paquetes",
        index="ciudad_destino",
        columns="tipo_servicio",
        aggfunc="sum",
        fill_value=0
    )
    st.dataframe(pivote, use_container_width=True)

st.divider()

# Sección 2: Minería K-Means y Gobernanza
c_kdd, c_gob = st.columns(2)

with c_kdd:
    st.subheader("Segmentación K-Means (Minería KDD)")
    df_kdd = df.copy()
    df_kdd["tiempo_entrega_horas"] = df_kdd["tiempo_entrega_horas"].fillna(df_kdd["tiempo_entrega_horas"].median())
    X = StandardScaler().fit_transform(df_kdd[["id_ubicacion", "cantidad_paquetes", "tiempo_entrega_horas"]])
    df_kdd["cluster"] = KMeans(n_clusters=2, random_state=42, n_init=10).fit_predict(X)
    st.dataframe(
        df_kdd[["id_envio", "ciudad_destino", "tipo_servicio", "cantidad_paquetes", "tiempo_entrega_horas", "cluster"]],
        use_container_width=True
    )

with c_gob:
    st.subheader("Auditoría de Calidad de Datos (Gobernanza)")
    st.dataframe(df_calidad, use_container_width=True)