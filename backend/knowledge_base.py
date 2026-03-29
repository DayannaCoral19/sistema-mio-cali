"""
BASE DE CONOCIMIENTO DEL MIO DE CALI
=====================================
Este archivo contiene toda la información del sistema de transporte
"""

import math

# ============================================================
# 1. DICCIONARIO DE ESTACIONES CON COORDENADAS
# ============================================================

estaciones = {
    # RUTA T31
    "Capri": {"coords": (3.4567, -76.5523), "rutas": ["T31", "P27D"]},
    "Caldas B1": {"coords": (3.4542, -76.5498), "rutas": ["T31"]},
    "Refugio B1": {"coords": (3.4518, -76.5472), "rutas": ["T31"]},
    "Pampalinda B1": {"coords": (3.4493, -76.5447), "rutas": ["T31"]},
    "Guadalupe B1": {"coords": (3.4469, -76.5421), "rutas": ["T31"]},
    "Unidad Deportiva": {"coords": (3.4444, -76.5396), "rutas": ["T31", "P27D"]},
    "Lido": {"coords": (3.4420, -76.5370), "rutas": ["T31"]},
    "Tequendama": {"coords": (3.4395, -76.5345), "rutas": ["T31", "P27D"]},
    "Estadio": {"coords": (3.4371, -76.5319), "rutas": ["T31", "P27D"]},
    "Manzana Del Saber": {"coords": (3.4346, -76.5294), "rutas": ["T31"]},
    "Santa Librada": {"coords": (3.4322, -76.5268), "rutas": ["T31", "P27D"]},
    "San Bosco": {"coords": (3.4297, -76.5243), "rutas": ["T31", "P27D", "E21"]},
    "San Pascual": {"coords": (3.4273, -76.5217), "rutas": ["T31"]},
    "Petecuy": {"coords": (3.4248, -76.5192), "rutas": ["T31"]},
    "San Pedro": {"coords": (3.4224, -76.5166), "rutas": ["T31"]},
    "Torre De Cali": {"coords": (3.4199, -76.5141), "rutas": ["T31", "P41", "E21", "P27D"]},
    "San Nicolas": {"coords": (3.4175, -76.5115), "rutas": ["P41"]},
    "Piloto Colombina": {"coords": (3.4150, -76.5090), "rutas": ["P41"]},
    "Fatima B1": {"coords": (3.4126, -76.5064), "rutas": ["T31", "P41"]},
    "Manzanares B1": {"coords": (3.4101, -76.5039), "rutas": ["T31", "P41"]},
    "Popular B2": {"coords": (3.4077, -76.5013), "rutas": ["T31", "P41"]},
    "Salomia B1": {"coords": (3.4052, -76.4988), "rutas": ["T31", "P41"]},
    "Flora Industrial B1": {"coords": (3.4028, -76.4962), "rutas": ["T31", "P41"]},
    "Chiminangos": {"coords": (3.4003, -76.4937), "rutas": ["T31", "P41"]},
    "Paso Del Comercio B5": {"coords": (3.3979, -76.4911), "rutas": ["T31", "P41"]},
    
    # RUTA E21
    "Plaza De Caycedo": {"coords": (3.4215, -76.5158), "rutas": ["E21"]},
    "Centro A1": {"coords": (3.4239, -76.5184), "rutas": ["E21"]},
    "Melendez A1": {"coords": (3.4310, -76.5342), "rutas": ["P27D", "E21"]},
    "Buitrera A1": {"coords": (3.4055, -76.5489), "rutas": ["P27D", "E21"]},
    "Universidades": {"coords": (3.3750, -76.5500), "rutas": ["E21", "P27D"]},
    
    # RUTA P27D
    "Caldas A1": {"coords": (3.4542, -76.5498), "rutas": ["P27D"]},
    "Pampalinda A1": {"coords": (3.4493, -76.5447), "rutas": ["P27D"]},
}

# ============================================================
# 2. GRAFO DE CONEXIONES
# ============================================================

