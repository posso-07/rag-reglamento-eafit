"""Consulta: recuperar fragmentos -> prompt anti-alucinación -> respuesta + fuentes."""
import json
import numpy as np
import config
import nim

SYSTEM_PROMPT = f"""Eres un asistente que responde dudas de estudiantes sobre el reglamento y el plan de estudios de su carrera.

Reglas:
1. Responde SOLO con el contexto proporcionado. No uses conocimiento externo ni supongas.
2. Si el contexto no contiene la información necesaria, responde exactamente: "{config.NO_INFO}"
3. Cita siempre la fuente con el número del fragmento entre corchetes, por ejemplo [1] o [2][3].
4. Si la pregunta combina varios documentos, usa fragmentos de cada uno y di de cuál viene cada dato.
5. No hagas asesoría personalizada (calcular promedios, decidir trámites del estudiante). Explica solo lo que dicen los documentos.
6. Responde en español, de forma breve y clara, en un máximo de 150 palabras."""


class RAG:
    def __init__(self):
        if not config.CHUNKS_FILE.exists():
            raise RuntimeError("No existe el índice. Ejecuta primero: python ingest.py")
        self.meta = json.loads(config.META_FILE.read_text(encoding="utf-8"))
        self.index, self.vectors = None, None
        if config.INDEX_FILE.exists():
            try:
                import faiss
                self.index = faiss.read_index(str(config.INDEX_FILE))
            except ImportError:
                pass
        if self.index is None:                        # respaldo: búsqueda exacta con NumPy
            self.vectors = np.load(config.VECTORS_FILE)
        self.chunks = json.loads(config.CHUNKS_FILE.read_text(encoding="utf-8"))

    def retrieve(self, question: str, k: int = config.TOP_K):
        """Top-k por similitud, garantizando que cada documento aporte su mejor fragmento
        (útil para preguntas que cruzan reglamento + plan de estudios)."""
        q = nim.embed([question], input_type="query", model=self.meta["embed_model"])
        n = min(config.FETCH_K, len(self.chunks))
        if self.index is not None:
            scores, ids = self.index.search(q, n)
            scores, ids = scores[0], ids[0]
        else:
            sims = self.vectors @ q[0]
            ids = np.argsort(-sims)[:n]
            scores = sims[ids]
        candidates = [(float(s), self.chunks[int(i)]) for s, i in zip(scores, ids) if i != -1]

        chosen, seen_files = [], set()
        for s, c in candidates:                       # mejor fragmento de cada documento
            if c["file"] not in seen_files and s >= config.MIN_SCORE:
                chosen.append((s, c))
                seen_files.add(c["file"])
        chosen = chosen[:k]
        taken = {c["id"] for _, c in chosen}
        for s, c in candidates:                       # completar hasta k por puntaje
            if len(chosen) >= k:
                break
            if c["id"] not in taken and s >= config.MIN_SCORE:
                chosen.append((s, c))
                taken.add(c["id"])
        return sorted(chosen, key=lambda x: -x[0])

    def ask(self, question: str) -> dict:
        hits = self.retrieve(question)
        if not hits:                                  # nada relevante: ni se llama al LLM
            return {"answer": config.NO_INFO, "sources": []}

        context = "\n\n".join(
            f"[{n}] (archivo: {c['file']}, página {c['page']})\n{c['text']}"
            for n, (_, c) in enumerate(hits, start=1)
        )
        try:
            answer = nim.chat(SYSTEM_PROMPT, f"CONTEXTO:\n{context}\n\nPREGUNTA: {question}")
        except Exception as e:                        # el servicio falló: se informa en vez de detenerse
            answer = f"[El modelo no devolvió una respuesta: {e}]"
        sources = [
            {"n": n, "file": c["file"], "page": c["page"], "score": round(s, 3), "text": c["text"]}
            for n, (s, c) in enumerate(hits, start=1)
        ]
        return {"answer": answer, "sources": sources}
