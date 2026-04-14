# Algoritmo GSAT

## Descripción

GSAT (Greedy SAT) es un algoritmo de búsqueda local estocástica para resolver problemas SAT. Fue introducido por Selman, Levesque y Mitchell en 1992.

## Principio de Funcionamiento

1. **Inicialización**: Asignación aleatoria de valores a todas las variables
2. **Iteración**: En cada paso, evalúa el "gain" (ganancia) de flippear cada variable
3. **Selección**: Elije la variable que maximiza el número de cláusulas satisfechas
4. **Flip**: Invierte el valor de la variable seleccionada

## Pseudocódigo

```
function GSAT(formula, n_vars, max_steps):
    assignment = random_assignment(n_vars)
    
    for step from 1 to max_steps:
        if is_satisfied(formula, assignment):
            return assignment, step
        
        best_var = null
        best_score = -infinity
        
        for var from 1 to n_vars:
            flip(assignment, var)
            score = count_satisfied(formula, assignment)
            flip(assignment, var)  // undo
            
            if score > best_score:
                best_score = score
                best_var = var
        
        flip(assignment, best_var)
    
    return null, null  // failed
```

## Complejidad

- **Tiempo por iteración**: O(n × m) donde n = variables, m = cláusulas
- **Espacio**: O(n) para la asignación

## Ventajas

- Simple de implementar
- Converge rápido en instancias fáciles
- Determinístico una vez iniciado (excepto inicialización)

## Desventajas

- Puede quedar atrapado en mínimos locales
- No tiene mecanismo de escape
- Peor que WalkSAT en instancias difíciles

## Variantes

- **GSAT with Restart**: Reinicio con nueva asignación aleatoria tras estancamiento
- **GSAT with Random Walk**: Probabilidad pequeña de flip aleatorio

## Referencias

Selman, B., Levesque, H., & Mitchell, D. (1992). "A New Method for Solving Hard Satisfiability Problems". AAAI 1992.
