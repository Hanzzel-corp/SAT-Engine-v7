# Algoritmo WalkSAT

## Descripción

WalkSAT es una mejora de GSAT que introduce ruido estocástico para escapar de mínimos locales. Desarrollado por Selman, Kautz y Cohen en 1994.

## Principio de Funcionamiento

1. Selecciona una cláusula insatisfecha aleatoriamente
2. Con probabilidad `p` (noise):
   - Flip aleatorio de una variable en esa cláusula
3. Con probabilidad `1-p` (greedy):
   - Flip de la variable que causa menos conflictos (menor breakcount)

## Pseudocódigo

```
function WalkSAT(formula, n_vars, max_steps, p_noise):
    assignment = random_assignment(n_vars)
    
    for step from 1 to max_steps:
        if is_satisfied(formula, assignment):
            return assignment, step
        
        unsat_clauses = get_unsatisfied(formula, assignment)
        clause = random_choice(unsat_clauses)
        
        if random() < p_noise:
            // Random walk
            var = abs(random_choice(clause))
            flip(assignment, var)
        else:
            // Greedy - minimize breakcount
            best_var = null
            best_break = infinity
            
            for lit in clause:
                var = abs(lit)
                breaks = count_breaks(formula, assignment, var)
                if breaks < best_break:
                    best_break = breaks
                    best_var = var
            
            flip(assignment, best_var)
    
    return null, null  // failed
```

## Parámetros

| Parámetro | Descripción | Valor típico |
|-----------|-------------|--------------|
| `max_steps` | Máximo de iteraciones | 10000 - 100000 |
| `p_noise` | Probabilidad de ruido | 0.5 - 0.6 |

## Breakcount

El breakcount de una variable es el número de cláusulas que pasan de satisfechas a insatisfechas al flippear esa variable.

```
breakcount(v) = |{c ∈ clauses : c satisfecha antes, insatisfecha después de flip(v)}|
```

## Ventajas sobre GSAT

- Mejor escape de mínimos locales
- Más eficiente en instancias ruidosas
- Enfoque focalizado en cláusulas problemáticas

## Variantes

- **Novelty**: Considera la edad de las variables
- **Novelty+**: Añade probabilidad de flip completamente aleatorio
- **WalkSAT with adaptive noise**: Ajusta `p_noise` dinámicamente

## Referencias

Selman, B., Kautz, H., & Cohen, B. (1994). "Noise Strategies for Improving Local Search". AAAI 1994.

McAllester, D., Selman, B., & Kautz, H. (1997). "Evidence for Invariants in Local Search". AAAI 1997.
