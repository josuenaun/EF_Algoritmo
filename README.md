# Sistema de Optimización de Rutas para Reparto Urbano (TSP)

Este proyecto corresponde al **Proyecto Final** de la asignatura **Análisis de Algoritmos y Estrategias de Programación** de la carrera de **Ingeniería de Sistemas Computacionales**.

### Integrantes del Equipo
*   **Josué**
*   **Ángel**
*   **Fabiana**
*   **Gian**
*   **Jason**

---

## 1. Justificación de la Estrategia Algorítmica

El problema de diseñar rutas de reparto eficientes es una variante directa del **Problema del Viajante de Comercio (TSP - Travelling Salesperson Problem)**, un problema clásico clasificado como **NP-hard** en la teoría de la complejidad computacional. Esto significa que no se conoce ningún algoritmo que pueda resolverlo de forma exacta en tiempo polinomial.

Para abordar este desafío, el equipo ha seleccionado estratégicamente dos enfoques contrapuestos que representan el balance fundamental de la ingeniería de software:

1.  **Fuerza Bruta (Resolución Exacta):** Garantiza encontrar el óptimo global absoluto al examinar todo el espacio de soluciones. Sin embargo, su costo computacional es factorial, lo que restringe su uso a instancias pequeñas (ej. $N \le 10$). Este enfoque establece la "línea de base" de optimalidad del sistema.
2.  **Algoritmo Voraz / Greedy (Aproximación Heurística - Vecino Más Cercano):** Sacrifica la garantía de optimalidad global a cambio de un tiempo de respuesta instantáneo y polinomial ($O(N^2)$). Es la solución de producción viable para escenarios de gran escala (ej. 20, 50 o 100 puntos de entrega).

La comparación de ambas estrategias permite evaluar cuantitativamente la pérdida de calidad de la solución (el "gap" heurístico) frente a la ganancia en eficiencia temporal.

---

## 2. Análisis de Complejidad Asintótica (Big O)

### 2.1. Algoritmo de Fuerza Bruta

#### Complejidad Temporal: $O(N \cdot N!)$
Para un grafo de $N$ nodos, fijamos el nodo inicial (depósito). Debemos evaluar todos los circuitos hamiltonianos posibles que recorren los restantes $N - 1$ nodos intermedios. El número de permutaciones posibles de estos nodos intermedios es:
$$P(N-1) = (N-1)!$$
Para cada una de las permutaciones generadas, el algoritmo realiza un ciclo para sumar las distancias entre nodos consecutivos en el camino y retornar al origen, lo cual requiere $N$ operaciones de consulta. Por tanto, el número total de operaciones básicas está acotado por:
$$T(N) = N \cdot (N-1)! = N!$$
En términos de notación asintótica, el crecimiento es estrictamente de orden **$O(N \cdot N!)$** (o simplemente **$O(N!)$**). 

#### ¿Por qué colapsa en Fuerza Bruta?
La tasa de crecimiento de la función factorial es extremadamente explosiva. Observemos el número de operaciones requeridas según el tamaño de la instancia:
*   Para $N = 5$: $5! = 120$ operaciones (instantáneo).
*   Para $N = 10$: $10! = 3,628,800$ operaciones (~1.2 segundos).
*   Para $N = 20$: $20! \approx 2.43 \times 10^{18}$ operaciones. 
    *   *Nota de cálculo:* Un supercomputador moderno ejecutando a $10^{15}$ operaciones por segundo (1 PetaFLOP) tardaría aproximadamente **40.5 minutos** en resolverlo. Una computadora estándar de escritorio (CPU de 3 GHz) tardaría más de **25 años**.

#### Complejidad Espacial: $O(N)$
El algoritmo almacena en memoria la lista del mejor camino encontrado ($O(N)$) y la permutación que está siendo evaluada en el instante actual ($O(N)$). Las permutaciones pueden generarse de manera perezosa (lazy evaluation) mediante generadores en Python (`itertools.permutations`), manteniendo el consumo espacial estrictamente lineal respecto al número de nodos.

---

### 2.2. Algoritmo Voraz (Greedy - Vecino Más Cercano)

