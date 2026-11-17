# Resultados de las pruebas

Generado por `run_eval.py` el 17 de noviembre de 2026. La valoración de cada caso se hizo a mano, comparando la respuesta con los documentos de `docs/`.


Modelos usados: LLM `mistralai/mistral-large-4-1t-a52b` · embeddings `nvidia/nemotron-3-embed-1b` · índice `faiss`


## Caso 1 · habitual

**Pregunta:** ¿Puedo cancelar solo algunas materias del semestre? ¿Hay algún límite?

**Resultado esperado:** Reglamento, Art. 49: sí; la cancelación parcial no puede superar el 50 % de los créditos matriculados, la asignatura no puede estar evaluada en más del 75 % y hay una fecha límite en el calendario académico. La práctica no se puede cancelar.

**Respuesta obtenida:**

> Sí, puedes cancelar parcialmente créditos matriculados, pero con estos límites: la cancelación parcial **no puede superar el 50 % de los créditos totales matriculados** en el período; además, la asignatura **no puede haber sido evaluada en más del 75 %** (lo verifica el profesor) y debes hacerlo **antes de la fecha límite** que fija el Consejo Académico en el calendario académico [1].
> 
> Ten en cuenta que los créditos de la práctica estudiantil no se pueden cancelar, salvo fuerza mayor o caso fortuito comprobado ante el Comité de Casos [1].

**Fuentes recuperadas:**

- [1] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.542)
- [2] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.438)
- [3] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.327)
- [4] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.321)

**Valoración:** Correcta. Coincide con el Art. 49 (50 %, 75 %, fecha límite, práctica) y todo sale del fragmento [1]. Los fragmentos [2] a [4] tienen similitud baja (0.32 a 0.44) y no aportan: se recuperan solo para completar k=4.


## Caso 2 · habitual

**Pregunta:** Si pierdo una materia, ¿cuándo puedo repetirla?

**Resultado esperado:** Reglamento, Art. 52: en el período académico que el estudiante escoja, siempre que cumpla prerrequisitos y correquisitos.

**Respuesta obtenida:**

> Puedes escoger el período académico en el que la repites, siempre que cumplas los prerrequisitos y correquisitos de tu plan de estudios. El reglamento no establece un número máximo de veces que se puede repetir una asignatura [1].

**Fuentes recuperadas:**

- [1] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.563)
- [2] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 5 (sim=0.341)
- [3] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.337)
- [4] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 5 (sim=0.335)

**Valoración:** Correcta y respaldada por el fragmento [1] (Art. 52). Añade que no hay un máximo de repeticiones, lo cual también está en el fragmento.


## Caso 3 · habitual

**Pregunta:** ¿Con qué promedio pierdo la condición de estudiante por rendimiento académico?

**Resultado esperado:** Reglamento, Art. 54: semestral < 2.5 en la primera matrícula; semestral y acumulado < 2.8 con hasta tres matrículas; semestral y acumulado < 3.0 con cuatro o más.

**Respuesta obtenida:**

> Según el Artículo 54, pierdes la condición de estudiante por rendimiento académico en estos casos [1][3]:
> 
> *   Al finalizar tu **primera matrícula** con promedio crédito semestral **inferior a 2.5** [1].
> *   Si has tenido **hasta tres matrículas** semestrales y registras promedio crédito semestral **inferior a 2.8** y promedio crédito acumulado **inferior a 2.8** [1].
> *   Si has tenido **cuatro o más matrículas** semestrales y registras promedio crédito semestral **inferior a 3.0** y promedio crédito acumulado **inferior a 3.0** [1][3].

**Fuentes recuperadas:**

- [1] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.613)
- [2] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.527)
- [3] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.434)
- [4] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.424)

**Valoración:** Correcta. Los tres umbrales (2.5, 2.8 y 3.0) coinciden con el Art. 54 y están en el fragmento [1].


## Caso 4 · dos documentos

**Pregunta:** ¿Qué prerrequisitos y correquisitos tiene Inteligencia Artificial y qué dice el reglamento si quiero matricularla sin cumplir un prerrequisito?

**Resultado esperado:** Plan de estudios (semestre 5): prerrequisito Estructura de datos y algoritmos (SI2001); correquisitos Análisis y Diseño de Algoritmos (SI3005) y Arquitectura de Software (SI3001). Reglamento, Art. 9: la excepción la autoriza el jefe del programa y solo si se cumple alguna condición (percentil 90, doble programa, salud, seguridad, etc.). La respuesta debe citar AMBOS documentos.

**Respuesta obtenida:**

