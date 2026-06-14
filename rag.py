#!/usr/bin/env python3
"""
rag.py — a tiny, 100%-local "ask my documents" assistant (optional Phase G).

EmbeddingGemma (google/embeddinggemma-300m via Ollama) embeds your docs; Gemma 4
12B answers questions grounded in the most relevant chunks. No cloud, no vector
DB — just stdlib + Ollama. Demonstrates a private local knowledge assistant over
PM docs.

Usage:
  ollama pull embeddinggemma
  python rag.py "What did we decide about the free trial credit-card requirement?"
  python rag.py            # interactive
"""
from __future__ import annotations

import json
import pathlib
import sys
import urllib.request

import gemma_client as gc

ROOT = pathlib.Path(__file__).resolve().parent
DOCS_DIR = ROOT / "inputs" / "docs"
EMBED_MODEL = "embeddinggemma"
OLLAMA = gc.OLLAMA_URL


def embed(texts: list[str]) -> list[list[float]]:
    payload = {"model": EMBED_MODEL, "input": texts}
    req = urllib.request.Request(OLLAMA + "/api/embed",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())["embeddings"]


def chunk(text: str, size: int = 900, overlap: int = 150) -> list[str]:
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i + size])
        i += size - overlap
    return out


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def build_index() -> list[dict]:
    chunks = []
    for fp in sorted(DOCS_DIR.glob("*.md")) + sorted(DOCS_DIR.glob("*.csv")):
        for j, c in enumerate(chunk(fp.read_text(errors="replace"))):
            chunks.append({"source": fp.name, "n": j, "text": c})
    print(f"Embedding {len(chunks)} chunks from {DOCS_DIR.name}/ …")
    vecs = embed([c["text"] for c in chunks])
    for c, v in zip(chunks, vecs):
        c["vec"] = v
    return chunks


def answer(query: str, index: list[dict], k: int = 4) -> None:
    qv = embed([query])[0]
    ranked = sorted(index, key=lambda c: cosine(qv, c["vec"]), reverse=True)[:k]
    context = "\n\n".join(f"[{c['source']}#{c['n']}]\n{c['text']}" for c in ranked)
    prompt = (
        "Answer the question using ONLY the context below. Cite sources in "
        "[brackets]. If the answer isn't in the context, say so.\n\n"
        f"# Context\n{context}\n\n# Question\n{query}"
    )
    r = gc.generate(prompt, log=False)
    print(f"\n💬 {r['response']}\n")
    print(f"— sources: {', '.join(sorted({c['source'] for c in ranked}))} "
          f"· {r['latency_s']}s · local + private")


if __name__ == "__main__":
    if not gc.is_ready():
        sys.exit("gemma4:12b not pulled. Run: ollama pull gemma4:12b")
    idx = build_index()
    if len(sys.argv) > 1:
        answer(" ".join(sys.argv[1:]), idx)
    else:
        print("Ask about your docs (Ctrl-C to quit).")
        try:
            while True:
                q = input("\n❓ ").strip()
                if q:
                    answer(q, idx)
        except (KeyboardInterrupt, EOFError):
            print("\nbye")
