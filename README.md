<<<<<<< HEAD
📄 SAT Engine v7 — A Hybrid Local-Search Laboratory for Phase-Transition Analysis in Random 3-SAT
Technical Report — Hanzzel Corp ∑Δ9 (José Zamora)
Abstract

Random 3-SAT exhibits a well-defined computational phase transition:
a narrow critical region where instances abruptly change from almost always satisfiable to almost always unsatisfiable, and where solver performance deteriorates dramatically.
This behavior mirrors physical systems near critical points and is considered one of the strongest empirical indicators of structural hardness in NP-complete problems.

SAT Engine v7 implements a hybrid solver architecture combining stochastic local search, gradient-based heuristics, probabilistic flips, multi-restart strategies and a C++ backend optimized with OpenMP.
The engine generates controlled random instances, sweeps density ratios 
𝑚
/
𝑛
m/n, and empirically reconstructs the phase-transition curve associated with the SAT threshold.

The platform is designed as an experimental testbed for studying the phenomenology behind P vs NP from the computational and statistical-physics perspective.

1. Introduction

The satisfiability problem (SAT) is the canonical NP-complete problem and the gateway into the P vs NP question.
While theoretical formulations rely on reductions and asymptotic complexity, the empirical structure of SAT—particularly its transition behavior—reveals deeper insights into the nature of computational hardness.

Random 3-SAT is known to undergo a sharp transition around a critical clause-to-variable ratio.
This threshold behaves analogously to physical phase transitions, displaying:

sudden drop in satisfiability,

divergence in solver runtimes,

metastable states in search dynamics,

sensitivity to noise and initial conditions.

SAT Engine v7 was built to reproduce and analyze these phenomena systematically.

2. System Overview

SAT Engine v7 consists of three layers:

2.1 Instance Generator

Produces random 3-SAT instances with controlled density 
𝛼
=
𝑚
/
𝑛
α=m/n.
Supports batch sampling, reproducible seeds, and fine-grained sweeps.

2.2 Hybrid Solver (C++ backend)

A high-performance implementation using:

OpenMP parallelism,

probabilistic neighborhood exploration,

GSAT-style gradient moves,

WalkSAT-style random flips,

multi-restart strategies,

early conflict detection.

Compiled as a Python extension (.pyd), it allows fast experimentation without leaving Python’s environment.

2.3 Python Analysis Layer

Provides:

density sweeps,

empirical SAT-rate estimation,

runtime profiling,

solver-stability measurement,

transition-curve reconstruction.

3. Methodology

Each sweep consists of:

Select variable count 
𝑛
n.

Sweep density ratio 
𝛼
=
𝑚
/
𝑛
α=m/n over a predefined range.

For each 
𝛼
α, generate 
𝑘
k independent instances.

Apply the hybrid solver with fixed computational budget.

Record:

satisfiable fraction,

average runtime,

median runtime,

number of restarts required.

The result is an empirical complexity curve mapping the search-space landscape as constraints accumulate.

4. Empirical Results

SAT Engine v7 reproduces the classical behavior:

4.1 Low-density regime (easy phase)

Instances overwhelmingly satisfiable.
Local search converges rapidly; runtime grows sublinearly.

4.2 Critical regime (phase transition)

Around 
𝛼
≈
4.2
α≈4.2, the system exhibits:

collapse in SAT probability,

order-of-magnitude runtime increases,

metastability in solver trajectories,

sensitivity to the choice of flips,

abrupt shifts in solution-space structure.

This regime constitutes the empirical “hard core” of the SAT problem.

4.3 High-density regime (overconstrained)

Instances predominantly unsatisfiable.
Solvers detect contradictions early, but local minima proliferate.

5. Significance for P vs NP

Although P vs NP is formally a question about asymptotic worst-case behavior, empirical studies reveal patterns suggesting deep structural barriers:

hardness concentrates in a narrow region, not uniformly,

solver performance degrades systematically at the same density threshold,

the landscape behaves like a physical system near criticality.

If a polynomial-time solver existed for SAT, it would necessarily handle this critical region efficiently.
Every empirical study—including SAT Engine v7—suggests instead that this region resists all known algorithmic paradigms.

SAT Engine v7 thus serves as a computational microscope into the structure of NP-complete problems.

6. Architecture Diagram
SAT Engine v7
│
├── Instance Generator
│     └── Random 3-SAT (n, m = αn)
│
├── Hybrid Solver (C++ / OpenMP)
│     ├── GSAT moves
│     ├── WalkSAT flips
│     ├── stochastic perturbations
│     ├── multi-restart control
│     └── early conflict pruning
│
└── Python Analysis Layer
      ├── density sweep
      ├── SAT-rate estimation
      ├── runtime curve
      └── transition-curve visualization

7. Reproducibility
Compile backend
python setup.py build_ext --inplace

Run full sweep
python sat_engine_v5.py

8. Conclusion

SAT Engine v7 demonstrates that computational hardness in SAT is not random but emergent.
The phase transition appears consistently across solvers, seeds, and architectures.
This universality strongly suggests that the difficulty of SAT—and by extension NP-complete problems—arises from deep structural regularities rather than incidental instance design.

The project provides a platform for systematic exploration of:

hardness landscapes,

solver decay dynamics,

critical-point phenomenology,

empirical complexity theory.

Author

José Zamora — Hanzzel Corp ∑Δ9
Experimental computational mathematics, hybrid solvers, and emergent-complexity modeling.
=======
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
