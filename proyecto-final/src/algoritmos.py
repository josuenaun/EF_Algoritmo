"""
Módulo: algoritmos.py
Descripción: Contiene las estructuras de datos y algoritmos de optimización para el reparto urbano.
             Implementa el modelamiento de la ciudad como un Grafo y las soluciones al
             Problema del Viajante de Comercio (TSP) mediante Fuerza Bruta y Algoritmo Voraz.

Autores: Josué, Ángel, Fabiana, Gian y Jason
Curso: Análisis de Algoritmos y Estrategias de Programación
"""

import itertools
import math
from typing import Dict, List, Set, Tuple, Optional


class Grafo:
    """
    Representa un Grafo no dirigido ponderado para modelar los puntos de entrega de la ciudad.
    Utiliza una representación interna de Lista de Adyacencia mediante diccionarios anidados.
    """

    def __init__(self) -> None:
        # Estructura: {nodo_origen: {nodo_destino: peso_distancia}}
        self._adyacencia: Dict[str, Dict[str, float]] = {}

    def agregar_nodo(self, nodo: str) -> None:
        """
        Registra un nuevo punto de entrega en el grafo si no existe previamente.
        """
        if nodo not in self._adyacencia:
            self._adyacencia[nodo] = {}

    def agregar_arista(self, origen: str, destino: str, peso: float, bidireccional: bool = True) -> None:
        """
        Establece una conexión (arista) ponderada entre dos puntos de entrega.
        Si alguno de los nodos no está registrado, lo agrega automáticamente.
        """
        if peso < 0:
            raise ValueError("El peso (distancia/tiempo) de una arista no puede ser negativo.")

        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        self._adyacencia[origen][destino] = peso
        if bidireccional:
            self._adyacencia[destino][origen] = peso

    def obtener_distancia(self, origen: str, destino: str) -> float:
        """
        Retorna la distancia o costo entre dos nodos adyacentes.
        Si no existe conexión directa, retorna infinito (math.inf).
        """
        if origen in self._adyacencia and destino in self._adyacencia[origen]:
            return self._adyacencia[origen][destino]
        return math.inf

    def obtener_nodos(self) -> List[str]:
        """
        Retorna la lista de todos los puntos de entrega registrados en el grafo.
        """
        return list(self._adyacencia.keys())

    def obtener_vecinos(self, nodo: str) -> Dict[str, float]:
        """
        Retorna los vecinos adyacentes a un nodo dado y sus respectivos pesos.
        """
        return self._adyacencia.get(nodo, {})

    def verificar_conectividad(self) -> bool:
        """
        Verifica si el grafo es conexo (existe un camino entre cualquier par de nodos).
        Utiliza una búsqueda a lo ancho (BFS) para la verificación.
        """
        nodos = self.obtener_nodos()
        if not nodos:
            return True

        visitados: Set[str] = set()
        cola: List[str] = [nodos[0]]
        visitados.add(nodos[0])

        while cola:
            actual = cola.pop(0)
            for vecino in self.obtener_vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        return len(visitados) == len(nodos)