#### Complejidad Temporal: $O(N^2)$
El algoritmo parte del nodo inicial y construye la ruta paso a paso mediante decisiones locales e irrevocables:
1.  En el paso $k$ (desde $k=1$ hasta $N-1$), el repartidor se encuentra en un nodo y debe decidir cuál de los $N - k$ nodos restantes no visitados es el más cercano.
2.  Para tomar esta decisión local, se comparan las distancias hacia todos los vecinos que aún no pertenecen a la ruta recorrida. Esto toma $N-k$ comparaciones.
3.  El número total de comparaciones de aristas viene dado por la suma aritmética:
$$S(N) = \sum_{k=1}^{N-1} (N-k) = (N-1) + (N-2) + \dots + 1 = \frac{N(N-1)}{2} = \frac{N^2 - N}{2}$$
Asintóticamente, el término dominante es $N^2$, lo que resulta en una complejidad temporal de **$O(N^2)$** en el peor y mejor caso.

#### Eficiencia para Instancias Grandes
*   Para $N = 100$ nodos: $S(100) \approx 4,950$ comparaciones básicas, ejecutándose en fracciones de milisegundo ($<0.001$ segundos).
*   Para $N = 1000$ nodos: $S(1000) \approx 499,500$ comparaciones básicas, completándose en menos de $0.05$ segundos.

#### Complejidad Espacial: $O(N)$
Se requiere almacenar la lista de nodos visitados (representada como un conjunto `Set` para búsquedas en tiempo promedio $O(1)$) y el camino resultante en un arreglo de tamaño $N+1$. Por ende, la ocupación en memoria es lineal, **$O(N)$**.

---

## 3. Guía de Instalación y Ejecución

### Requisitos Previos
*   Python 3.8 o superior instalado en el sistema.
*   No se requieren librerías externas (se utilizan únicamente módulos estándar de Python como `csv`, `math`, `time` e `itertools` para asegurar la portabilidad e independencia del código).

### Instalación
1.  Descargue o clone el repositorio en su máquina local:
    ```bash
    git clone <url-del-repositorio>
    cd proyecto-final
    ```

2.  Asegúrese de respetar la siguiente estructura de carpetas:
    ```plaintext
    proyecto-final/
    ├── README.md
    ├── data/
    │   └── datos_entrada.csv
    └── src/
        ├── main.py
        └── algoritmos.py
    ```

### Instrucciones de Ejecución
1.  Abra una terminal o consola de comandos (PowerShell, CMD o Terminal de Linux/macOS).
2.  Navegue hasta el directorio `src/` del proyecto:
    ```bash
    cd src
    ```
3.  Ejecute el script principal `main.py`:
    ```bash
    python main.py
    ```

---

## 4. Funcionamiento del Sistema de Consola Interactivo

Al iniciar la ejecución de `main.py`, se presentará un menú interactivo en español con las siguientes opciones:

1.  **Generar nuevo archivo CSV de datos de entrada simulados:** Permite ingresar un número de nodos (ej. 20, 50, 100). El sistema generará automáticamente coordenadas espaciales aleatorias y creará el archivo `data/datos_entrada.csv` con todas las distancias calculadas bajo el modelo euclidiano.
2.  **Cargar grafo desde CSV y resolver rutas específicas:** Lee el archivo `datos_entrada.csv`, muestra al usuario los nodos disponibles en la red y permite seleccionar un nodo de partida. Si el número de nodos es menor o igual a 10, ejecutará tanto Fuerza Bruta como Voraz para comparar resultados. Si supera los 10 nodos, resolverá de forma instantánea usando únicamente el algoritmo Voraz para evitar cuelgues del procesador.
3.  **Ejecutar tabla de resultados comparativos (Demostración):** Ejecuta un experimento automatizado sobre instancias de tamaños crecientes: $N \in \{4, 5, 6, 7, 8, 9, 10, 20, 50, 100\}$. Imprime directamente en la consola la tabla comparativa con los costos de ruta y tiempos exactos de cálculo para cada enfoque.
4.  **Registrar punto de entrega manual en el grafo:** Permite ingresar manualmente conexiones de un grafo arbitrario (ej. ingresar conexiones `A-B` con costo `10`), ideal para validar ejercicios teóricos explicados en clase.
5.  **Salir del programa.**
