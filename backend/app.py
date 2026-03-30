"""
SERVIDOR WEB FLASK - API REST
-------------------------
Este archivo crea un servidor web que expone una API REST para:
- Obtener la lista de estaciones
- Calcular rutas entre estaciones
- Obtener información del sistema

Para ejecutar: python backend/app.py
Luego abrir: http://localhost:5000

Autor: Equipo de Desarrollo
Fecha: Marzo 2026
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json

# Agregar el directorio actual al path para importar módulos
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
CORS(app)  # Permitir peticiones desde cualquier origen

# --------------------------------------------------
# RUTAS DE LA API
# --------------------------------------------------

@app.route('/')
def index():
    """Servir la interfaz principal (frontend)"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/api/estaciones', methods=['GET'])
def get_estaciones():
    """
    API: Obtener todas las estaciones disponibles
    
    GET /api/estaciones
    Response: {
        "estaciones": ["Capri", "Caldas B1", ...],
        "total": 30,
        "rutas_disponibles": ["T31", "E21", "P27D", "P41"]
    }
    """
    estaciones_lista = obtener_todas_estaciones()
    
    # Obtener rutas únicas
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
    """
    API: Obtener información detallada de una estación
    
    GET /api/estaciones/Capri
    Response: {
        "nombre": "Capri",
        "coordenadas": [3.4567, -76.5523],
        "rutas": ["T31", "P27D"],
        "conexiones": [...]
    }
    """
    if nombre not in estaciones:
        return jsonify({"error": f"Estación '{nombre}' no encontrada"}), 404
    
    info = estaciones[nombre]
    
    # Obtener conexiones desde esta estación
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
    """
    API: Calcular la mejor ruta entre dos estaciones
    
    POST /api/ruta
    Body: {
        "origen": "Capri",
        "destino": "Universidades",
        "hora": 14.5 (opcional)
    }
    
    Response: {
        "exito": true,
        "origen": "Capri",
        "destino": "Universidades",
        "ruta": ["Capri", "Caldas A1", ...],
        "costo_total_minutos": 24.5,
        "numero_transbordos": 1,
        "detalles_pasos": [...],
        "nodos_explorados": 47
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos. Envía un JSON con 'origen' y 'destino'"}), 400
    
    origen = data.get('origen')
    destino = data.get('destino')
    hora = data.get('hora', None)
    
    # Validar campos obligatorios
    if not origen or not destino:
        return jsonify({"error": "Se requieren los campos 'origen' y 'destino'"}), 400
    
    # Validar que las estaciones existan
    if origen not in estaciones:
        return jsonify({"error": f"La estación de origen '{origen}' no existe"}), 400
    
    if destino not in estaciones:
        return jsonify({"error": f"La estación de destino '{destino}' no existe"}), 400
    
    # Ejecutar algoritmo A*
    ruta, costo, transbordos, nodos_explorados = a_star(origen, destino, hora)
    
    # Formatear resultado
    resultado = formatear_resultado(origen, destino, ruta, costo, transbordos, nodos_explorados)
    
    return jsonify(resultado)


@app.route('/api/info', methods=['GET'])
def get_info_sistema():
    """
    API: Obtener información general del sistema
    
    GET /api/info
    Response: {
        "total_estaciones": 30,
        "total_conexiones": 85,
        "rutas_disponibles": ["T31", "E21", "P27D", "P41"],
        "reglas": {...}
    }
    """
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
    """
    API: Obtener descripción de todas las reglas lógicas
    
    GET /api/reglas
    Response: {
        "regla_1": {...},
        "regla_2": {...},
        ...
    }
    """
    return jsonify(obtener_descripcion_reglas())


@app.route('/api/rutas', methods=['GET'])
def get_rutas_info():
    """
    API: Obtener información de todas las rutas
    
    GET /api/rutas
    Response: {
        "rutas": [
            {"nombre": "T31", "tipo": "Troncal", "estaciones": 25, "descripcion": "..."},
            ...
        ]
    }
    """
    # Contar estaciones por ruta
    rutas_info = {}
    for estacion, info in estaciones.items():
        for ruta in info.get("rutas", []):
            if ruta not in rutas_info:
                rutas_info[ruta] = []
            rutas_info[ruta].append(estacion)
    
    descripciones_rutas = {
        "T31": {
            "tipo": "Troncal",
            "descripcion": "Ruta principal que conecta Capri con Paso del Comercio",
            "color": "#00adb5"
        },
        "E21": {
            "tipo": "Express",
            "descripcion": "Ruta exprés que conecta Torre de Cali con Universidades",
            "color": "#5c6bc0"
        },
        "P27D": {
            "tipo": "Periférica",
            "descripcion": "Ruta circular periférica (inventada para el ejercicio)",
            "color": "#ff6b6b"
        },
        "P41": {
            "tipo": "Alimentador",
            "descripcion": "Ruta alimentadora del centro (inventada para el ejercicio)",
            "color": "#ffc107"
        }
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


# --------------------------------------------------
# MANEJADORES DE ERRORES
# --------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    """Manejar error 404"""
    return jsonify({"error": "Ruta no encontrada"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejar error 500"""
    return jsonify({"error": "Error interno del servidor"}), 500


# --------------------------------------------------
# INICIAR SERVIDOR
# --------------------------------------------------

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 SISTEMA INTELIGENTE DE RUTAS MIO DE CALI")
    print("=" * 70)
    
    # Mostrar información del sistema
    info = obtener_info_completa()
    print(f"📊 Base de conocimiento cargada:")
    print(f"   • {info['total_estaciones']} estaciones")
    print(f"   • {info['total_conexiones']} conexiones")
    print(f"   • Rutas: {', '.join(info['rutas_disponibles'])}")
    print()
    print(f"🌐 Servidor iniciado en: http://localhost:5000")
    print(f"📡 API disponible en: http://localhost:5000/api/")
    print()
    print("📋 Endpoints disponibles:")
    print("   GET  /api/estaciones        - Listar todas las estaciones")
    print("   GET  /api/estaciones/:nombre - Información de una estación")
    print("   POST /api/ruta              - Calcular ruta entre estaciones")
    print("   GET  /api/info              - Información del sistema")
    print("   GET  /api/reglas            - Reglas lógicas implementadas")
    print("   GET  /api/rutas             - Información de todas las rutas")
    print()
    print("🎯 Para probar la interfaz gráfica, abre: http://localhost:5000")
    print("=" * 70)
    print()
    print("Presiona Ctrl+C para detener el servidor")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)