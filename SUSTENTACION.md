# Guion para la sustentación (17 de noviembre de 2026)

Todos deben poder explicar todo. Reparto sugerido para hablar, pero cada uno debe dominar el flujo completo.

## Estructura (≈10 min)
1. **Problema (1 min).** Estudiantes sin claridad sobre el reglamento; documentos largos. Alcance y lo que queda fuera.
2. **Por qué RAG (1 min).** Documentos concretos que cambian; el modelo no los conoce; hay que citar la fuente; no hay nada que calcular, así que un agente no aporta.
3. **Arquitectura (2 min).** Mostrar el diagrama del README: ingesta → índice → recuperación → LLM → respuesta con fuentes.
4. **Demo en vivo (3 min).** `python ask.py` con los casos 1 (habitual), 4 (dos documentos) y 5 (límite). Mostrar las fuentes en pantalla y abrir el PDF de `docs/` en esa página. El caso 4 puede tardar: tener `resultados.md` abierto como respaldo.
5. **Resultados y limitaciones (2 min).** Tabla de los 5 casos y el error observado con su mejora.
6. **Preguntas (1 min).**

## Preguntas que probablemente harán
- **¿Qué es un embedding?** Vector que representa el significado de un texto; textos parecidos quedan cerca.
- **¿Por qué fragmentos de 800 caracteres con solape de 150?** Lo bastante cortos para ser específicos y lo bastante largos para conservar una regla completa; el solape evita cortar una regla por la mitad.
- **¿Por qué `input_type` passage/query?** El modelo de NVIDIA está entrenado para asimetría pregunta/documento y lo exige.
- **¿Qué hace el prompt anti-alucinación y funciona?** Obliga a responder solo con el contexto y a decir "No encuentro información suficiente…". Lo verificamos con los casos 5 y 7.
- **¿Para qué el umbral `MIN_SCORE`?** Si nada es relevante, no se llama al LLM y se evita que invente.
- **¿Por qué recuperación balanceada?** Para que las preguntas de dos documentos reciban fragmentos de ambos.
- **¿Por qué FAISS y no una base vectorial?** Es local, sin servidor, suficiente para pocos miles de fragmentos.
- **¿Qué pasa si el reglamento cambia?** Se vuelve a ejecutar `ingest.py`; la actualización automática está fuera de alcance.
- **¿Dónde está la clave de API?** En `.env` (local) o Secrets de Colab; nunca en el repositorio.

## Antes de la sustentación
- [x] Ejecutar todo de principio a fin (`resultados.md` generado el 17-nov).
- [x] Valoración, errores y mejoras completados en el README.
- [ ] Leer la sección 7 del README: son las limitaciones que hay que saber explicar.
- [ ] Verificar contra los PDF de `docs/` la respuesta de los 5 casos.
- [ ] Tener claro (y decirlo) que los documentos son un resumen del reglamento y los semestres 1 a 6 del plan, preparados por el equipo a partir de la información oficial de EAFIT.
- [ ] Revisar que no hay claves en el repo (`git log -p | grep nvapi` no debe devolver nada).
- [ ] Tener la demo preparada por si falla internet (capturas de las respuestas).
