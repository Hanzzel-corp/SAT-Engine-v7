# Guía de Contribución

¡Gracias por tu interés en contribuir a SAT Engine! Este documento proporciona pautas para contribuir al proyecto.

## Cómo Contribuir

### Reportar Bugs

Si encuentras un error, por favor abre un issue con:
- Descripción clara del problema
- Pasos para reproducirlo
- Versión del motor utilizada
- Mensaje de error completo (si aplica)

### Sugerir Mejoras

Las mejoras son bienvenidas. Abre un issue describiendo:
- La mejora propuesta
- Justificación / caso de uso
- Posible implementación (opcional)

### Pull Requests

1. Fork el repositorio
2. Crea una rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## Estándares de Código

### Python
- Seguir [PEP 8](https://peps.python.org/pep-0008/)
- Usar `black` para formateo: `black *.py`
- Docstrings en funciones públicas
- Type hints donde sea apropiado

### C++
- Seguir [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- Indentación: 4 espacios
- Llaves en nueva línea para funciones
- Comentarios con `//` para inline, `/* */` para bloques

## Estructura de Commits

```
tipo: descripción corta (máx 50 chars)

cuerpo opcional más detallado (wrap a 72 chars)
```

Tipos:
- `feat`: nueva funcionalidad
- `fix`: corrección de bug
- `docs`: documentación
- `perf`: mejora de rendimiento
- `refactor`: reestructuración de código
- `test`: tests

## Testing

Antes de enviar un PR:
- Verificar que todas las versiones ejecutan sin errores
- Si modificas el backend C++, recompilar y probar
- Añadir tests si aplica

## Áreas de Contribución Prioritarias

- [ ] Implementar DPLL/CDCL completo
- [ ] Añadir parser DIMACS CNF
- [ ] Benchmarks comparativos
- [ ] Documentación de algoritmos
- [ ] Tests unitarios
- [ ] Optimizaciones del backend C++

## Contacto

Para dudas, abre un issue de tipo "Question".

---

Al contribuir, aceptas que tu código será licenciado bajo MIT License.
