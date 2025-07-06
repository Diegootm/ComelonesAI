import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

# Cargamos los datos de nutricion
with open('datos/nutricion.json', encoding='utf-8') as f:
    alimentos = json.load(f)

df = pd.DataFrame(alimentos)

# Convertir valores a numéricos y manejamos los nulos 
numeric_cols = ['calorias', 'proteina', 'grasa_total', 'carbohidratos', 'fibra']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].replace(r'[^\d.]', '', regex=True), errors='coerce')
df[numeric_cols] = df[numeric_cols].fillna(0)

# Selección de características clave
features = df[['calorias', 'proteina', 'grasa_total', 'carbohidratos', 'fibra']]

# Escalado y clustering
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Entrenar modelo de clustering
kmeans = KMeans(n_clusters=20, random_state=42)
df['cluster'] = kmeans.fit_predict(scaled_features)

# Guardar modelo y metadatos
joblib.dump(kmeans, 'modelo/clustering_model.pkl')
df[['nombre', 'cluster'] + numeric_cols].to_csv('datos/alimentos_clusters.csv', index=False)