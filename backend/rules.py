"""
REGLAS LÓGICAS DEL SISTEMA INTELIGENTE
"""

def regla_costo_transbordo(ruta_actual, ruta_siguiente):
    """Penaliza cambio de ruta con +5 minutos"""
    if ruta_actual is None:
        return 0
    if ruta_actual != ruta_siguiente:
        return 5
    return 0


def regla_costo_congestion(hora_del_dia):
    """Factor de congestión según hora"""
    if hora_del_dia is None:
        return 1.0
    if (6 <= hora_del_dia <= 9) or (17 <= hora_del_dia <= 19):
        return 1.5
    return 1.0


def regla_preferencia_transbordos(numero_transbordos):
    """Penaliza rutas con muchos transbordos"""
    if numero_transbordos > 2:
        return 10
    elif numero_transbordos > 1:
        return 3
    return 0


def regla_heuristica_adaptativa(distancia_base, transbordos_realizados):
    """Ajusta heurística según transbordos realizados"""
    if transbordos_realizados > 1:
        return distancia_base * 0.8
    return distancia_base


def regla_ruta_nocturna(hora, ruta):
    """Valida disponibilidad nocturna"""
    if hora is None:
        return True
    rutas_restringidas = ["P41", "P27D"]
    if hora > 21 and ruta in rutas_restringidas:
        return False
    return True


def aplicar_todas_reglas(ruta_actual, ruta_siguiente, transbordos, hora=None):
    """Aplica todas las reglas y calcula costo adicional"""
    resultados = {
        "costo_transbordo": 0,
        "costo_congestion": 1.0,
        "penalizacion_transbordos": 0,
        "costo_total_adicional": 0,
        "reglas_aplicadas": []
    }
    
    costo_tb = regla_costo_transbordo(ruta_actual, ruta_siguiente)
    resultados["costo_transbordo"] = costo_tb
    if costo_tb > 0:
        resultados["reglas_aplicadas"].append("transbordo")
    
    penalizacion = regla_preferencia_transbordos(transbordos)
    resultados["penalizacion_transbordos"] = penalizacion
    if penalizacion > 0:
        resultados["reglas_aplicadas"].append("penalizacion_transbordos")
    
    resultados["costo_total_adicional"] = costo_tb + penalizacion
    
    return resultados


REGLAS = {
    "costo_transbordo": regla_costo_transbordo,
    "costo_congestion": regla_costo_congestion,
    "preferencia_transbordos": regla_preferencia_transbordos,
    "heuristica_adaptativa": regla_heuristica_adaptativa,
    "ruta_nocturna": regla_ruta_nocturna,
}


def obtener_descripcion_reglas():
    """Retorna descripción de las reglas"""
    return {
        "regla_1": {
            "nombre": "Costo de Transbordo",
            "formato": "IF ruta_actual != ruta_siguiente THEN +5 minutos",
            "justificacion": "Tiempo de espera y desplazamiento"
        },
        "regla_2": {
            "nombre": "Congestión Horaria",
            "formato": "IF hora entre 6-9 o 17-19 THEN ×1.5",
            "justificacion": "Mayor afluencia de pasajeros"
        },
        "regla_3": {
            "nombre": "Preferencia de Transbordos",
            "formato": "IF transbordos > 2 THEN +10, IF > 1 THEN +3",
            "justificacion": "Preferencia por menos transbordos"
        }
    }


if __name__ == "__main__":
    print("Módulo de reglas cargado correctamente")
    print("Reglas disponibles:", list(REGLAS.keys()))