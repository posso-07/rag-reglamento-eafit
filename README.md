# Asistente RAG del Reglamento Académico de Pregrado y plan de estudios de Ingeniería de Sistemas (EAFIT)

**SI3003 Inteligencia Artificial · Proyecto final · Opción A: sistema RAG**

**Integrantes:** Sebastián Martínez · Jerónimo Ramírez · Juan Pablo Posso

## 1. Problema y usuarios
Los estudiantes de pregrado de EAFIT no saben con precisión qué dice el reglamento sobre pérdida de
materias, cancelaciones, homologaciones o requisitos de grado. Los documentos son largos y están dispersos.
El prototipo responde esas dudas **citando el texto original** (archivo, página y fragmento).

**Qué atiende:** preguntas factuales ("¿cuánto puedo cancelar de un semestre?") y preguntas que combinan
dos documentos (reglamento + plan de estudios).

**Fuera de alcance:** asesoría personalizada (p. ej. calcular el promedio de un estudiante), trámites,
PDF escaneados sin texto, otras facultades, interfaz de producción y actualización automática de documentos.

## 2. Por qué RAG y no un agente
La información está en documentos concretos, que cambian y que el modelo no conoce. RAG permite responder
con base en ellos y mostrar la fuente. Un agente con herramientas aportaría poco: no hay nada que calcular
ni servicios externos que consultar.

## 3. Documentos (fuentes)
Los dos documentos están en `docs/` y vienen incluidos en el repositorio.

| Documento | Archivo en `docs/` | Origen |
|---|---|---|
| Reglamento académico de los programas de pregrado de EAFIT: resumen por artículos (arts. 1 a 90) | `reglamento-academico-pregrado-eafit-resumen.pdf` | Reglamento oficial (acta 019 de 2020, con modificaciones hasta febrero de 2024): https://www.eafit.edu.co/institucional/reglamentos |
| Plan de estudios de Ingeniería de Sistemas, vigente desde 2025-1 (semestres 1 a 6) | `plan-estudios-ingenieria-sistemas-2025-1.pdf` | https://www.eafit.edu.co/pregrado-ingenieria-de-sistemas-2025/plan-de-estudio |

**Importante sobre los documentos.** No son los PDF oficiales: son documentos de trabajo preparados por el
equipo con la información oficial de EAFIT consultada el 17 de noviembre de 2026.
- El reglamento es un **resumen por artículos**: cada regla conserva su número de artículo para poder
  verificarla en el texto oficial. No incluye los capítulos posteriores al artículo 90 (por ejemplo,
  requisitos de grado y régimen disciplinario).
- El plan de estudios recoge asignaturas, códigos, créditos, prerrequisitos y correquisitos de los
  **semestres 1 a 6**, tal como aparecen en la página del programa. Los semestres 7 a 9 no se incluyen.
- Se generan con `tools/build_docs.py` (requiere `pip install reportlab`), donde está todo su contenido.

Para usar los PDF oficiales basta con copiarlos a `docs/` y volver a ejecutar `python ingest.py`.

## 4. Arquitectura
```
PDF ──pypdf──> texto por página ──> fragmentos (800 car., solape 150) + metadatos (archivo, página)
    ──embeddings de NVIDIA NIM──> vectores ──> FAISS (IndexFlatIP, similitud coseno)

Pregunta ──embedding (query)──> top-k (k=4, ≥1 fragmento por documento)
         ──> prompt anti-alucinación + contexto ──LLM de NVIDIA NIM──> respuesta + fuentes
```
| Archivo | Función |
|---|---|
| `config.py` | Parámetros (tamaño de fragmento, k, modelos, umbral) |
| `nim.py` | Cliente NVIDIA NIM (embeddings y LLM) |
| `ingest.py` | Extracción, fragmentación, embeddings e índice FAISS |
| `rag.py` | Recuperación, prompt y generación |
| `ask.py` | CLI: una pregunta o modo interactivo |
| `run_eval.py` + `eval_questions.json` | Ejecuta los casos de prueba y genera `resultados.md` |
| `rag_reglamento.ipynb` | Notebook para Google Colab con todo el flujo |
| `download_docs.py` | Verifica que los documentos estén en `docs/` |
| `tools/build_docs.py` | Genera los dos PDF de `docs/` |
| `EJECUTAR.bat` | Windows: instala, pide la clave y ejecuta todo |

