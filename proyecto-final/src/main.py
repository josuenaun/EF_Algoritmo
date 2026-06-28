"""
Módulo: main.py
Descripción: Punto de entrada de la aplicación para el Sistema de Optimización de Rutas.
             Permite la simulación de datos en formato CSV, la carga de grafos,
             la ejecución interactiva de los algoritmos y la comparación empírica de rendimiento.

Integrantes del equipo de desarrollo (Ingeniería de Sistemas Computacionales):
    - Josué
    - Ángel
    - Fabiana
    - Gian
    - Jason

Curso: Análisis de Algoritmos y Estrategias de Programación
"""

import csv
import math
import os
import random
import time
from typing import Tuple, List

# Importar las estructuras y algoritmos desde algoritmos.py
from algoritmos import Grafo, resolver_tsp_fuerza_bruta, resolver_tsp_voraz


def obtener_rutas_sistema() -> Tuple[str, str]:
    """
    Define y crea de forma robusta las rutas de directorios para el proyecto.
    Retorna la ruta absoluta del directorio de datos y del archivo CSV.
    """
    # Directorio base: proyecto-final/
    directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directorio_datos = os.path.join(directorio_base, "data")
    ruta_csv = os.path.join(directorio_datos, "datos_entrada.csv")
    
    # Crear directorio data si no existe
    if not os.path.exists(directorio_datos):
        os.makedirs(directorio_datos)
        
    return directorio_datos, ruta_csv


def generar_datos_simulados(num_nodos: int, ruta_archivo: str) -> None:
    """
    Auto-genera un archivo CSV con distancias simuladas entre puntos de entrega.
    Modela los puntos en un plano cartesiano 2D y calcula la distancia euclidiana
    entre cada par de nodos para garantizar la desigualdad triangular.
    """
    if num_nodos < 2:
        raise ValueError("Se requieren al menos 2 nodos para simular un mapa de distribución.")

    # Semilla fija para consistencia en la demostración académica
    random.seed(12345)
    
    # Coordenadas aleatorias en un plano de 100 x 100 km
    coordenadas = {}
    for i in range(num_nodos):
        if i == 0:
            nombre = "Depósito"
        else:
            nombre = f"Punto_{i}"
        x = random.uniform(0.0, 100.0)
        y = random.uniform(0.0, 100.0)
        coordenadas[nombre] = (x, y)

    # Escribir la lista de aristas en el CSV
    nodos = list(coordenadas.keys())
    try:
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Origen", "Destino", "Distancia"])
            
            # Generamos un grafo completo (todos contra todos)
            for i in range(num_nodos):
                for j in range(i + 1, num_nodos):
                    n1, n2 = nodos[i], nodos[j]
                    x1, y1 = coordenadas[n1]
                    x2, y2 = coordenadas[n2]
                    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    escritor.writerow([n1, n2, round(distancia, 2)])
                    
        print(f"[OK] Archivo de datos simulados creado exitosamente en: {ruta_archivo}")
        print(f"     Se registraron {num_nodos} nodos y {num_nodos * (num_nodos - 1) // 2} aristas (distancias).")
    except Exception as e:
        print(f"[ERROR] No se pudo escribir el archivo CSV: {e}")


