from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecomendadorNutricional:
    def __init__(self, datos_path, modelo_path):
        self.df = pd.read_csv(datos_path)
        self.modelo = joblib.load(modelo_path)
        self.scaler = StandardScaler()
        self.scaler.fit(self.df[['calorias', 'proteina', 'grasa_total', 'carbohidratos', 'fibra']])
    
    def _calcular_similitud(self, meta_nutricional):
        # Escalar meta
        meta_scaled = self.scaler.transform([meta_nutricional])
        
        # Calcular similitud con todos los alimentos
        features = self.df[['calorias', 'proteina', 'grasa_total', 'carbohidratos', 'fibra']]
        scaled_features = self.scaler.transform(features)
        
        similitudes = cosine_similarity(meta_scaled, scaled_features)
        self.df['similitud'] = similitudes[0]
        
        return self.df.sort_values('similitud', ascending=False)
    
    def recomendar(self, objetivo, calorias_meta=None, n_recomendaciones=5):
        if objetivo == "bajar":
            # Meta: bajo calorías, alta proteína y fibra
            meta = [120, 20, 5, 15, 8]
        elif objetivo == "subir":
            # Meta: alto calorías, balance proteína/grasas
            meta = [450, 15, 15, 60, 5]
        elif objetivo == "calorias" and calorias_meta:
            # Personalizado según calorías
            meta = [calorias_meta, 15, 10, calorias_meta/7, 5]
        else:
            raise ValueError("Objetivo no válido")
        
        recomendaciones = self._calcular_similitud(meta)
        return recomendaciones.head(n_recomendaciones)