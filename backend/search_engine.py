"""
MOTOR DE BÚSQUEDA A*
"""

import heapq
from typing import List, Tuple, Optional, Dict
from backend.knowledge_base import (
    grafo, 
    obtener_conexiones, 
    calcular_distancia_euclidiana,
    estaciones
)
from backend.rules import (
    aplicar_todas_reglas,
    regla_heuristica_adaptativa,
    regla_ruta_nocturna,
    regla_costo_congestion
)


class NodoBusqueda:
    def __init__(self, estacion: str, ruta: Optional[str], 
                 costo_g: float, camino: List[str], 
                 transbordos: int, hora: Optional[float] = None):
        self.estacion = estacion
        self.ruta = ruta
        self.costo_g = costo_g
        self.camino = camino.copy()
        self.transbordos = transbordos
        self.hora = hora
    
    def __lt__(self, other):
        return self.costo_g < other.costo_g


def a_star(inicio: str, objetivo: str, hora: Optional[float] = None) -> Tuple[Optional[List[str]], float, int, int]:
    """Algoritmo A* para encontrar la ruta óptima"""
    
    if inicio not in estaciones or objetivo not in estaciones:
        return None, float('inf'), None, 0
    
    if inicio == objetivo:
        return [inicio], 0, 0, 0
    
    cola_prioridad = []
    nodo_inicial = NodoBusqueda(
        estacion=inicio,
        ruta=None,
        costo_g=0,
        camino=[inicio],
        transbordos=0,
        hora=hora
    )
    
    h_inicial = calcular_distancia_euclidiana(inicio, objetivo)
    f_inicial = nodo_inicial.costo_g + h_inicial
    
    heapq.heappush(cola_prioridad, (f_inicial, nodo_inicial))
    visitados: Dict[Tuple[str, Optional[str]], float] = {}
    nodos_explorados = 0
    
    while cola_prioridad:
        f_actual, nodo_actual = heapq.heappop(cola_prioridad)
        nodos_explorados += 1
        
        if nodo_actual.estacion == objetivo:
            return (nodo_actual.camino, 
                    round(nodo_actual.costo_g, 2), 
                    nodo_actual.transbordos, 
                    nodos_explorados)
        
        estado_actual = (nodo_actual.estacion, nodo_actual.ruta)
        if estado_actual in visitados and visitados[estado_actual] <= nodo_actual.costo_g:
            continue
        visitados[estado_actual] = nodo_actual.costo_g
        
        for vecino, ruta_vecino, tiempo_base in obtener_conexiones(nodo_actual.estacion):
            if hora is not None:
                if not regla_ruta_nocturna(hora, ruta_vecino):
                    continue
            
            reglas_aplicadas = aplicar_todas_reglas(
                nodo_actual.ruta, 
                ruta_vecino, 
                nodo_actual.transbordos,
                hora
            )
            
            if hora is not None:
                factor_congestion = regla_costo_congestion(hora)
                tiempo_ajustado = tiempo_base * factor_congestion
            else:
                tiempo_ajustado = tiempo_base
            
            nuevo_costo_g = nodo_actual.costo_g + tiempo_ajustado + reglas_aplicadas["costo_total_adicional"]
            
            nuevos_transbordos = nodo_actual.transbordos
            if nodo_actual.ruta is not None and nodo_actual.ruta != ruta_vecino:
                nuevos_transbordos += 1
            
            distancia_base = calcular_distancia_euclidiana(vecino, objetivo)
            heuristica = regla_heuristica_adaptativa(distancia_base, nuevos_transbordos)
            nuevo_f = nuevo_costo_g + heuristica
            
            nuevo_nodo = NodoBusqueda(
                estacion=vecino,
                ruta=ruta_vecino,
                costo_g=nuevo_costo_g,
                camino=nodo_actual.camino + [vecino],
                transbordos=nuevos_transbordos,
                hora=hora
            )
            
            heapq.heappush(cola_prioridad, (nuevo_f, nuevo_nodo))
    
    return None, float('inf'), None, nodos_explorados


def obtener_ruta_detallada(ruta: List[str]) -> List[Dict]:
    """Obtiene información detallada de cada paso"""
    if not ruta or len(ruta) < 2:
        return []
    
    detalles = []
    ruta_actual = None
    
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i + 1]
        
        ruta_encontrada = None
        tiempo = None
        
        for vecino, ruta_vecino, tiempo_base in obtener_conexiones(origen):
            if vecino == destino:
                ruta_encontrada = ruta_vecino
                tiempo = tiempo_base
                break
        
        es_transbordo = (ruta_actual is not None and ruta_actual != ruta_encontrada)
        
        detalles.append({
            "desde": origen,
            "hasta": destino,
            "ruta": ruta_encontrada,
            "tiempo": tiempo,
            "es_transbordo": es_transbordo,
            "paso": i + 1
        })
        
        ruta_actual = ruta_encontrada
    
    return detalles


def formatear_resultado(inicio: str, objetivo: str, ruta: List[str], 
                        costo: float, transbordos: int, nodos_explorados: int) -> Dict:
    """Formatea el resultado para la API"""
    if ruta is None:
        return {
            "exito": False,
            "origen": inicio,
            "destino": objetivo,
            "mensaje": f"No se encontró ruta entre '{inicio}' y '{objetivo}'",
            "nodos_explorados": nodos_explorados
        }
    
    detalles_pasos = obtener_ruta_detallada(ruta)
    
    return {
        "exito": True,
        "origen": inicio,
        "destino": objetivo,
        "ruta": ruta,
        "costo_total_minutos": round(costo, 2),
        "numero_transbordos": transbordos,
        "detalles_pasos": detalles_pasos,
        "nodos_explorados": nodos_explorados,
        "tiempo_estimado": f"{round(costo, 2)} minutos",
        "mensaje": f"Ruta encontrada con {transbordos} transbordo(s)"
    }


if __name__ == "__main__":
    print("Motor de búsqueda A* cargado correctamente")