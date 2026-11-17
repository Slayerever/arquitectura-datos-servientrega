import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Leer los datos segmentados
df = pd.read_csv("envios_segmentados_python.csv")

# Variables utilizadas para agrupar
columnas = ["id_ubicacion", "cantidad_paquetes"]

datos = df[columnas].copy()

# Tratar posibles valores vacios
datos = datos.fillna(datos.median())

# Normalizar los datos
escalador = StandardScaler()
datos_escalados = escalador.fit_transform(datos)

# Aplicar K-means con dos grupos
modelo = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)

df["cluster"] = modelo.fit_predict(datos_escalados)

# Guardar resultados
df.to_csv("envios_kmeans.csv", index=False)

print("AGRUPACION K-MEANS COMPLETADA")
print(df[["id_envio", "id_ubicacion",
          "cantidad_paquetes", "cluster"]])

print("\nCantidad de envios por grupo:")
print(df["cluster"].value_counts().sort_index())

print("\nArchivo generado: envios_kmeans.csv")
