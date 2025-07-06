from flask import Flask, request, jsonify
from modelo.recomendador import RecomendadorNutricional

app = Flask(__name__)
recomendador = RecomendadorNutricional(
    datos_path='datos/alimentos_clusters.csv',
    modelo_path='modelo/clustering_model.pkl'
)

@app.route('/recomendar', methods=['POST'])
def recomendar_alimentos():
    data = request.json
    objetivo = data.get('objetivo')
    calorias = data.get('calorias', None)
    
    try:
        if objetivo == "calorias" and not calorias:
            return jsonify({"error": "Se requiere parámetro 'calorias'"}), 400
            
        resultados = recomendador.recomendar(objetivo, calorias)
        return jsonify({
            "recomendaciones": resultados[['nombre', 'calorias', 'proteina', 'grasa_total', 'carbohidratos']].to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)