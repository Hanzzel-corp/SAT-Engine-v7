# Ejemplos de Uso Básico

## Ejemplo 1: Resolver una instancia simple

```python
from sat_engine_v2 import generate_sat_instance, gsat, walksat

# Generar instancia 3-SAT con 20 variables, 80 cláusulas
n_vars = 20
n_clauses = 80
clauses = generate_sat_instance(n_vars, n_clauses, k=3)

print(f"Instancia: {n_vars} variables, {n_clauses} cláusulas")
print(f"Primeras 3 cláusulas: {clauses[:3]}")

# Resolver con GSAT
solution_gsat, steps_gsat = gsat(clauses, n_vars, max_steps=1000)
print(f"GSAT: {'SAT' if solution_gsat else 'FAIL'} en {steps_gsat} pasos")

# Resolver con WalkSAT
solution_ws, steps_ws = walksat(clauses, n_vars, max_steps=1000, p=0.5)
print(f"WalkSAT: {'SAT' if solution_ws else 'FAIL'} en {steps_ws} pasos")
```

## Ejemplo 2: Verificar una solución

```python
from sat_engine_v1 import verify

# Supongamos que tenemos una asignación
assignment = [True, False, True, True, False]  # 5 variables

# Verificar contra cláusulas
clauses = [[1, -2, 3], [-1, 4, 5], [2, -3, -4]]

is_valid = verify(clauses, assignment)
print(f"¿La asignación satisface la fórmula? {is_valid}")
```

## Ejemplo 3: Análisis de transición de fase

```python
from sat_engine_v3 import run_phase_transition

# Ejecutar análisis completo
run_phase_transition(n_vars=30, trials=10)

# Genera gráficos de:
# - Probabilidad SAT vs m/n
# - Tiempo promedio vs m/n
# - Pasos de convergencia vs m/n
```

## Ejemplo 4: Uso del backend C++ (v5)

```python
from sat_backend import SATInstance, solve_parallel

# Crear instancia manualmente
n = 50
clauses = [
    [1, -2, 3],
    [-1, 2, -4],
    [3, 4, 5],
    # ... más cláusulas
]

inst = SATInstance(n, clauses)

# Resolver con paralelismo (4 threads)
result = solve_parallel(inst, max_steps=50000, threads=4)

if result["found"]:
    print("¡Solución encontrada!")
else:
    print("No se encontró solución en los pasos dados")
```

## Ejemplo 5: Comparar algoritmos

```python
import time
from sat_engine_v4 import gsat_restart, walksat_advanced, generate_3sat_instance

def benchmark_solver(solver_func, clauses, n_vars, name):
    start = time.time()
    result, steps = solver_func(clauses, n_vars)
    elapsed = time.time() - start
    
    print(f"{name:15} | {'SAT' if result else 'UNSAT':6} | "
          f"{steps:8} pasos | {elapsed:.4f}s")
    return result, elapsed

# Instancia de prueba
n = 40
m = 170  # ratio ~4.25 (zona crítica)
clauses = generate_3sat_instance(n, m)

print(f"Benchmark: {n} vars, {m} cláusulas (m/n={m/n:.2f})")
print("-" * 60)

benchmark_solver(gsat_restart, clauses, n, "GSAT+Restart")
benchmark_solver(walksat_advanced, clauses, n, "WalkSAT")
```

## Ejemplo 6: Generador personalizado

```python
import random

def generate_ksat_custom(n_vars, n_clauses, k, seed=None):
    """
    Generador de k-SAT con control de semilla.
    """
    if seed is not None:
        random.seed(seed)
    
    clauses = []
    for _ in range(n_clauses):
        # Seleccionar k variables distintas
        vars_selected = random.sample(range(1, n_vars + 1), k)
        
        # Asignar signos aleatorios
        clause = [v if random.random() < 0.5 else -v 
                  for v in vars_selected]
        clauses.append(clause)
    
    return clauses

# Uso
clauses = generate_ksat_custom(30, 100, 3, seed=42)
```

## Ejemplo 7: Exportar a formato DIMACS

```python
def to_dimacs(clauses, n_vars, comment=""):
    """
    Convierte cláusulas a formato DIMACS CNF.
    """
    lines = [f"c {comment}"] if comment else []
    lines.append(f"p cnf {n_vars} {len(clauses)}")
    
    for clause in clauses:
        line = " ".join(str(lit) for lit in clause) + " 0"
        lines.append(line)
    
    return "\n".join(lines)

# Uso
dimacs = to_dimacs(clauses, 20, "Instancia de prueba")
print(dimacs)
# c Instancia de prueba
# p cnf 20 3
# 1 -2 3 0
# -1 4 5 0
# ...
```
