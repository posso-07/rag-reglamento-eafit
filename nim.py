"""Cliente de NVIDIA NIM (embeddings y LLM) vía API compatible con OpenAI.

NVIDIA retira modelos del catálogo con frecuencia (error 410). Por eso no se depende de un nombre fijo:
se prueban primero los preferidos de config.py y, si no están, se consulta el catálogo (/v1/models)
y se usa el primero que responda. El modelo elegido se guarda en .modelos.json.
"""
import json
import os
import re
import sys
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, APIConnectionError, AuthenticationError
import config

load_dotenv(config.BASE_DIR / ".env")

class _Unusable(Exception):
    """El modelo respondió pero no sirve (p. ej. texto vacío): se prueba el siguiente."""


CACHE = config.BASE_DIR / ".modelos.json"
_client = None
_skip = set()   # modelos descartados en esta ejecución
_chosen = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}

# Orden de preferencia cuando hay que elegir del catálogo (subcadenas del id del modelo).
RANK = {
    "llm": ["llama-3.3-70b", "llama-4", "llama-3.1-70b", "llama-3.1-405b", "meta/llama", "mistral-large",
            "mistral-small", "mistral", "mixtral", "nemotron", "gemma", "qwen", "phi-4", "phi", "gpt-oss"],
    "embed": ["nv-embedqa-e5-v5", "llama-3.2-nv-embedqa-1b-v2", "llama-nemotron-embed-1b", "embedqa",
              "nv-embed-v1", "bge-m3", "arctic-embed", "embed"],
}
EXCLUDE = {
    "llm": ["embed", "rerank", "guard", "safety", "vision", "vlm", "-vl", "clip", "whisper", "tts", "asr",
            "parse", "ocr", "deplot", "coder", "code", "reward", "detect", "nv-", "pii", "topic", "audio",
            "video", "image", "diffusion", "flux", "sdxl", "retriev", "translate", "riva", "bge", "e5"],
    "embed": ["clip", "-vl", "vlm", "code", "image", "rerank"],
}


def client() -> OpenAI:
    global _client
    if _client is None:
        key = (os.getenv("NVIDIA_API_KEY") or "").strip()
        if not key:
            raise RuntimeError("Falta NVIDIA_API_KEY. Copia .env.example a .env y pon tu clave.")
        _client = OpenAI(base_url=config.NIM_BASE_URL, api_key=key, max_retries=2, timeout=75)
    return _client


def _candidates(kind: str, preferred: list[str]) -> list[str]:
    """Preferidos de config.py y, después, los del catálogo ordenados por RANK."""
    try:
        ids = [m.id for m in client().models.list().data]
    except AuthenticationError:
        raise
    except Exception:
        ids = []
    ids = [i for i in ids if not any(x in i.lower() for x in EXCLUDE[kind])]
    if kind == "embed":
        ids = [i for i in ids if "embed" in i.lower() or "bge" in i.lower()]

    def rank(i):
        for n, key in enumerate(RANK[kind]):
            if key in i.lower():
                return n
        return len(RANK[kind])
    ranked = sorted((i for i in ids if rank(i) < len(RANK[kind])), key=rank)
    out = []
    for m in preferred + ranked:
        if m not in out:
            out.append(m)
    return out[:40]


def _with_model(kind: str, preferred: list[str], call):
    """Ejecuta call(modelo) con el primer modelo que responda y lo recuerda."""
    if kind in _chosen:
        try:
            return call(_chosen[kind])
        except (_Unusable, APIConnectionError):
            bad = _chosen.pop(kind)                 # el modelo guardado no sirve aquí: se busca otro
            print(f"  (aviso) {bad} no respondió a tiempo o devolvió vacío; se busca otro modelo")
            preferred = [m for m in preferred if m != bad]
            _skip.add(bad)
        except APIStatusError as e:
            if e.status_code not in (404, 410):
                raise
            _chosen.pop(kind)                       # el modelo guardado fue retirado: se busca otro
    errors = []
    for model in _candidates(kind, preferred):
        if model in _skip:
            continue
        try:
            out = call(model)
        except AuthenticationError:
            raise
        except (_Unusable, APIConnectionError) as e:
            errors.append(f"{model}: {type(e).__name__}")
            continue
        except APIStatusError as e:
            if e.status_code == 429:
                raise
            errors.append(f"{model}: {e.status_code}")   # retirado, sin acceso o parámetros no admitidos
            continue
        _chosen[kind] = model
        CACHE.write_text(json.dumps(_chosen, indent=1), encoding="utf-8")
        print(f"  Modelo {kind}: {model}")
        return out
    raise RuntimeError("Ningún modelo de NVIDIA NIM respondió para '" + kind + "'. Intentos: " + "; ".join(errors[:15]))


def embed(texts: list[str], input_type: str, model: str | None = None, batch_size: int = 32) -> np.ndarray:
    """input_type: 'passage' para documentos, 'query' para preguntas (lo exigen los modelos de NVIDIA)."""
    if model:
        _chosen["embed"] = model

    def call_for(batch):
        def call(m):
            return client().embeddings.create(
                model=m, input=batch, encoding_format="float",
                extra_body={"input_type": input_type, "truncate": "END"},
            )
        return call

    vectors = []
    for i in range(0, len(texts), batch_size):
        resp = _with_model("embed", config.EMBED_MODELS, call_for(texts[i:i + batch_size]))
        vectors.extend(d.embedding for d in resp.data)
    arr = np.array(vectors, dtype="float32")
    arr /= np.linalg.norm(arr, axis=1, keepdims=True)  # normalizado: producto interno = coseno
    return arr


def embed_model() -> str:
    return _chosen.get("embed", config.EMBED_MODELS[0])


def llm_model() -> str:
    return _chosen.get("llm", config.LLM_MODELS[0])


def chat(system: str, user: str, max_tokens: int = 900) -> str:
    def call(m):
        # Algunos modelos razonan antes de responder y gastan ahí los tokens: si el texto llega vacío,
        # se reintenta con más margen; si sigue vacío, se pasa al siguiente modelo.
        for budget in (max_tokens, 3000):
            r = client().chat.completions.create(
                model=m,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=0.0, max_tokens=budget,
            )
            text = (r.choices[0].message.content or "") if r.choices else ""
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
            text = re.sub(r"^.*?</think>", "", text, flags=re.S).strip()
            if text:
                return text
        raise _Unusable("respuesta vacía")
    return _with_model("llm", config.LLM_MODELS, call)


def check():
    """Verifica la clave y elige modelos que funcionen. Código de salida 2 = clave inválida."""
    try:
        chat("Responde solo: ok", "ok", max_tokens=200)
        embed(["prueba"], input_type="query")
    except AuthenticationError:
        print("La clave de NVIDIA no es válida (401).")
        sys.exit(2)
    print("Clave de NVIDIA verificada.")


if __name__ == "__main__":
    check()
