# Changelog

Todos los cambios notables en SAT Engine serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.0.0] - 2026-04-14

### Added
- Lanzamiento inicial como SAT Engine v7
- Versión 1: Backtracking exhaustivo con verificación P vs NP
- Versión 2: GSAT y WalkSAT estocásticos
- Versión 3: Análisis de transición de fase con visualizaciones
- Versión 4: GSAT con reinicios y WalkSAT adaptativo
- Versión 5: Backend C++ con pybind11, OpenMP y solver híbrido paralelo
- Documentación completa (README, docs/, CONTRIBUTING, LICENSE)
- Ejemplos de uso en `docs/examples/`
- Archivos de configuración para GitHub

### Features
- Generador de instancias k-SAT aleatorias
- Verificador polinomial O(m·k)
- Múltiples algoritmos de resolución SAT
- Análisis de phase transition
- Backend C++ paralelizado con 3 heurísticas

## Versiones Anteriores

Las versiones v1-v6 fueron desarrolladas iterativamente como pasos de aprendizaje:

- **v1** (Foundation): Backtracking NP básico
- **v2** (Stochastic): Introducción de GSAT/WalkSAT
- **v3** (Analysis): Visualización de transición de fase
- **v4** (Optimization): Reinicios y adaptación dinámica
- **v5** (Performance): Backend C++ con paralelismo
- **v6**: (Internal development)

## Próximos Releases

### [Planned] v7.1.0
- Parser DIMACS CNF
- Tests unitarios con pytest
- Benchmarks comparativos

### [Planned] v8.0.0
- Implementación DPLL/CDCL
- Soporte CUDA/GPU
- API REST para solver remoto

---

[7.0.0]: https://github.com/Hanzzel-corp/SAT-Engine-v7/releases/tag/v7.0.0
