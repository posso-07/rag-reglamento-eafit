"""Interfaz de línea de comandos.

Uso:
  python ask.py "¿Cuántas veces puedo repetir una materia?"
  python ask.py                      # modo interactivo
"""
import sys
import config
from rag import RAG


def show(result: dict):
    print("\nRESPUESTA\n" + result["answer"])
    if result["sources"] and config.NO_INFO not in result["answer"]:
        print("\nFUENTES")
        for s in result["sources"]:
            snippet = " ".join(s["text"].split())[:300]
            print(f"  [{s['n']}] {s['file']} · pág. {s['page']} · sim={s['score']}\n      \"{snippet}...\"")
    print()


def main():
    rag = RAG()
    if len(sys.argv) > 1:
        show(rag.ask(" ".join(sys.argv[1:])))
        return
    print("Asistente de reglamento. Escribe 'salir' para terminar.")
    while True:
        q = input("\nPregunta> ").strip()
        if q.lower() in {"salir", "exit", "q"}:
            break
        if q:
            show(rag.ask(q))


if __name__ == "__main__":
    main()
