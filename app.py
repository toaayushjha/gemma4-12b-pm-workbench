#!/usr/bin/env python3
"""
app.py — the PM Workbench: a friendly local web UI for Gemma 4 12B.

100% local. Backed by Ollama (so a PM doesn't touch model code). Three tabs:
  1. Chat        — text + image, streaming, with a Thinking-Mode toggle and a
                   live latency / tokens-per-second readout.
  2. Benchmark   — pick a task from prompts/tasks.json, run it, see the output
                   and stats. Every run is logged to results/run_log.jsonl.
  3. Audio       — native speech understanding (transcribe / summarise a clip).
  4. Results     — render the latest results/results.md.

Run:  source .venv/bin/activate && python app.py   (opens http://127.0.0.1:7860)

NOTE: this deliberately uses Ollama instead of raw `transformers` (the
gemma-dev skill's default) — it's easier for a non-engineer and the engine is
already running. Swap GEMMA_MODEL / OLLAMA_URL via env vars.
"""
from __future__ import annotations

import json
import pathlib
import time

import gradio as gr

import gemma_client as gc

ROOT = pathlib.Path(__file__).resolve().parent
TASKS = json.loads((ROOT / "prompts" / "tasks.json").read_text())["tasks"] \
    if (ROOT / "prompts" / "tasks.json").exists() else []
RESULTS_MD = ROOT / "results" / "results.md"

INTRO = """
# 🧪 Gemma 4 12B — PM Workbench
**Frontier multimodal AI, 100% on your laptop. Free. Private. No data leaves this machine.**

Engine: local **Ollama** · Model: `{model}` · {status}
""".strip()


def status_line() -> str:
    models = gc.list_models()
    ok = gc.is_ready()
    return ("✅ model ready" if ok else "⏳ not pulled yet — run `ollama pull "
            f"{gc.DEFAULT_MODEL}`") + f"  ·  local models: {', '.join(models) or 'none'}"


# --------------------------------------------------------------------------- #
# Chat tab
# --------------------------------------------------------------------------- #
def chat_respond(message: dict, history: list, think: bool, temp: float):
    text = message.get("text", "") if isinstance(message, dict) else str(message)
    files = message.get("files", []) if isinstance(message, dict) else []
    images = [f for f in files if str(f).lower().endswith(
        (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"))]
    t0 = time.time()
    partial = ""
    try:
        for partial in gc.generate_stream(
            text, images=images or None, think=think, temperature=temp):
            yield partial
    except Exception as exc:  # noqa: BLE001
        yield f"⚠️ {exc}"
        return
    dt = time.time() - t0
    yield partial + f"\n\n_⏱ {dt:.1f}s · 🖼 {len(images)} image(s) · think={think}_"


# --------------------------------------------------------------------------- #
# Benchmark tab
# --------------------------------------------------------------------------- #
def run_benchmark(task_label: str, think_choice: str):
    task = next((t for t in TASKS if _label(t) == task_label), None)
    if not task:
        return "Pick a task.", ""
    think = {"task default": None, "on": True, "off": False}[think_choice]
    input_path = (ROOT / task["input"]) if task.get("input") else None
    modality = task.get("modality", "text")
    try:
        if modality == "image" and input_path:
            rec = gc.generate(task["prompt"], images=[str(input_path)],
                              task_id=task["id"], category=task["category"], think=think)
        else:  # text (inline any text input)
            prompt = task["prompt"]
            if input_path and input_path.suffix.lower() in {".md", ".txt", ".csv"}:
                prompt += f"\n\n--- INPUT ---\n{input_path.read_text(errors='replace')}"
            rec = gc.generate(prompt, task_id=task["id"],
                              category=task["category"], think=think)
        stats = (f"**⏱ {rec['latency_s']}s · {rec.get('tokens_per_s','–')} tok/s · "
                 f"{rec.get('output_tokens','–')} tokens · think={think}**")
        return rec["response"], stats
    except Exception as exc:  # noqa: BLE001
        return f"⚠️ {exc}", ""


def _label(t: dict) -> str:
    star = " ⭐" if t.get("hero") else ""
    return f"[{t['category']}/{t.get('modality','text')}] {t['id']} — {t['title']}{star}"


# --------------------------------------------------------------------------- #
# Audio tab
# --------------------------------------------------------------------------- #
def run_audio(audio_path: str, prompt: str):
    if not audio_path:
        return "Upload or record a short clip first."
    try:
        rec = gc.analyze_audio(prompt or "Transcribe this audio, then summarise it "
                               "and list any action items.", audio_path)
        return (f"**⏱ {rec['latency_s']}s · backend: {rec.get('audio_backend')}**\n\n"
                + rec["response"])
    except Exception as exc:  # noqa: BLE001
        return (f"⚠️ Native audio isn't wired up on this runtime yet.\n\n`{exc}`\n\n"
                "See README → *Audio understanding* for the confirmed local path.")


def load_results() -> str:
    return RESULTS_MD.read_text() if RESULTS_MD.exists() else \
        "_No results yet. Run `python run_eval.py`._"


# --------------------------------------------------------------------------- #
# Layout
# --------------------------------------------------------------------------- #
with gr.Blocks(title="Gemma 4 12B — PM Workbench", theme=gr.themes.Soft()) as demo:
    gr.Markdown(INTRO.format(model=gc.DEFAULT_MODEL, status=status_line()))

    with gr.Tab("💬 Chat"):
        with gr.Row():
            think_tg = gr.Checkbox(label="Thinking Mode", value=False)
            temp_sl = gr.Slider(0.0, 1.5, value=0.7, step=0.1, label="Temperature")
        gr.ChatInterface(
            fn=chat_respond,
            type="messages",
            multimodal=True,
            additional_inputs=[think_tg, temp_sl],
            description="Type a message. Attach an image with the 📎 clip to test vision.",
        )

    with gr.Tab("🧪 Benchmark"):
        gr.Markdown("Run a predefined PM task from `prompts/tasks.json` and see the output + speed.")
        with gr.Row():
            task_dd = gr.Dropdown([_label(t) for t in TASKS], label="Task",
                                  value=_label(TASKS[0]) if TASKS else None, scale=4)
            think_dd = gr.Dropdown(["task default", "on", "off"],
                                   value="task default", label="Thinking Mode", scale=1)
        run_btn = gr.Button("Run task", variant="primary")
        bench_stats = gr.Markdown()
        bench_out = gr.Markdown(label="Output")
        run_btn.click(run_benchmark, [task_dd, think_dd], [bench_out, bench_stats])

    with gr.Tab("🎙 Audio"):
        gr.Markdown("Native speech understanding (ASR + reasoning). Record or upload a clip.")
        audio_in = gr.Audio(type="filepath", label="Audio clip")
        audio_prompt = gr.Textbox(label="Instruction",
                                  value="Transcribe this, then summarise and list action items.")
        audio_btn = gr.Button("Analyse audio", variant="primary")
        audio_out = gr.Markdown()
        audio_btn.click(run_audio, [audio_in, audio_prompt], audio_out)

    with gr.Tab("📊 Results"):
        res_md = gr.Markdown(load_results())
        gr.Button("Refresh").click(load_results, outputs=res_md)


if __name__ == "__main__":
    demo.launch(inbrowser=True)
