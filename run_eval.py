#!/usr/bin/env python3
"""
run_eval.py — headless batch runner for the Gemma 4 12B PM evaluation.

Reads prompts/tasks.json, runs each task against the local model via
gemma_client, and writes:
  * results/results.md   — human-readable: each task's prompt + full output + stats
  * results/results.csv  — one row per task (latency, tokens/s, ok) for charts
  * results/run_log.jsonl — appended by the client (full history, all runs)

Usage:
  python run_eval.py                  # run everything
  python run_eval.py --list           # list tasks, don't run
  python run_eval.py --category 04_summarizing
  python run_eval.py --hero-only      # just the cross-model "hero" prompts
  python run_eval.py --task dw1 sum2  # specific task ids
  python run_eval.py --think on       # force Thinking Mode on (override per-task)

Video is handled as frames@1FPS via ffmpeg (Gemma sees a video as image
frames + its audio track). Audio tasks call the native-audio path and are
recorded as 'pending' if the local runtime can't accept audio yet.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import subprocess
import sys
import tempfile
import time

import gemma_client as gc

ROOT = pathlib.Path(__file__).resolve().parent
TASKS_PATH = ROOT / "prompts" / "tasks.json"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

TEXT_INPUT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".log"}
MAX_VIDEO_FRAMES = 12  # 1 FPS, capped to keep the prompt lightweight


def load_tasks() -> dict:
    if not TASKS_PATH.exists():
        sys.exit(f"No task manifest at {TASKS_PATH}. Create it first (Phase B2).")
    return json.loads(TASKS_PATH.read_text())


def resolve(p: str | None) -> pathlib.Path | None:
    if not p:
        return None
    path = (ROOT / p).resolve()
    if not path.exists():
        print(f"  ! input not found: {p}")
        return None
    return path


def extract_frames(video: pathlib.Path, outdir: pathlib.Path) -> list[str]:
    """Sample frames at 1 FPS (capped) with ffmpeg → list of jpg paths."""
    pattern = str(outdir / "frame_%03d.jpg")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video), "-vf", "fps=1",
         "-frames:v", str(MAX_VIDEO_FRAMES), "-loglevel", "error", pattern],
        check=True,
    )
    return sorted(str(p) for p in outdir.glob("frame_*.jpg"))


def build_prompt(task: dict, input_path: pathlib.Path | None) -> str:
    prompt = task["prompt"]
    if input_path and input_path.suffix.lower() in TEXT_INPUT_SUFFIXES:
        body = input_path.read_text(errors="replace")
        prompt = f"{prompt}\n\n--- BEGIN INPUT ({input_path.name}) ---\n{body}\n--- END INPUT ---"
    return prompt


def run_task(task: dict, think_override: bool | None) -> dict:
    tid, cat, modality = task["id"], task["category"], task.get("modality", "text")
    think = think_override if think_override is not None else task.get("think")
    input_path = resolve(task.get("input"))
    print(f"▶ {tid} [{cat}/{modality}] {task['title']}")

    try:
        if modality == "text":
            rec = gc.generate(build_prompt(task, input_path), task_id=tid,
                              category=cat, think=think)
        elif modality == "image":
            if not input_path:
                raise RuntimeError("image task missing input")
            rec = gc.generate(task["prompt"], images=[str(input_path)],
                              task_id=tid, category=cat, think=think)
        elif modality == "video":
            if not input_path:
                raise RuntimeError("video task missing input")
            rec = gc.analyze_video(task["prompt"], str(input_path),
                                   task_id=tid, category=cat)
        elif modality == "audio":
            if not input_path:
                raise RuntimeError("audio task missing input")
            rec = gc.analyze_audio(task["prompt"], str(input_path),
                                   task_id=tid, category=cat)
        else:
            raise RuntimeError(f"unknown modality {modality!r}")
        rec["ok"] = True
        rec["title"] = task["title"]
        rec["hero"] = task.get("hero", False)
        preview = rec["response"][:120].replace("\n", " ")
        print(f"  ✓ {rec['latency_s']}s | {rec.get('tokens_per_s')} tok/s | {preview}…")
        return rec
    except Exception as exc:  # noqa: BLE001
        print(f"  ✗ FAILED: {exc}")
        return {"task_id": tid, "category": cat, "modality": modality,
                "title": task["title"], "ok": False, "error": str(exc),
                "hero": task.get("hero", False), "response": ""}


def write_reports(records: list[dict]) -> None:
    # CSV (for charts)
    csv_path = RESULTS_DIR / "results.csv"
    cols = ["task_id", "category", "title", "modality", "think", "ok",
            "latency_s", "prompt_tokens", "output_tokens", "tokens_per_s", "hero"]
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow(r)

    # Markdown (readable)
    md = RESULTS_DIR / "results.md"
    ok = [r for r in records if r.get("ok")]
    lat = [r["latency_s"] for r in ok if r.get("latency_s")]
    tps = [r["tokens_per_s"] for r in ok if r.get("tokens_per_s")]
    lines = [
        "# Gemma 4 12B — PM Workbench Results",
        f"\n_Generated {time.strftime('%Y-%m-%d %H:%M')} · model `{gc.DEFAULT_MODEL}` "
        f"· {len(ok)}/{len(records)} tasks succeeded._\n",
        "## Summary",
        f"- Avg latency: **{(sum(lat)/len(lat)):.1f}s**" if lat else "- Avg latency: n/a",
        f"- Avg speed: **{(sum(tps)/len(tps)):.0f} tok/s**" if tps else "- Avg speed: n/a",
        "\n| Task | Category | Modality | Latency | tok/s | OK |",
        "|---|---|---|--:|--:|:--:|",
    ]
    for r in records:
        lines.append(
            f"| {r.get('task_id')} — {r.get('title','')} | {r.get('category')} "
            f"| {r.get('modality')} | {r.get('latency_s','–')}s "
            f"| {r.get('tokens_per_s','–')} | {'✅' if r.get('ok') else '❌'} |")
    lines.append("\n---\n\n## Full outputs\n")
    for r in records:
        lines.append(f"### {r.get('task_id')} — {r.get('title','')}")
        meta = (f"`{r.get('category')}` · {r.get('modality')} · "
                f"{r.get('latency_s','–')}s · {r.get('tokens_per_s','–')} tok/s")
        lines.append(f"_{meta}_\n")
        if r.get("ok"):
            lines.append(r.get("response", "").strip() + "\n")
        else:
            lines.append(f"> ❌ {r.get('error','(no output)')}\n")
    md.write_text("\n".join(lines))
    print(f"\nWrote {csv_path.name} and {md.name} to results/")


def main() -> None:
    ap = argparse.ArgumentParser(description="Gemma 4 12B PM eval runner")
    ap.add_argument("--category")
    ap.add_argument("--task", nargs="*")
    ap.add_argument("--hero-only", action="store_true")
    ap.add_argument("--think", choices=["on", "off"])
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    tasks = load_tasks()["tasks"]
    if args.category:
        tasks = [t for t in tasks if t["category"] == args.category]
    if args.task:
        tasks = [t for t in tasks if t["id"] in set(args.task)]
    if args.hero_only:
        tasks = [t for t in tasks if t.get("hero")]

    if args.list:
        for t in tasks:
            flag = " ⭐" if t.get("hero") else ""
            print(f"{t['id']:>5}  [{t['category']}/{t.get('modality','text')}]"
                  f"  {t['title']}{flag}")
        print(f"\n{len(tasks)} task(s).")
        return

    if not gc.is_ready():
        sys.exit(f"Model not ready. Pulled models: {gc.list_models()}\n"
                 f"Run: ollama pull {gc.DEFAULT_MODEL}")

    think_override = {"on": True, "off": False}.get(args.think)
    print(f"Running {len(tasks)} task(s) against {gc.DEFAULT_MODEL}…\n")
    records = [run_task(t, think_override) for t in tasks]
    write_reports(records)


if __name__ == "__main__":
    main()
