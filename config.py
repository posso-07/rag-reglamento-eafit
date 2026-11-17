"""Parámetros centrales del prototipo. Ajusta aquí, no en el resto del código."""
from pathlib import Path

BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
INDEX_DIR = BASE_DIR / "index"
INDEX_FILE = INDEX_DIR / "faiss.index"
VECTORS_FILE = INDEX_DIR / "vectors.npy"
CHUNKS_FILE = INDEX_DIR / "chunks.json"
META_FILE = INDEX_DIR / "meta.json"

# NVIDIA NIM expone una API compatible con OpenAI
NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"
# Se usa el primer modelo de cada lista que esté disponible para la clave.
EMBED_MODELS = ["nvidia/nv-embedqa-e5-v5", "nvidia/nv-embedqa-mistral-7b-v2", "nvidia/nv-embed-v1"]
LLM_MODELS = ["meta/llama-3.3-70b-instruct", "meta/llama-3.1-70b-instruct", "meta/llama-3.1-8b-instruct"]

# Fragmentación
CHUNK_SIZE = 800        # caracteres (500-1000)
CHUNK_OVERLAP = 150     # caracteres (100-200)

# Recuperación
TOP_K = 4               # fragmentos que se pasan al LLM (3-5)
FETCH_K = 20            # candidatos iniciales antes de balancear entre documentos
MIN_SCORE = 0.25        # similitud coseno mínima; por debajo, no se llama al LLM

NO_INFO = "No encuentro información suficiente en los documentos."
