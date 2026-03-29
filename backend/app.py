"""
SERVIDOR WEB FLASK - API REST
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Configurar path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos del backend
from backend.knowledge_base import (
    obtener_todas_estaciones, 
    estaciones, 
    obtener_info_completa,
    obtener_rutas_estacion,
    obtener_coordenadas
)
from backend.search_engine import a_star, formatear_resultado
from backend.rules import obtener_descripcion_reglas

# Crear aplicación Flask
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)


# ============================================================
# RUTAS DE LA API
# ============================================================

@app.route('/')
def index():
    """Servir la interfaz principal"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/api/estaciones', methods=['GET'])
def get_estaciones():
    """Obtener todas las estaciones"""
    estaciones_lista = obtener_todas_estaciones()
    
    rutas_unicas = set()
    for estacion_info in estaciones.values():
        for ruta in estacion_info.get("rutas", []):
            rutas_unicas.add(ruta)
    
    return jsonify({
        "estaciones": estaciones_lista,
        "total": len(estaciones_lista),
        "rutas_disponibles": sorted(list(rutas_unicas))
    })


@app.route('/api/estaciones/<nombre>', methods=['GET'])
def get_estacion_info(nombre):
    """Obtener información de una estación"""
    if nombre not in estaciones:
        return jsonify({"error": f"Estación '{nombre}' no encontrada"}), 404
    
    info = estaciones[nombre]
    from backend.knowledge_base import obtener_conexiones
    conexiones = obtener_conexiones(nombre)
    
    return jsonify({
        "nombre": nombre,
        "coordenadas": list(info["coords"]),
        "rutas": info["rutas"],
        "conexiones": [
            {"destino": c[0], "ruta": c[1], "tiempo": c[2]} 
            for c in conexiones
        ]
    })


@app.route('/api/ruta', methods=['POST'])
def calcular_ruta():
    """Calcular la mejor ruta entre dos estaciones"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    
    origen = data.get('origen')
    destino = data.get('destino')
    hora = data.get('hora', None)
    
    if not origen or not destino:
        return jsonify({"error": "Se requieren origen y destino"}), 400
    
    if origen not in estaciones:
        return jsonify({"error": f"La estación '{origen}' no existe"}), 400
    
    if destino not in estaciones:
        return jsonify({"error": f"La estación '{destino}' no existe"}), 400
    
    ruta, costo, transbordos, nodos_explorados = a_star(origen, destino, hora)
    resultado = formatear_resultado(origen, destino, ruta, costo, transbordos, nodos_explorados)
    
    return jsonify(resultado)


@app.route('/api/info', methods=['GET'])
def get_info_sistema():
    """Obtener información general del sistema"""
    info_base = obtener_info_completa()
    reglas = obtener_descripcion_reglas()
    
    return jsonify({
        "total_estaciones": info_base["total_estaciones"],
        "total_conexiones": info_base["total_conexiones"],
        "rutas_disponibles": info_base["rutas_disponibles"],
        "reglas": reglas
    })


@app.route('/api/reglas', methods=['GET'])
def get_reglas():
    """Obtener descripción de las reglas"""
    return jsonify(obtener_descripcion_reglas())


@app.route('/api/rutas', methods=['GET'])
def get_rutas_info():
    """Obtener información de todas las rutas"""
    rutas_info = {}
    for estacion, info in estaciones.items():
        for ruta in info.get("rutas", []):
            if ruta not in rutas_info:
                rutas_info[ruta] = []
            rutas_info[ruta].append(estacion)
    
    descripciones_rutas = {
        "T31": {"tipo": "Troncal", "descripcion": "Conecta Capri con Paso del Comercio", "color": "#00adb5"},
        "E21": {"tipo": "Express", "descripcion": "Conecta Torre de Cali con Universidades", "color": "#5c6bc0"},
        "P27D": {"tipo": "Periférica", "descripcion": "Ruta circular periférica (inventada)", "color": "#ff6b6b"},
        "P41": {"tipo": "Alimentador", "descripcion": "Ruta alimentadora del centro (inventada)", "color": "#ffc107"}
    }
    
    resultado = []
    for ruta, estaciones_lista in rutas_info.items():
        info = descripciones_rutas.get(ruta, {
            "tipo": "Desconocido",
            "descripcion": "Ruta del sistema MIO",
            "color": "#6c757d"
        })
        resultado.append({
            "nombre": ruta,
            "tipo": info["tipo"],
            "descripcion": info["descripcion"],
            "color": info["color"],
            "numero_estaciones": len(estaciones_lista),
            "estaciones": sorted(estaciones_lista)
        })
    
    return jsonify({"rutas": resultado})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("SISTEMA INTELIGENTE DE RUTAS MIO DE CALI")
    print("=" * 60)
    
    info = obtener_info_completa()
    print(f"Base de conocimiento cargada:")
    print(f"  - {info['total_estaciones']} estaciones")
    print(f"  - {info['total_conexiones']} conexiones")
    print(f"  - Rutas: {', '.join(info['rutas_disponibles'])}")
    print()
    print(f"Servidor iniciado en: http://localhost:5000")
    print("Presiona Ctrl+C para detener")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)