def cargar_grafo_desde_csv(ruta_archivo: str) -> Grafo:
    """
    Carga el grafo desde el archivo CSV.
    Cada fila representa una conexión bidireccional entre dos puntos de entrega con su respectiva distancia.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe. Genere los datos primero.")

    grafo = Grafo()
    
    with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for num_linea, fila in enumerate(lector, start=2):
            origen = fila.get("Origen")
            destino = fila.get("Destino")
            distancia_str = fila.get("Distancia")
            
            if not origen or not destino or distancia_str is None:
                print(f"[ADVERTENCIA] Fila {num_linea} incompleta en CSV. Se omitirá.")
                continue
                
            try:
                distancia = float(distancia_str)
                grafo.agregar_arista(origen, destino, distancia, bidireccional=True)
            except ValueError:
                print(f"[ADVERTENCIA] Distancia inválida en la línea {num_linea}: '{distancia_str}'. Se omitirá.")
                
    return grafo


def ejecutar_modulo_comparativo(ruta_csv: str) -> None:
    """
    Ejecuta el experimento de comparación de rendimiento (Fuerza Bruta vs Voraz)
    para diferentes tamaños de nodos e imprime la tabla comparativa por consola.
    """
    print("\n" + "=" * 115)
    print(" INICIANDO PRUEBA DE RENDIMIENTO COMPARATIVA: FUERZA BRUTA VS ALGORITMO VORAZ ".center(115, "="))
    print("=" * 115)
    
    # Tamaños de prueba definidos para el experimento
    tamanos = [4, 5, 6, 7, 8, 9, 10, 20, 50, 100]
    
    # Encabezado de la tabla comparativa
    formato_fila = "| {:<15} | {:<20} | {:<22} | {:<20} | {:<22} |"
    separador_tabla = "+" + "-"*17 + "+" + "-"*22 + "+" + "-"*24 + "+" + "-"*22 + "+" + "-"*24 + "+"
    
    print(separador_tabla)
    print(formato_fila.format("Nodos (N)", "Costo Ruta (FB)", "Tiempo Ejec. FB (s)", "Costo Ruta (Voraz)", "Tiempo Ejec. Voraz (s)"))
    print(separador_tabla)
    
    for n in tamanos:
        # Generar datos temporales para el experimento con n nodos
        ruta_temporal = ruta_csv + f".tmp_{n}"
        generar_datos_simulados(n, ruta_temporal)
        
        try:
            grafo_exp = cargar_grafo_desde_csv(ruta_temporal)
            nodos = grafo_exp.obtener_nodos()
            if not nodos:
                continue
            inicio = nodos[0] # Depósito por defecto
            
            # --- Fuerza Bruta ---
            # Se limita Fuerza Bruta a N <= 10 por la explosión combinatoria factorial
            if n <= 10:
                t0 = time.perf_counter()
                _, costo_fb = resolver_tsp_fuerza_bruta(grafo_exp, inicio)
                t1 = time.perf_counter()
                tiempo_fb_str = f"{t1 - t0:.6f}"
                costo_fb_str = f"{costo_fb:.2f}"
            else:
                costo_fb_str = "No viable (N! )"
                tiempo_fb_str = "N/A (Excesivo)"
                
            # --- Algoritmo Voraz ---
            t0 = time.perf_counter()
            _, costo_voraz = resolver_tsp_voraz(grafo_exp, inicio)
            t1 = time.perf_counter()
            tiempo_voraz_str = f"{t1 - t0:.6f}"
            costo_voraz_str = f"{costo_voraz:.2f}"
            
            # Imprimir fila con resultados
            print(formato_fila.format(n, costo_fb_str, tiempo_fb_str, costo_voraz_str, tiempo_voraz_str))
            
        except Exception as e:
            print(f"| Error en tamaño {n:<6} | Ocurrió un error inesperado al procesar: {str(e):<71} |")
        finally:
            # Limpieza del archivo temporal
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
                
    print(separador_tabla)
    print("Nota: El enfoque de Fuerza Bruta no se ejecuta para N > 10 debido a que requiere O(N!) operaciones,")
    print("      lo cual colapsaría la memoria y el procesador de la máquina de demostración en tiempo de exposición.")
    print("=" * 115 + "\n")


def mostrar_menu_principal() -> None:
    """
    Despliega la interfaz de consola interactiva en español.
    """
    _, ruta_csv = obtener_rutas_sistema()
    
    while True:
        print("=" * 65)
        print(" SISTEMA DE OPTIMIZACIÓN DE RUTAS DE REPARTO URBANO (TSP) ".center(65))
        print(" Curso: Análisis de Algoritmos - Proyecto Final ".center(65))
        print(" Integrantes: Josué, Ángel, Fabiana, Gian y Jason ".center(65))
        print("=" * 65)
        print(" 1. Generar nuevo archivo CSV de datos de entrada simulados")
        print(" 2. Cargar grafo desde CSV y resolver rutas específicas")
        print(" 3. Ejecutar tabla de resultados comparativos (Demostración)")
        print(" 4. Registrar punto de entrega manual en el grafo y calcular")
        print(" 5. Salir del programa")
        print("-" * 65)
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            print("\n--- Generación de Datos de Entrada ---")
            try:
                nodos_input = input("Ingrese la cantidad de puntos de entrega a simular (ej. 20): ").strip()
                n = int(nodos_input)
                if n < 2:
                    print("[Error] Se necesitan al menos 2 nodos para la simulación.")
                else:
                    generar_datos_simulados(n, ruta_csv)
            except ValueError:
                print("[Error] Por favor, ingrese un número entero válido.")
            print()
            
        elif opcion == "2":
            print("\n--- Carga de Grafo y Resolución de Ruta ---")
            if not os.path.exists(ruta_csv):
                print(f"[Alerta] El archivo CSV ({ruta_csv}) no existe.")
                print("Por favor, ejecute la opción 1 para generar datos de prueba.")
                print()
                continue
                
            try:
                grafo = cargar_grafo_desde_csv(ruta_csv)
                nodos = grafo.obtener_nodos()
                print(f"[OK] Grafo cargado exitosamente. Nodos encontrados: {len(nodos)}")
                print(f"Puntos de entrega: {', '.join(nodos)}")
                
                inicio = input(f"Seleccione el punto de partida (Depósito por defecto, Enter para confirmar): ").strip()
                if not inicio:
                    inicio = "Depósito"
                
                if inicio not in nodos:
                    print(f"[Error] El punto '{inicio}' no existe en el grafo cargado.")
                    print()
                    continue
                
                # Ejecutar Fuerza Bruta si N es razonable
                if len(nodos) <= 10:
                    print("\nCalculando ruta exacta con Fuerza Bruta...")
                    t0 = time.perf_counter()
                    ruta_fb, costo_fb = resolver_tsp_fuerza_bruta(grafo, inicio)
                    t1 = time.perf_counter()
                    print(f"-> Ruta Óptima (FB): {' -> '.join(ruta_fb)}")
                    print(f"-> Costo Total (Distancia): {costo_fb:.2f} km")
                    print(f"-> Tiempo de cómputo: {t1 - t0:.6f} segundos")
                else:
                    print(f"\n[Aviso] Nodos = {len(nodos)}. Fuerza Bruta omitido para evitar cuelgues (Complejidad O(N!)).")
                
                # Ejecutar Algoritmo Voraz
                print("\nCalculando ruta con Algoritmo Voraz (Vecino Más Cercano)...")
                t0 = time.perf_counter()
                ruta_v, costo_v = resolver_tsp_voraz(grafo, inicio)
                t1 = time.perf_counter()
                if costo_v == math.inf:
                    print("-> [Error] No se pudo encontrar una ruta voraz válida. ¿El grafo es conexo?")
                else:
                    print(f"-> Ruta Sugerida (Voraz): {' -> '.join(ruta_v)}")
                    print(f"-> Costo Total (Distancia): {costo_v:.2f} km")
                    print(f"-> Tiempo de cómputo: {t1 - t0:.6f} segundos")
                
            except Exception as e:
                print(f"[Error] Ocurrió un error al procesar el grafo: {e}")
            print()
            
        elif opcion == "3":
            ejecutar_modulo_comparativo(ruta_csv)
            
        elif opcion == "4":
            print("\n--- Registro Manual de Punto de Entrega ---")
            # Para permitir probar la flexibilidad del grafo
            grafo_manual = Grafo()
            print("Vamos a construir un grafo manual pequeño. Ingrese las conexiones.")
            print("Escriba 'FIN' en el nombre del origen para terminar de ingresar.")
            
            while True:
                orig = input("Nombre del punto origen (ej. A): ").strip()
                if orig.upper() == "FIN":
                    break
                dest = input("Nombre del punto destino (ej. B): ").strip()
                dist_str = input("Distancia o tiempo de traslado (ej. 12.5): ").strip()
                try:
                    dist = float(dist_str)
                    grafo_manual.agregar_arista(orig, dest, dist)
                    print(f"[OK] Conectado {orig} <-> {dest} con distancia {dist}")
                except ValueError:
                    print("[Error] Distancia no válida. Intente de nuevo.")
            
            nodos_manual = grafo_manual.obtener_nodos()
            if len(nodos_manual) < 2:
                print("[Error] El grafo debe tener al menos 2 nodos para calcular una ruta.")
                print()
                continue
                
            print(f"\nNodos registrados: {', '.join(nodos_manual)}")
            inicio_manual = input(f"Ingrese nodo inicial ({nodos_manual[0]} por defecto): ").strip()
            if not inicio_manual:
                inicio_manual = nodos_manual[0]
                
            if inicio_manual not in nodos_manual:
                print(f"[Error] El nodo '{inicio_manual}' no existe en su lista.")
                print()
                continue
                
            # Resolver
            print("\nCalculando en Grafo Manual...")
            rf, cf = resolver_tsp_fuerza_bruta(grafo_manual, inicio_manual)
            print(f"-> Ruta Óptima (Fuerza Bruta): {' -> '.join(rf)} (Costo: {cf:.2f})")
            
            rv, cv = resolver_tsp_voraz(grafo_manual, inicio_manual)
            print(f"-> Ruta Heurística (Voraz): {' -> '.join(rv)} (Costo: {cv:.2f})")
            print()
            
        elif opcion == "5":
            print("\nGracias por utilizar el optimizador de rutas de reparto urbano.")
            print("Cerrando sistema. Éxitos en la sustentación del proyecto final.")
            break
        else:
            print("[Error] Opción inválida. Seleccione un número entre 1 y 5.\n")


if __name__ == "__main__":
    mostrar_menu_principal()
