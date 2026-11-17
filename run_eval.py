"""Corre los casos de eval_questions.json y escribe resultados.md para completar la valoración.

Uso:  python run_eval.py
"""
import json
import time
import config
import nim
from rag import RAG

rag = RAG()
casos = json.loads((config.BASE_DIR / "eval_questions.json").read_text(encoding="utf-8"))

out = ["# Resultados de las pruebas\n",
       "Generado por `run_eval.py`. Completa la **Valoración** de cada caso comparando con los PDF originales.\n"]
for c in casos:
    print(f"Caso {c['id']}: {c['pregunta']}", flush=True)
    t0 = time.time()
    r = rag.ask(c["pregunta"])
    print(f"   listo en {time.time() - t0:.0f} s", flush=True)
    out.append(f"\n## Caso {c['id']} · {c['categoria']}\n")
    out.append(f"**Pregunta:** {c['pregunta']}\n")
    out.append(f"**Resultado esperado:** {c['esperado']}\n")
    out.append(f"**Respuesta obtenida:**\n\n> " + r["answer"].replace("\n", "\n> ") + "\n")
    if r["sources"]:
        out.append("**Fuentes recuperadas:**\n")
        for s in r["sources"]:
            out.append(f"- [{s['n']}] `{s['file']}` p. {s['page']} (sim={s['score']})")
    else:
        out.append("**Fuentes recuperadas:** ninguna (por debajo del umbral)")
    out.append("\n**Valoración:** _(completar: ¿relevante? ¿respaldada por los fragmentos? ¿errores?)_\n")

out.insert(2, f"\nModelos usados: LLM `{nim.llm_model()}` · embeddings `{nim.embed_model()}` · índice `{rag.meta['backend']}`\n")
(config.BASE_DIR / "resultados.md").write_text("\n".join(out), encoding="utf-8")
print("\nListo: resultados.md")
