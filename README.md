# SAT Engine v7

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![C++](https://img.shields.io/badge/C%2B%2B-17-orange)](https://isocpp.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Motor de resolución SAT (Satisfiability) progresivo, desde backtracking NP hasta optimizaciones paralelas en C++ con pybind11 y OpenMP.

## Descripción

**SAT Engine** es una colección de solvers para el problema de satisfacibilidad booleana (SAT) implementados en Python y C++. El proyecto demuestra la evolución de algoritmos desde fuerza bruta hasta técnicas estocásticas avanzadas con paralelización.

### ¿Qué es SAT?

El problema SAT pregunta: *¿existe una asignación de valores (verdadero/falso) a variables booleanas que haga verdadera una fórmula en forma normal conjuntiva (CNF)?*

SAT fue el primer problema demostrado NP-completo (Teorema de Cook-Levin, 1971).

## Versiones

| Versión | Algoritmo | Características | Archivo |
|---------|-----------|-----------------|---------|
| **v1** | Backtracking | Fuerza bruta exhaustiva, verificación P vs resolución NP | `sat_engine_v1.py` |
| **v2** | GSAT + WalkSAT | Búsqueda estocástica local, heurísticas básicas | `sat_engine_v2.py` |
| **v3** | GSAT + Visualización | Análisis de transición de fase con gráficos matplotlib | `sat_engine_v3.py` |
| **v4** | GSAT + WalkSAT mejorado | Reinicios adaptativos, noise dinámico, dual solver | `sat_engine_v4.py` |
| **v5** | C++ Híbrido Paralelo | GSAT + WalkSAT + Simulated Annealing con OpenMP | `SAT_Engine_v5/` |

### Características por versión

#### v1 - Backtracking Exhaustivo
- Generador de instancias 3-SAT aleatorias
- Verificador polinomial O(m·k)
- Solver NP mediante backtracking recursivo
- Medición de tiempos en zonas: subcrítica (m/n=3), crítica (m/n≈4.26), supercrítica (m/n=6)

#### v2 - Búsqueda Local Estocástica
- **GSAT**: Greedy SAT, flip de variable con mayor ganancia
- **WalkSAT**: Híbrido greedy/aleatorio, selecciona cláusula insatisfecha
- Evaluación comparativa de ambos algoritmos

#### v3 - Análisis de Transición de Fase
- Parámetro de orden m/n (cláusulas/variables)
- Gráficos de probabilidad SAT, tiempo promedio, pasos de convergencia
- Identificación del umbral crítico ~4.26

#### v4 - Optimizaciones Avanzadas
- Reinicios múltiples con inicialización aleatoria
- Noise adaptativo (estilo Novelty+)
- Combinación GSAT + WalkSAT secuencial
- Detección automática de dificultad de instancia

#### v5 - Backend C++ de Alto Rendimiento
- **Tres algoritmos paralelizados** con OpenMP:
  - GSAT optimizado
  - WalkSAT con breakcount
  - Simulated Annealing con temperatura adaptativa
- **pybind11** para bindings Python-C++
- Ejecución multi-hilo configurable

## Instalación

### Requisitos

- Python 3.8 o superior
- Compilador C++17 compatible (g++/clang++/MSVC)
- OpenMP

### Dependencias Python

```bash
pip install -r requirements.txt
```

### Compilación del backend C++ (v5)

```bash
cd SAT_Engine_v5
python setup.py build_ext --inplace
```

Requisitos adicionales para v5:
- `pybind11`: `pip install pybind11`
- OpenMP (generalmente incluido en g++/MSVC)

## Uso

### Ejecutar una versión específica

```bash
# Versión 1 - Backtracking
python sat_engine_v1.py

# Versión 2 - GSAT/WalkSAT
python sat_engine_v2.py

# Versión 3 - Análisis de fase
python sat_engine_v3.py

# Versión 4 - Optimizado
python sat_engine_v4.py

# Versión 5 - C++ paralelo
cd SAT_Engine_v5 && python sat_engine_v5.py
```

### API básica

```python
# Generar instancia
from sat_engine_v2 import generate_sat_instance, gsat

clauses = generate_sat_instance(n_vars=30, n_clauses=120, k=3)

# Resolver con GSAT
solution, steps = gsat(clauses, n_vars=30, max_steps=5000)
```

### Uso del backend C++ (v5)

```python
from sat_backend import SATInstance, solve_parallel

# Crear instancia
inst = SATInstance(n_vars=40, clauses=[[1, -2, 3], [-1, 2, -3], ...])

# Resolver paralelo (8 threads, 50000 pasos máximos)
result = solve_parallel(inst, max_steps=50000, threads=8)
print(f"Solución encontrada: {result['found']}")
```

## Transición de Fase

El comportamiento de SAT exhibe una transición de fase abrupta:

- **m/n < 4.0**: Casi todas las fórmulas son SAT (satisfacibles)
- **m/n ≈ 4.26**: Punto crítico, probabilidad 50% SAT, máxima dificultad computacional
- **m/n > 4.5**: Casi todas las fórmulas son UNSAT (insatisfacibles)

![Transición de Fase](docs/images/phase_transition.png)

## Estructura del Proyecto

```
SAT-Engine-v7/
├── sat_engine_v1.py          # Backtracking básico
├── sat_engine_v2.py          # GSAT + WalkSAT
├── sat_engine_v3.py          # Análisis de fase
├── sat_engine_v4.py          # Optimizaciones avanzadas
├── SAT_Engine_v5/            # Backend C++ paralelo
│   ├── sat_backend.cpp       # Implementación C++
│   ├── sat_engine_v5.py      # Wrapper Python
│   ├── setup.py              # Build configuration
│   └── instance_generator.py # Generador de instancias
├── usados/                   # Recursos y referencias
├── docs/                     # Documentación adicional
├── requirements.txt          # Dependencias
├── LICENSE                   # Licencia MIT
└── README.md                 # Este archivo
```

## Algoritmos Implementados

| Algoritmo | Tipo | Complejidad | Descripción |
|-----------|------|-------------|-------------|
| Backtracking | Completo | O(2ⁿ) | Fuerza bruta sistemática |
| GSAT | Estocástico | O(max_steps × n × m) | Greedy local search |
| WalkSAT | Estocástico | O(max_steps × k) | Híbrido greedy/aleatorio |
| Simulated Annealing | Estocástico | O(max_steps × n) | Aceptación probabilística |

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías de contribución.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## Referencias

1. Cook, S. A. (1971). "The Complexity of Theorem-Proving Procedures"
2. Selman, B., Levesque, H., & Mitchell, D. (1992). "A New Method for Solving Hard Satisfiability Problems"
3. McAllester, D., Selman, B., & Kautz, H. (1997). "Evidence for Invariants in Local Search"
4. pybind11: https://github.com/pybind/pybind11

## Autor

Desarrollado como proyecto evolutivo de algoritmos SAT.

---

⭐ **Si este proyecto te es útil, considera darle una estrella en GitHub!**
>>>>>>> 8bb0678 (feat: initial Linux setup for SAT-Engine-v7)