def resolver_tsp_fuerza_bruta(grafo: Grafo, inicio: str) -> Tuple[List[str], float]:
    """
    Resuelve el Problema del Viajante de Comercio (TSP) usando el enfoque de Fuerza Bruta.
    Explora todas las permutaciones posibles de los nodos restantes para encontrar la ruta óptima exacta.

    Complejidad Temporal: O(N!) - donde N es el número total de nodos.
    Complejidad Espacial: O(N) - para almacenar el camino y las variables de control.
    
    Parámetros:
        grafo: Instancia de la clase Grafo que representa la ciudad.
        inicio: Nodo de origen (depósito o punto de partida).

    Retorna:
        Una tupla (ruta_optima, costo_minimo) donde:
            - ruta_optima: Lista de nodos en el orden de visita (inicia y termina en 'inicio').
            - costo_minimo: La distancia total de la ruta óptima. Si no hay ruta válida, retorna ([], math.inf).
    """
    nodos = grafo.obtener_nodos()
    if inicio not in nodos:
        return [], math.inf

    # Nodos a visitar excluyendo el nodo inicial
    nodos_intermedios = [nodo for nodo in nodos if nodo != inicio]
    
    # Si solo está el nodo de origen, la ruta es regresar a él mismo con costo 0
    if not nodos_intermedios:
        return [inicio, inicio], 0.0

    costo_minimo = math.inf
    ruta_optima: List[str] = []

    # Generamos todas las permutaciones de los nodos restantes
    for permutacion in itertools.permutations(nodos_intermedios):
        costo_actual = 0.0
        nodo_actual = inicio
        es_ruta_valida = True

        # Calcular costo de la ruta sugerida por la permutación
        for siguiente_nodo in permutacion:
            dist = grafo.obtener_distancia(nodo_actual, siguiente_nodo)
            if dist == math.inf:
                es_ruta_valida = False
                break
            costo_actual += dist
            nodo_actual = siguiente_nodo

        # Agregar el retorno al punto de partida
        if es_ruta_valida:
            dist_retorno = grafo.obtener_distancia(nodo_actual, inicio)
            if dist_retorno == math.inf:
                es_ruta_valida = False
            else:
                costo_actual += dist_retorno

        # Si encontramos un costo estrictamente menor, actualizamos la ruta óptima
        if es_ruta_valida and costo_actual < costo_minimo:
            costo_minimo = costo_actual
            ruta_optima = [inicio] + list(permutacion) + [inicio]

    return ruta_optima, costo_minimo


def resolver_tsp_voraz(grafo: Grafo, inicio: str) -> Tuple[List[str], float]:
    """
    Resuelve el Problema del Viajante de Comercio (TSP) usando un Enfoque Voraz (Greedy).
    Aplica la heurística del "Vecino Más Cercano": en cada paso, selecciona el punto de entrega
    no visitado que se encuentre a menor distancia del punto actual.

    Complejidad Temporal: O(N^2) - donde N es el número total de nodos.
    Complejidad Espacial: O(N) - para la estructura de nodos visitados y el camino resultante.

    Parámetros:
        grafo: Instancia de la clase Grafo que representa la ciudad.
        inicio: Nodo de origen (depósito o punto de partida).

    Retorna:
        Una tupla (ruta_sugerida, costo_total) donde:
            - ruta_sugerida: Lista de nodos en el orden de visita (inicia y termina en 'inicio').
            - costo_total: La distancia total de la ruta sugerida. Si no hay ruta válida, retorna ([], math.inf).
    """
    nodos = grafo.obtener_nodos()
    if inicio not in nodos:
        return [], math.inf

    visitados: Set[str] = {inicio}
    ruta: List[str] = [inicio]
    costo_total = 0.0
    nodo_actual = inicio

    while len(visitados) < len(nodos):
        vecinos = grafo.obtener_vecinos(nodo_actual)
        proximo_nodo: Optional[str] = None
        distancia_minima = math.inf

        # Estrategia Voraz: Buscar el vecino no visitado con menor distancia
        for vecino, peso in vecinos.items():
            if vecino not in visitados:
                if peso < distancia_minima:
                    distancia_minima = peso
                    proximo_nodo = vecino

        # Si no encontramos ningún vecino accesible no visitado, el algoritmo falla (grafo no conexo)
        if proximo_nodo is None:
            return [], math.inf

        # Realizar el movimiento (decisión voraz irrevocable)
        visitados.add(proximo_nodo)
        ruta.append(proximo_nodo)
        costo_total += distancia_minima
        nodo_actual = proximo_nodo

    # Retorno al nodo de origen para completar el circuito Hamiltoniano
    dist_retorno = grafo.obtener_distancia(nodo_actual, inicio)
    if dist_retorno == math.inf:
        return [], math.inf

    costo_total += dist_retorno
    ruta.append(inicio)

    return ruta, costo_total