**Decisiones de diseño**
- *Prompt anti-alucinación:* responde solo con el contexto; si no alcanza responde
  "No encuentro información suficiente en los documentos." y cita `[n]`.
- *Umbral de similitud (`MIN_SCORE`):* si ningún fragmento es relevante, ni se llama al LLM.
- *Recuperación balanceada:* cada documento aporta su mejor fragmento, para que las preguntas que cruzan
  reglamento y plan de estudios vean ambos.
- *`input_type`:* el modelo de embeddings distingue `passage` y `query`; se usa cada uno donde corresponde.
- *Temperatura 0* para respuestas reproducibles.
- *Selección automática de modelos:* NVIDIA retira modelos de su catálogo (error 410), así que `nim.py`
  prueba los preferidos de `config.py` y, si no están, usa el primero disponible del catálogo. Los modelos
  usados quedan anotados en `resultados.md`.
- *Respaldo sin FAISS:* si `faiss-cpu` no se puede instalar, la búsqueda se hace con NumPy (mismo resultado).

## 5. Cómo ejecutarlo
**Clave de API (privada):** consigue una gratis en https://build.nvidia.com (empieza por `nvapi-`).
Nunca va en el código ni en el repo (`.env` está en `.gitignore`).

**Windows, en un paso:** doble clic en `EJECUTAR.bat`.