> Inteligencia Artificial (SI3003) tiene como **prerrequisito**: Estructura de datos y algoritmos (SI2001) [1][4]. Como **correquisitos**: Análisis y Diseño de Algoritmos (SI3005) y Arquitectura de Software (SI3001) [1][4].
> 
> Según el reglamento (Artículo 9), un prerrequisito es indispensable haberlo aprobado para matricular la asignatura [3]. Si deseas matricularla sin cumplirlo, cualquier excepción debe ser **autorizada por el jefe del programa de pregrado** y solo procede si cumples alguna de estas condiciones: promedio crédito acumulado en el percentil 90 o superior de tu programa; compromisos previos con entidades externas (práctica, investigación o condonación de becas); estar activo en doble programa de pregrado; razones de salud o cognitivas certificadas; razones de seguridad certificadas; o condiciones análogas validadas por la decanatura [2].

**Fuentes recuperadas:**

- [1] `plan-estudios-ingenieria-sistemas-2025-1.pdf` p. 5 (sim=0.504)
- [2] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 1 (sim=0.491)
- [3] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 1 (sim=0.416)
- [4] `plan-estudios-ingenieria-sistemas-2025-1.pdf` p. 5 (sim=0.409)

**Valoración:** Correcta y es el caso más exigente: usa los dos documentos. Los requisitos salen del plan (fragmentos [1] y [4], semestre 5) y la regla de excepción del reglamento (fragmentos [2] y [3], Art. 9). Fue el caso más lento y el que hizo fallar al primer modelo (ver análisis en el README).


## Caso 5 · limite (información ausente)

**Pregunta:** ¿Qué materias se ven en el noveno semestre de Ingeniería de Sistemas?

**Resultado esperado:** El documento del plan solo cubre los semestres 1 a 6. Debe responder 'No encuentro información suficiente en los documentos.' sin inventar materias.

**Respuesta obtenida:**

> No encuentro información suficiente en los documentos.

**Fuentes recuperadas:**

- [1] `plan-estudios-ingenieria-sistemas-2025-1.pdf` p. 1 (sim=0.551)
- [2] `plan-estudios-ingenieria-sistemas-2025-1.pdf` p. 4 (sim=0.473)
- [3] `plan-estudios-ingenieria-sistemas-2025-1.pdf` p. 1 (sim=0.463)
- [4] `plan-estudios-ingenieria-sistemas-2025-1.pdf` p. 3 (sim=0.436)

**Valoración:** Correcta: reconoce que no tiene la información y no inventa materias. Ojo: la similitud de los fragmentos fue alta (0.55) porque hablan del mismo plan, así que el umbral no lo detuvo; quien evitó la alucinación fue el prompt.


## Caso 6 · extra: fuera de alcance (personalizada)

**Pregunta:** Saqué 2.9 de promedio semestral en mi quinta matrícula, ¿me retiran?

**Resultado esperado:** Debe explicar la regla del Art. 54 literal (c) sin dar un veredicto sobre el caso (además depende del promedio acumulado).

**Respuesta obtenida:**

> Según el Artículo 54 literal (c), se pierde la condición de estudiante cuando se han tenido **cuatro o más matrículas semestrales** y el estudiante registra **promedio crédito semestral inferior a 3.0 y promedio crédito acumulado inferior a 3.0** [1].
> 
> En tu caso (quinta matrícula), con un promedio semestral de 2.9, el retiro aplica únicamente si tu **promedio acumulado también es inferior a 3.0**.

**Fuentes recuperadas:**

- [1] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.478)
- [2] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.445)
- [3] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 5 (sim=0.321)
- [4] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.312)

**Valoración:** Parcial. Explica bien el Art. 54 (c) y aclara que depende del promedio acumulado, pero aplica la regla al caso del estudiante ('en tu caso...'), que es asesoría personalizada y estaba fuera del alcance.


## Caso 7 · extra: información ausente

**Pregunta:** ¿Cuál es el horario de la biblioteca?

**Resultado esperado:** 'No encuentro información suficiente en los documentos.'

**Respuesta obtenida:**

> No encuentro información suficiente en los documentos.

**Fuentes recuperadas:** ninguna (por debajo del umbral)

**Valoración:** Correcta. Ningún fragmento superó el umbral de similitud, así que ni siquiera se llamó al LLM.


## Caso 8 · extra: pregunta con supuesto falso

**Pregunta:** ¿Cuántas veces máximo puedo repetir una misma materia?

**Resultado esperado:** El Art. 52 no fija un número máximo de repeticiones. No debe inventar una cifra.

**Respuesta obtenida:**

> Según el Artículo 52, el reglamento **no establece un número máximo de veces** que se puede repetir una asignatura, siempre que no se pierda la condición de estudiante regular y se cumplan los prerrequisitos y correquisitos del plan de estudios [1].

**Fuentes recuperadas:**

- [1] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.46)
- [2] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 5 (sim=0.324)
- [3] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.267)
- [4] `reglamento-academico-pregrado-eafit-resumen.pdf` p. 4 (sim=0.258)

**Valoración:** Correcta: no inventa una cifra y cita el Art. 52. Depende de que el resumen diga explícitamente que no hay máximo.
