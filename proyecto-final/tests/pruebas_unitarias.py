"""
Pruebas Unitarias del Sistema de Optimización de Rutas para Reparto Urbano (TSP).
Valida el correcto funcionamiento del modelo de Grafo y de los algoritmos de
Fuerza Bruta y Voraz.

Autores: Josué, Ángel, Fabiana, Gian y Jason
Curso: Análisis de Algoritmos y Estrategias de Programación
"""

import sys
import os
import unittest
import math

# Ajustar ruta de importación para encontrar el módulo src/
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from algoritmos import Grafo, resolver_tsp_fuerza_bruta, resolver_tsp_voraz


class TestSistemaRutas(unittest.TestCase):
    def setUp(self):
        """Inicializa un grafo de prueba básico para los tests."""
        self.grafo = Grafo()
        # Creamos un grafo de 4 nodos (Depósito, A, B, C) con distancias conocidas
        self.grafo.agregar_arista("Depósito", "A", 10.0)
        self.grafo.agregar_arista("Depósito", "B", 15.0)
        self.grafo.agregar_arista("Depósito", "C", 20.0)
        self.grafo.agregar_arista("A", "B", 35.0)
        self.grafo.agregar_arista("A", "C", 25.0)
        self.grafo.agregar_arista("B", "C", 30.0)

    def test_modelo_grafo(self):
        """Valida que los nodos y aristas se agreguen y consulten correctamente."""
        self.assertEqual(len(self.grafo.obtener_nodos()), 4)
        self.assertIn("Depósito", self.grafo.obtener_nodos())
        self.assertIn("A", self.grafo.obtener_nodos())
        
        # Verificar distancias agregadas
        self.assertEqual(self.grafo.obtener_distancia("Depósito", "A"), 10.0)
        self.assertEqual(self.grafo.obtener_distancia("A", "Depósito"), 10.0)  # No dirigido
        
        # Verificar distancia no existente (infinito)
        self.assertEqual(self.grafo.obtener_distancia("A", "Inexistente"), math.inf)

    def test_fuerza_bruta_optimo(self):
        """Prueba que el algoritmo de Fuerza Bruta encuentre el camino mínimo exacto."""
        # Rutas posibles y sus costos:
        # Depósito -> A -> B -> C -> Depósito: 10 + 35 + 30 + 20 = 95
        # Depósito -> A -> C -> B -> Depósito: 10 + 25 + 30 + 15 = 80  <-- MÍNIMO
        # Depósito -> B -> A -> C -> Depósito: 15 + 35 + 25 + 20 = 95
        
        ruta, costo = resolver_tsp_fuerza_bruta(self.grafo, "Depósito")
        self.assertEqual(costo, 80.0)
        self.assertEqual(ruta[0], "Depósito")
        self.assertEqual(ruta[-1], "Depósito")
        self.assertEqual(len(ruta), 5)  # Depósito -> A -> C -> B -> Depósito (5 elementos)

    def test_algoritmo_voraz_greedy(self):
        """Prueba la heurística del Vecino Más Cercano."""
        # Desde Depósito: vecinos son A(10), B(15), C(20). Elige A (10) por ser el menor.
        # Desde A: vecinos no visitados son B(35), C(25). Elige C (25) por ser el menor.
        # Desde C: único vecino no visitado es B(30). Elige B (30).
        # Desde B: no quedan no visitados. Retorna a Depósito (15).
        # Costo Total Voraz: 10 (A) + 25 (C) + 30 (B) + 15 (Retorno) = 80
        
        ruta, costo = resolver_tsp_voraz(self.grafo, "Depósito")
        self.assertEqual(costo, 80.0)
        self.assertEqual(ruta, ["Depósito", "A", "C", "B", "Depósito"])

    def test_grafo_no_conexo(self):
        """Valida que los algoritmos manejen correctamente grafos desconectados."""
        grafo_roto = Grafo()
        grafo_roto.agregar_arista("Depósito", "A", 10.0)
        grafo_roto.agregar_nodo("B")  # B está aislado
        
        ruta_fb, costo_fb = resolver_tsp_fuerza_bruta(grafo_roto, "Depósito")
        ruta_v, costo_v = resolver_tsp_voraz(grafo_roto, "Depósito")
        
        self.assertEqual(costo_fb, math.inf)
        self.assertEqual(costo_v, math.inf)


if __name__ == "__main__":
    unittest.main()
