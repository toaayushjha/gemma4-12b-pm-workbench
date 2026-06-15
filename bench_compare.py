#!/usr/bin/env python3
"""
bench_compare.py — fair, apples-to-apples A/B of two local models on the
*text* categories of the workbench (daily workflows, orchestration, light
coding, summarizing). Multimodal tasks are skipped because coder models can't
see images/audio.

Usage:
  python bench_compare.py                              # gemma4:12b vs qwen3-coder:30b
  python bench_compare.py gemma4:12b qwen3-coder:30b
  python bench_compare.py --cats 03_light_coding

Outputs:
  results/compare_<A>_vs_<B>.md   — full side-by-side outputs + per-task stats
  results/compare_<A>_vs_<B>.csv  — latency / tokens-per-sec per model per task
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import re

import gemma_client as gc
from run_eval import build_prompt, load_tasks, resolve

ROOT = pathlib.Path(__file__).resolve().parent
RESULTS = ROOT / "results"
TEXT_CATS = ["01_daily_workflows", "02_orchestration", "03_light_coding", "04_summarizing"]


def safe(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def run_one(task: dict, model: str) -> dict:
    prompt = build_prompt(task, resolve(task.get("input")))
    return gc.generate(prompt, model=model, task_id=task["id"],
                       category=task["category"], log=False)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model_a", nargs="?", default="gemma4:12b")
    ap.add_argument("model_b", nargs="?", default="qwen3-coder:30b")
    ap.add_argument("--cats", nargs="*", default=TEXT_CATS)
    args = ap.parse_args()
    a, b = args.model_a, args.model_b

    have = " ".join(gc.list_models())
    for m in (a, b):
        if m.split(":")[0] not in have:
            raise SystemExit(f"Model '{m}' not pulled. Have: {have}\nRun: ollama pull {m}")

    tasks = [t for t in load_tasks()["tasks"]
             if t["category"] in args.cats and t.get("modality", "text") == "text"]
    print(f"Benchmarking {a}  vs  {b}  on {len(tasks)} text tasks\n")

    rows = []
    for t in tasks:
        print(f"▶ {t['id']} — {t['title']}")
        ra = run_one(t, a)
        print(f"   {a:<22} {ra['latency_s']:>6}s  {ra['tokens_per_s']} tok/s")
        rb = run_one(t, b)
        print(f"   {b:<22} {rb['latency_s']:>6}s  {rb['tokens_per_s']} tok/s")
        rows.append((t, ra, rb))

    stem = f"compare_{safe(a)}_vs_{safe(b)}"
    # CSV
    with open(RESULTS / f"{stem}.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["task_id", "category", "title",
                    f"{a}_latency_s", f"{a}_tok_s", f"{a}_out_tok",
                    f"{b}_latency_s", f"{b}_tok_s", f"{b}_out_tok"])
        for t, ra, rb in rows:
            w.writerow([t["id"], t["category"], t["title"],
                        ra["latency_s"], ra["tokens_per_s"], ra["output_tokens"],
                        rb["latency_s"], rb["tokens_per_s"], rb["output_tokens"]])

    # Markdown
    def avg(rs, side, key):
        vals = [r[side][key] for r in [(x[1], x[2]) for x in rows] if r[side][key]]
        return sum(vals) / len(vals) if vals else 0
    la = [r[1]["latency_s"] for r in rows]; lb = [r[2]["latency_s"] for r in rows]
    ta = [r[1]["tokens_per_s"] for r in rows if r[1]["tokens_per_s"]]
    tb = [r[2]["tokens_per_s"] for r in rows if r[2]["tokens_per_s"]]
    md = [f"# Head-to-head: `{a}` vs `{b}` (text tasks)\n",
          f"_{len(tasks)} text tasks · multimodal tasks skipped (coder models can't see images/audio)._\n",
          "## Speed summary\n",
          f"| Model | Avg latency | Avg tok/s |", "|---|--:|--:|",
          f"| `{a}` | {sum(la)/len(la):.1f}s | {sum(ta)/len(ta):.0f} |",
          f"| `{b}` | {sum(lb)/len(lb):.1f}s | {sum(tb)/len(tb):.0f} |\n",
          "## Per-task\n",
          f"| Task | `{a}` lat / tok-s | `{b}` lat / tok-s |", "|---|--:|--:|"]
    for t, ra, rb in rows:
        md.append(f"| {t['id']} {t['title']} | {ra['latency_s']}s / {ra['tokens_per_s']} "
                  f"| {rb['latency_s']}s / {rb['tokens_per_s']} |")
    md.append("\n---\n\n## Full outputs (judge quality yourself)\n")
    for t, ra, rb in rows:
        md.append(f"### {t['id']} — {t['title']}\n")
        md.append(f"**`{a}`** _({ra['latency_s']}s, {ra['tokens_per_s']} tok/s)_\n\n{ra['response'].strip()}\n")
        md.append(f"\n**`{b}`** _({rb['latency_s']}s, {rb['tokens_per_s']} tok/s)_\n\n{rb['response'].strip()}\n\n---\n")
    (RESULTS / f"{stem}.md").write_text("\n".join(md))
    print(f"\nWrote results/{stem}.md and .csv")


if __name__ == "__main__":
    main()