**Local**
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                    # pegar NVIDIA_API_KEY
python ingest.py
python ask.py "¿Puedo cancelar solo algunas materias del semestre?"
python run_eval.py                                      # genera resultados.md
```
**Google Colab:** abre `rag_reglamento.ipynb`, guarda la clave en *Secrets* con el nombre `NVIDIA_API_KEY`
(con acceso al notebook activado) y ejecuta las celdas en orden.

## 6. Los cinco casos de prueba
El resultado esperado se tomó de los documentos de `docs/`. La respuesta obtenida y la valoración salen de
ejecutar `python run_eval.py` (detalle completo en `resultados.md`).

| # | Tipo | Pregunta | Resultado esperado |
|---|---|---|---|
| 1 | Habitual | ¿Puedo cancelar solo algunas materias del semestre? ¿Hay algún límite? | Art. 49: máx. 50 % de los créditos matriculados; asignatura evaluada en ≤75 %; antes de la fecha límite del calendario; no aplica a la práctica. |
| 2 | Habitual | Si pierdo una materia, ¿cuándo puedo repetirla? | Art. 52: en el período que elija, si cumple prerrequisitos y correquisitos. |
| 3 | Habitual | ¿Con qué promedio pierdo la condición de estudiante? | Art. 54: <2.5 en la primera matrícula; <2.8 (semestral y acumulado) hasta 3 matrículas; <3.0 con 4 o más. |
| 4 | Dos documentos | ¿Qué prerrequisitos y correquisitos tiene Inteligencia Artificial y qué dice el reglamento si quiero matricularla sin cumplir un prerrequisito? | Plan: prerrequisito SI2001; correquisitos SI3005 y SI3001. Reglamento, Art. 9: excepción autorizada por el jefe del programa bajo condiciones. |
| 5 | Límite | ¿Qué materias se ven en el noveno semestre de Ingeniería de Sistemas? | Información ausente (el plan cubre semestres 1 a 6): "No encuentro información suficiente en los documentos." |

Casos extra en `eval_questions.json`: pregunta personalizada (6), dato ausente (7) y pregunta con supuesto falso (8).

### Resultados
Ejecución del 17 de noviembre de 2026. Modelos: LLM `mistralai/mistral-large-4-1t-a52b`, embeddings
`nvidia/nemotron-3-embed-1b`, índice FAISS (47 fragmentos). Respuestas completas y fuentes en `resultados.md`.

| # | Respuesta obtenida (resumen) | ¿Relevante y respaldada por las fuentes? | Valoración |
|---|---|---|---|
| 1 | Sí se puede; máximo 50 % de los créditos, asignatura evaluada en ≤75 %, antes de la fecha límite; la práctica no se cancela. | Sí, todo sale del fragmento [1] (Art. 49). | Correcta |
| 2 | En el período que el estudiante escoja, si cumple prerrequisitos y correquisitos; no hay máximo de repeticiones. | Sí, fragmento [1] (Art. 52). | Correcta |
| 3 | <2.5 en la primera matrícula; <2.8 semestral y acumulado hasta tres matrículas; <3.0 con cuatro o más. | Sí, fragmento [1] (Art. 54). | Correcta |
| 4 | Prerrequisito SI2001; correquisitos SI3005 y SI3001. La excepción la autoriza el jefe del programa bajo las condiciones del Art. 9. | Sí, con ambos documentos: plan ([1], [4]) y reglamento ([2], [3]). | Correcta |
| 5 | "No encuentro información suficiente en los documentos." | Sí: el plan solo llega al semestre 6 y no inventó materias. | Correcta |

Casos extra: el 7 (horario de la biblioteca) se rechazó sin llamar al LLM porque ningún fragmento superó el
umbral; el 8 (máximo de repeticiones) respondió que el Art. 52 no fija un máximo, sin inventar una cifra; el 6
(caso personal) quedó **parcial**, como se explica abajo.

## 7. Análisis de resultados
Los cinco casos se resolvieron bien y cada respuesta está respaldada por los fragmentos citados. El caso más
difícil fue el 4, que necesita los dos documentos: funcionó porque la recuperación garantiza al menos un
fragmento de cada documento.

**Errores y limitaciones observados**
1. *Asesoría personalizada (caso 6).* Ante "saqué 2.9 en mi quinta matrícula, ¿me retiran?", el sistema explicó
   bien el Art. 54 pero aplicó la regla al caso del estudiante ("en tu caso..."), aunque el prompt lo prohíbe.
   El prompt por sí solo no basta para mantener el alcance.
2. *El umbral de similitud no detecta toda la información ausente (caso 5).* La pregunta sobre el noveno
   semestre recuperó fragmentos con similitud alta (0.55) porque hablan del mismo plan. No hubo alucinación
   solo porque el prompt hizo que el modelo reconociera que faltaba el dato; con otro modelo podría fallar.
3. *Fragmentos de relleno (caso 1).* Siempre se pasan k=4 fragmentos, aunque solo uno sea útil; los otros
   tenían similitud de 0.32 a 0.44 y no aportaban.
4. *Dependencia del servicio de NVIDIA.* Los modelos previstos (`llama-3.3-70b`, `nv-embedqa-e5-v5`) ya no
   estaban en el catálogo (error 410). El primer modelo que se seleccionó, de tipo razonador, devolvió texto
   vacío en el caso 4, y ese caso fue el más lento. Se resolvió con selección automática de modelos,
   reintentos y cambio de modelo.
5. *Documentos resumidos.* El reglamento es un resumen y el plan llega al semestre 6: no se puede responder
   sobre requisitos de grado, régimen disciplinario ni semestres 7 a 9, y la página citada es la del resumen,
   no la del reglamento oficial.

**Mejoras propuestas**
- Clasificar la pregunta antes de responder (o validar la respuesta después) para rechazar casos personales
  en lugar de confiar solo en el prompt.
- Recuperar por umbral relativo (descartar fragmentos muy por debajo del mejor) en vez de k fijo, y fragmentar
  por artículo o por asignatura en lugar de por caracteres.
- Ingerir los PDF oficiales completos, extrayendo la malla con `pdfplumber`, y añadir el calendario académico,
  al que el reglamento remite para las fechas límite.
- Fijar un modelo estable (o desplegar uno propio) para que los resultados sean reproducibles.

## 8. Herramientas
Python · pypdf · FAISS · NVIDIA NIM (modelos elegidos automáticamente; en nuestra ejecución `mistralai/mistral-large-4-1t-a52b` y `nvidia/nemotron-3-embed-1b`) · OpenAI SDK
(cliente compatible con NIM) · python-dotenv.
