import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Proceso KDD Completo - Operaciones Logísticas Servientrega S.A.\n",
                "**Etapas:** 1. Selección de datos | 2. Preprocesamiento | 3. Transformación | 4. Minería de datos (K-Means) | 5. Interpretación de resultados."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Selección de Datos (Desde Data Warehouse MariaDB)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "from sqlalchemy import create_engine, text\n",
                "from sklearn.preprocessing import StandardScaler\n",
                "from sklearn.cluster import KMeans\n",
                "import matplotlib.pyplot as plt\n\n",
                "engine = create_engine('mysql+pymysql://root:@localhost:3306/dw_servientrega?charset=utf8mb4')\n",
                "query = text('''\n",
                "    SELECT h.id_envio, c.nombre AS cliente, u.ciudad_origen, u.ciudad_destino,\n",
                "           s.tipo_servicio, e.estado_envio, h.id_ubicacion,\n",
                "           h.tiempo_entrega_horas, h.cantidad_paquetes\n",
                "    FROM hechos_envios h\n",
                "    JOIN dim_cliente c ON h.id_cliente = c.id_cliente\n",
                "    JOIN dim_ubicacion u ON h.id_ubicacion = u.id_ubicacion\n",
                "    JOIN dim_servicio s ON h.id_servicio = s.id_servicio\n",
                "    JOIN dim_estado e ON h.id_estado = e.id_estado\n",
                "''')\n",
                "df_raw = pd.read_sql(query, engine)\n",
                "print('Total de envíos seleccionados:', len(df_raw))\n",
                "display(df_raw)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Preprocesamiento (Limpieza e Imputación de Nulos)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df_clean = df_raw.copy()\n",
                "print('Nulos detectados antes de limpieza:\\n', df_clean.isna().sum())\n\n",
                "mediana_tiempo = df_clean['tiempo_entrega_horas'].median()\n",
                "df_clean['tiempo_entrega_horas'] = df_clean['tiempo_entrega_horas'].fillna(mediana_tiempo)\n",
                "print('\\nMediana imputada para envío en tránsito:', mediana_tiempo, 'horas')\n",
                "display(df_clean)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Transformación (Estandarización Z-Score)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "features = ['id_ubicacion', 'cantidad_paquetes', 'tiempo_entrega_horas']\n",
                "scaler = StandardScaler()\n",
                "X_scaled = scaler.fit_transform(df_clean[features])\n",
                "df_scaled = pd.DataFrame(X_scaled, columns=[f'{c}_norm' for c in features])\n",
                "display(df_scaled)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Minería de Datos (Agrupamiento K-Means, k=2)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)\n",
                "df_clean['cluster'] = kmeans.fit_predict(X_scaled)\n\n",
                "display(df_clean[['id_envio', 'ciudad_destino', 'tipo_servicio', 'estado_envio', 'cantidad_paquetes', 'tiempo_entrega_horas', 'cluster']])\n\n",
                "plt.figure(figsize=(7, 4))\n",
                "for c_id in sorted(df_clean['cluster'].unique()):\n",
                "    sub = df_clean[df_clean['cluster'] == c_id]\n",
                "    plt.scatter(sub['cantidad_paquetes'], sub['tiempo_entrega_horas'], label=f'Clúster {c_id}', s=120)\n",
                "    for _, r in sub.iterrows():\n",
                "        plt.annotate(f\"ID {r['id_envio']}\", (r['cantidad_paquetes'], r['tiempo_entrega_horas']), xytext=(5, 5), textcoords='offset points')\n",
                "plt.title('Segmentación K-Means de Envíos Servientrega')\n",
                "plt.xlabel('Cantidad de Paquetes')\n",
                "plt.ylabel('Tiempo de Entrega (Horas)')\n",
                "plt.legend()\n",
                "plt.grid(True, alpha=0.3)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Interpretación de Resultados\n",
                "- **Clúster 0 (Envíos estándar de 1 a 2 paquetes):** Concentra las rutas principales Bogotá–Medellín y Cali–Bogotá.\n",
                "- **Clúster 1 (Despacho multipaquete en corredor Caribe):** Aísla el envío `1004` (3 paquetes en ruta Barranquilla–Cartagena, estado *En tránsito*), indicando necesidad de seguimiento operativo prioritario."
            ]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("kdd_kpi_xa/kdd_servientrega.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Notebook creado en: kdd_kpi_xa/kdd_servientrega.ipynb")