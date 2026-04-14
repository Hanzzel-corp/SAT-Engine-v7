# Arquitectura del Proyecto

## Visión General

SAT Engine sigue una arquitectura evolutiva donde cada versión representa un nivel de optimización sobre la anterior.

```
┌─────────────────────────────────────────────────────────┐
│                    SAT Engine v7                        │
├─────────────────────────────────────────────────────────┤
│  v5 (C++ + Python)  │  v4 (Advanced Python)              │
│  ├─ pybind11        │  ├─ GSAT + Restart                 │
│  ├─ OpenMP          │  ├─ WalkSAT Adaptive               │
│  ├─ Hybrid Solver   │  └─ Dual Strategy                  │
│  └─ Parallel        │                                    │
├─────────────────────────────────────────────────────────┤
│  v3 (Analysis)      │  v2 (Stochastic)                   │
│  ├─ Phase Transition│  ├─ GSAT                           │
│  ├─ Visualization   │  └─ WalkSAT                        │
│  └─ Metrics         │                                    │
├─────────────────────────────────────────────────────────┤
│                    v1 (Foundation)                       │
│  ├─ CNF Generator   │  ├─ P Verifier                     │
│  └─ NP Backtracking │                                    │
└─────────────────────────────────────────────────────────┘
```

## Flujo de Datos

```
Entrada: (n_vars, n_clauses, k=3)
    ↓
Generador CNF ──→ Cláusulas [[1,-2,3], [-1,4,5], ...]
    ↓
┌────────────────────────────────────────┐
│  Verificador (P)                       │
│  O(m × k) - polinomial                 │
└────────────────────────────────────────┘
    ↓
Solvers (NP):
├── v1: Backtracking O(2^n)
├── v2: GSAT O(steps × n × m)
├── v3: GSAT + Análisis
├── v4: Optimizado con restart
└── v5: C++ paralelo O(steps × n × m / threads)
    ↓
Salida: Assignment {1:True, 2:False, ...} o UNSAT
```

## Componentes Principales

### 1. Generador de Instancias

**Ubicación**: `sat_engine_v*.py` (varios), `SAT_Engine_v5/instance_generator.py`

```python
def generate_cnf(n_vars, n_clauses, k=3):
    """
    Genera fórmula CNF aleatoria uniforme.
    
    Args:
        n_vars: Número de variables
        n_clauses: Número de cláusulas  
        k: Literales por cláusula (default 3)
    
    Returns:
        List[List[int]]: Lista de cláusulas
    """
```

### 2. Verificador

**Complejidad**: O(m × k) donde m = cláusulas, k = tamaño de cláusula

```python
def verify(clauses, assignment):
    """
    Verifica si assignment satisface todas las cláusulas.
    Pertenece a P (tiempo polinomial).
    """
```

### 3. Solvers

#### v1: Backtracking
- **Estrategia**: Búsqueda exhaustiva en árbol de asignaciones
- **Complejidad**: O(2^n)
- **Uso**: Instancias pequeñas (n < 20)

#### v2: GSAT
- **Estrategia**: Hill climbing greedy
- **Complejidad**: O(steps × n × m)
- **Uso**: Instancias medianas, fáciles

#### v2: WalkSAT
- **Estrategia**: Greedy + ruido estocástico
- **Complejidad**: O(steps × k)
- **Uso**: Instancias difíciles, transición de fase

#### v4: Avanzado
- **Estrategia**: GSAT con reinicios múltiples
- **Adaptación**: Noise dinámico
- **Complejidad**: O(restarts × steps × n × m)

#### v5: C++ Paralelo
- **Estrategia**: Múltiples heurísticas en paralelo
- **Paralelismo**: OpenMP con `omp parallel`
- **Cascada**: GSAT → WalkSAT → Simulated Annealing

## Backend C++ (v5)

### Estructura

```cpp
// sat_backend.cpp

struct SATInstance {
    int n_vars;
    std::vector<std::vector<int>> clauses;
};

// Algoritmos
bool gsat(const SATInstance&, std::vector<int>&, int, std::mt19937&);
bool walksat(const SATInstance&, std::vector<int>&, int, std::mt19937&);
bool anneal(const SATInstance&, std::vector<int>&, int, double, std::mt19937&);

// Solver híbrido paralelo
py::dict solve_parallel(const SATInstance&, int max_steps, int threads);
```

### Compilación

```bash
# setup.py configura pybind11 + OpenMP
python setup.py build_ext --inplace
```

### Bindings Python

```cpp
PYBIND11_MODULE(sat_backend, m) {
    py::class_<SATInstance>(m, "SATInstance")
        .def(py::init<int, std::vector<std::vector<int>>>());
    
    m.def("solve_parallel", &solve_parallel);
}
```

## Métricas y Análisis

### Transición de Fase (v3)

```python
def run_phase_transition(n_vars, trials):
    for ratio in np.linspace(1.0, 7.0, 25):
        m = int(ratio * n_vars)
        # Medir:
        # - Probabilidad SAT
        # - Tiempo promedio
        # - Pasos de convergencia
```

### Visualizaciones

- `sat_prob vs m/n`: Curva sigmoidea en α_c ≈ 4.26
- `avg_time vs m/n`: Pico en transición de fase
- `avg_steps vs m/n`: Correlación con dificultad

## Extensiones Futuras

1. **DPLL/CDCL**: Solver completo basado en conflicto
2. **CUDA**: Paralelización GPU
3. **Parser DIMACS**: Lectura de instancias estándar
4. **Incremental**: Resolución con asignaciones parciales
