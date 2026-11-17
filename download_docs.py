"""Verifica que los documentos del proyecto estén en docs/.

Los dos PDF vienen incluidos en el repositorio (ver README, sección Documentos).
Uso:  python download_docs.py
"""
import sys
import config

pdfs = sorted(p for p in config.DOCS_DIR.glob("*") if p.suffix.lower() in {".pdf", ".txt"})
for p in pdfs:
    print(f"= {p.name} ({p.stat().st_size // 1024} KB)")
if len(pdfs) < 2:
    sys.exit("Faltan documentos en docs/. Deben estar el reglamento y el plan de estudios (ver README).")