grafo = {
    # RUTA T31
    "Capri": [("Caldas B1", "T31", 2), ("Caldas A1", "P27D", 1)],
    "Caldas B1": [("Capri", "T31", 2), ("Refugio B1", "T31", 1)],
    "Refugio B1": [("Caldas B1", "T31", 1), ("Pampalinda B1", "T31", 2)],
    "Pampalinda B1": [("Refugio B1", "T31", 2), ("Guadalupe B1", "T31", 2)],
    "Guadalupe B1": [("Pampalinda B1", "T31", 2), ("Unidad Deportiva", "T31", 2)],
    "Unidad Deportiva": [("Guadalupe B1", "T31", 2), ("Lido", "T31", 1), ("Pampalinda A1", "P27D", 2)],
    "Lido": [("Unidad Deportiva", "T31", 1), ("Tequendama", "T31", 1)],
    "Tequendama": [("Lido", "T31", 1), ("Estadio", "T31", 1), ("Melendez A1", "P27D", 3)],
    "Estadio": [("Tequendama", "T31", 1), ("Manzana Del Saber", "T31", 1), ("Santa Librada", "P27D", 2)],
    "Manzana Del Saber": [("Estadio", "T31", 1), ("Santa Librada", "T31", 2)],
    "Santa Librada": [("Manzana Del Saber", "T31", 2), ("San Bosco", "T31", 2), ("Estadio", "P27D", 2)],
    "San Bosco": [("Santa Librada", "T31", 2), ("San Pascual", "T31", 1), ("Torre De Cali", "P27D", 3), ("Plaza De Caycedo", "E21", 2)],
    "San Pascual": [("San Bosco", "T31", 1), ("Petecuy", "T31", 2)],
    "Petecuy": [("San Pascual", "T31", 2), ("San Pedro", "T31", 2)],
    "San Pedro": [("Petecuy", "T31", 2), ("Torre De Cali", "T31", 2)],
    "Torre De Cali": [("San Pedro", "T31", 2), ("San Nicolas", "P41", 2), ("Plaza De Caycedo", "E21", 1), ("San Bosco", "P27D", 3)],
    "Fatima B1": [("Manzanares B1", "T31", 2), ("San Nicolas", "P41", 2)],
    "Manzanares B1": [("Fatima B1", "T31", 2), ("Popular B2", "T31", 2)],
    "Popular B2": [("Manzanares B1", "T31", 2), ("Salomia B1", "T31", 2)],
    "Salomia B1": [("Popular B2", "T31", 2), ("Flora Industrial B1", "T31", 2)],
    "Flora Industrial B1": [("Salomia B1", "T31", 2), ("Chiminangos", "T31", 2)],
    "Chiminangos": [("Flora Industrial B1", "T31", 2), ("Paso Del Comercio B5", "T31", 2)],
    "Paso Del Comercio B5": [("Chiminangos", "T31", 2), ("Chiminangos", "P41", 2)],
    
    # RUTA E21
    "Plaza De Caycedo": [("Torre De Cali", "E21", 1), ("Centro A1", "E21", 1)],
    "Centro A1": [("Plaza De Caycedo", "E21", 1), ("San Bosco", "E21", 2)],
    "Melendez A1": [("Tequendama", "P27D", 3), ("Buitrera A1", "E21", 3)],
    "Buitrera A1": [("Melendez A1", "E21", 3), ("Universidades", "E21", 4), ("Universidades", "P27D", 4)],
    "Universidades": [("Buitrera A1", "E21", 4), ("Buitrera A1", "P27D", 4)],
    
    # RUTA P27D
    "Caldas A1": [("Capri", "P27D", 1), ("Pampalinda A1", "P27D", 2)],
    "Pampalinda A1": [("Caldas A1", "P27D", 2), ("Unidad Deportiva", "P27D", 2)],
    
    # RUTA P41
    "San Nicolas": [("Torre De Cali", "P41", 2), ("Piloto Colombina", "P41", 2)],
    "Piloto Colombina": [("San Nicolas", "P41", 2), ("Fatima B1", "P41", 2)],
}


# ============================================================
# 3. FUNCIONES DE ACCESO
# ============================================================

def obtener_todas_estaciones():
    """Retorna lista ordenada de todas las estaciones"""
    return sorted(estaciones.keys())


def obtener_rutas_estacion(estacion):
    """Retorna las rutas que pasan por una estación"""
    return estaciones.get(estacion, {}).get("rutas", [])


def obtener_coordenadas(estacion):
    """Retorna coordenadas de una estación"""
    coords = estaciones.get(estacion, {}).get("coords", (0, 0))
    return coords


def obtener_conexiones(estacion):
    """Retorna todas las conexiones desde una estación"""
    return grafo.get(estacion, [])


def calcular_distancia_euclidiana(estacion1, estacion2):
    """Calcula distancia para heurística"""
    x1, y1 = obtener_coordenadas(estacion1)
    x2, y2 = obtener_coordenadas(estacion2)
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * 10


def obtener_info_completa():
    """Retorna información estadística del sistema"""
    total_estaciones = len(estaciones)
    total_conexiones = sum(len(conexiones) for conexiones in grafo.values())
    rutas_unicas = set()
    
    for estacion_info in estaciones.values():
        for ruta in estacion_info.get("rutas", []):
            rutas_unicas.add(ruta)
    
    return {
        "total_estaciones": total_estaciones,
        "total_conexiones": total_conexiones,
        "rutas_disponibles": sorted(list(rutas_unicas)),
        "estaciones": obtener_todas_estaciones()
    }


if __name__ == "__main__":
    print("=" * 60)
    print("BASE DE CONOCIMIENTO DEL MIO DE CALI")
    print("=" * 60)
    info = obtener_info_completa()
    print(f"Total estaciones: {info['total_estaciones']}")
    print(f"Total conexiones: {info['total_conexiones']}")
    print(f"Rutas disponibles: {', '.join(info['rutas_disponibles'])}")