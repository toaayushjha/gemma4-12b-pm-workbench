#!/usr/bin/env python3
"""
bench_next.py — add Qwen3-Coder-Next (LM Studio, MLX) to the text benchmark and
emit a 3-way comparison vs the Ollama models already measured.

Qwen3-Coder-Next runs in **LM Studio** (OpenAI-compatible server on :1234),
because that's where its MLX build lives. The other two models' numbers are read
from the existing 2-way CSV, so only one big model is in memory at a time.

Prereqs (done by the runner):
  lms server start
  lms load <qwen3-coder-next>        # other models unloaded first
Then:
  python bench_next.py
"""
from __future__ import annotations

import csv
import json
import pathlib
import time
import urllib.request

from run_eval import build_prompt, load_tasks, resolve

ROOT = pathlib.Path(__file__).resolve().parent
RESULTS = ROOT / "results"
LMS = "http://localhost:1234/v1"
TEXT_CATS = ["01_daily_workflows", "02_orchestration", "03_light_coding", "04_summarizing"]
PRIOR_CSV = RESULTS / "compare_gemma4-12b_vs_qwen3-coder-30b.csv"
LABEL = "qwen3-coder-next"


def lms_models() -> list[str]:
    with urllib.request.urlopen(LMS + "/models", timeout=10) as r:
        return [m["id"] for m in json.loads(r.read()).get("data", [])]


def detect_model() -> str:
    models = lms_models()
    for m in models:
        if "coder-next" in m.lower() or "coder_next" in m.lower():
            return m
    raise SystemExit(f"qwen3-coder-next not loaded in LM Studio.\nLoaded: {models}\n"
                     "Run: lms server start && lms load qwen/qwen3-coder-next")


def gen(prompt: str, model: str) -> dict:
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "stream": False, "temperature": 0.7}
    req = urllib.request.Request(LMS + "/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    resp = json.loads(urllib.request.urlopen(req, timeout=1800).read())
    dt = round(time.time() - t0, 2)
    usage = resp.get("usage", {})
    out = usage.get("completion_tokens")
    return {"response": resp["choices"][0]["message"]["content"], "latency_s": dt,
            "output_tokens": out, "tokens_per_s": round(out / dt, 1) if (out and dt) else None}


def load_prior() -> dict:
    prior = {}
    if PRIOR_CSV.exists():
        for row in csv.DictReader(open(PRIOR_CSV)):
            prior[row["task_id"]] = row
    return prior


def main() -> None:
    model = detect_model()
    print(f"Using LM Studio model: {model}\n")
    tasks = [t for t in load_tasks()["tasks"]
             if t["category"] in TEXT_CATS and t.get("modality", "text") == "text"]
    prior = load_prior()

    rows = []
    for t in tasks:
        prompt = build_prompt(t, resolve(t.get("input")))
        r = gen(prompt, model)
        print(f"▶ {t['id']:<5} {r['latency_s']:>6}s  {r['tokens_per_s']} tok/s  {t['title']}")
        rows.append((t, r))

    # 3-way CSV
    with open(RESULTS / "compare_3way_text.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["task_id", "title",
                    "gemma12b_lat", "gemma12b_tps",
                    "qwen30b_lat", "qwen30b_tps",
                    "qwennext_lat", "qwennext_tps"])
        for t, r in rows:
            p = prior.get(t["id"], {})
            w.writerow([t["id"], t["title"],
                        p.get("gemma4:12b_latency_s", ""), p.get("gemma4:12b_tok_s", ""),
                        p.get("qwen3-coder:30b_latency_s", ""), p.get("qwen3-coder:30b_tok_s", ""),
                        r["latency_s"], r["tokens_per_s"]])

    # 3-way markdown
    def col(side, key, cast=float):
        out = []
        for t, r in rows:
            p = prior.get(t["id"], {})
            v = r[key.split("_")[1]] if side == "next" else p.get(key)
            try:
                out.append(cast(v))
            except (TypeError, ValueError):
                pass
        return out

    g_lat = [float(prior[t["id"]]["gemma4:12b_latency_s"]) for t, _ in rows if t["id"] in prior]
    g_tps = [float(prior[t["id"]]["gemma4:12b_tok_s"]) for t, _ in rows if t["id"] in prior]
    q_lat = [float(prior[t["id"]]["qwen3-coder:30b_latency_s"]) for t, _ in rows if t["id"] in prior]
    q_tps = [float(prior[t["id"]]["qwen3-coder:30b_tok_s"]) for t, _ in rows if t["id"] in prior]
    n_lat = [r["latency_s"] for _, r in rows]
    n_tps = [r["tokens_per_s"] for _, r in rows if r["tokens_per_s"]]
    mean = lambda xs: sum(xs) / len(xs) if xs else 0

    md = ["# 3-way text benchmark: Gemma 4 12B vs Qwen3-Coder 30B vs Qwen3-Coder-Next\n",
          "_14 text tasks. Gemma 4 12B & Qwen3-Coder 30B via Ollama; "
          "**Qwen3-Coder-Next (MLX) via LM Studio**. Quality of the first two is in "
          "[`compare_gemma4-12b_vs_qwen3-coder-30b.md`](compare_gemma4-12b_vs_qwen3-coder-30b.md)._\n",
          "## Speed summary\n",
          "| Model | Runtime | Avg latency | Avg tok/s |", "|---|---|--:|--:|",
          f"| Gemma 4 12B | Ollama | {mean(g_lat):.1f}s | {mean(g_tps):.0f} |",
          f"| Qwen3-Coder 30B (MoE) | Ollama | {mean(q_lat):.1f}s | {mean(q_tps):.0f} |",
          f"| **Qwen3-Coder-Next (MLX)** | LM Studio | **{mean(n_lat):.1f}s** | **{mean(n_tps):.0f}** |\n",
          "## Per-task latency (s) / tok-s\n",
          "| Task | Gemma 12B | Qwen 30B | Qwen-Next |", "|---|--:|--:|--:|"]
    for t, r in rows:
        p = prior.get(t["id"], {})
        md.append(f"| {t['id']} {t['title']} "
                  f"| {p.get('gemma4:12b_latency_s','–')}s / {p.get('gemma4:12b_tok_s','–')} "
                  f"| {p.get('qwen3-coder:30b_latency_s','–')}s / {p.get('qwen3-coder:30b_tok_s','–')} "
                  f"| {r['latency_s']}s / {r['tokens_per_s']} |")
    md.append("\n---\n\n## Qwen3-Coder-Next — full outputs (judge quality)\n")
    for t, r in rows:
        md.append(f"### {t['id']} — {t['title']}\n_({r['latency_s']}s, {r['tokens_per_s']} tok/s)_\n")
        md.append(r["response"].strip() + "\n\n---\n")
    (RESULTS / "compare_3way_text.md").write_text("\n".join(md))
    print("\nWrote results/compare_3way_text.md and .csv")


if __name__ == "__main__":
    main()
