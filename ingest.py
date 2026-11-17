"""Ingesta: PDF/TXT -> texto por página -> fragmentos con metadatos -> embeddings -> FAISS.

Uso:  python ingest.py
"""
import json
import re
import sys
import numpy as np
from pypdf import PdfReader
import config
import nim


def read_pages(path):
    """Devuelve [(num_pagina, texto)]. Los .txt se tratan como una sola página."""
    if path.suffix.lower() == ".pdf":
        pages = []
        for n, page in enumerate(PdfReader(str(path)).pages, start=1):
            text = clean(page.extract_text() or "")
            if text:
                pages.append((n, text))
        if not pages:
            print(f"  ! {path.name}: sin texto extraíble (¿PDF escaneado?). Se omite.")
        return pages
    return [(1, clean(path.read_text(encoding="utf-8")))]


def clean(text: str) -> str:
    text = re.sub(r"-\n(?=\w)", "", text)      # palabras partidas por guion al final de línea
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def split_text(text: str, size: int, overlap: int):
    """Ventana deslizante que intenta cortar en fin de frase o salto de línea."""
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            window = text[start:end]
            cut = max(window.rfind(". "), window.rfind("\n"))
            if cut > size * 0.5:               # solo si el corte no deja un fragmento diminuto
                end = start + cut + 1
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def main():
    files = sorted(p for p in config.DOCS_DIR.iterdir() if p.suffix.lower() in {".pdf", ".txt"})
    if not files:
        sys.exit(f"No hay documentos en {config.DOCS_DIR}. Copia ahí el reglamento y el plan de estudios.")

    chunks = []
    for path in files:
        print(f"Leyendo {path.name}...")
        for page_num, text in read_pages(path):
            for piece in split_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP):
                chunks.append({"id": len(chunks), "file": path.name, "page": page_num, "text": piece})
    print(f"{len(chunks)} fragmentos de {len(files)} documento(s). Calculando embeddings...")

    vectors = nim.embed([c["text"] for c in chunks], input_type="passage")
    config.INDEX_DIR.mkdir(exist_ok=True)
    np.save(config.VECTORS_FILE, vectors)          # copia de respaldo de los vectores
    try:
        import faiss
        index = faiss.IndexFlatIP(vectors.shape[1])   # producto interno sobre vectores normalizados = coseno
        index.add(vectors)
        faiss.write_index(index, str(config.INDEX_FILE))
        backend = "faiss"
    except ImportError:
        config.INDEX_FILE.unlink(missing_ok=True)
        backend = "numpy"
        print("  (aviso) FAISS no está instalado; se usará búsqueda exacta con NumPy.")
    config.META_FILE.write_text(json.dumps(
        {"embed_model": nim.embed_model(), "dim": int(vectors.shape[1]), "backend": backend}), encoding="utf-8")
    config.CHUNKS_FILE.write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Índice guardado en {config.INDEX_DIR}/")


if __name__ == "__main__":
    main()
