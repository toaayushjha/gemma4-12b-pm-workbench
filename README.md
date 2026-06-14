# Gemma 4 12B — a PM's local AI workbench 🧪

> Can a **free, 100% on-device** open model replace the cloud LLM a product manager
> reaches for every day? I (a PM with **zero** prior local-model experience) put
> Google's brand-new **Gemma 4 12B** through the real PM workflows I'd normally use
> **Claude Opus 4.8** for — daily writing, orchestration, light coding, summarizing,
> and image / audio / video analysis — all running on a MacBook Pro. No API keys, no
> bills, no data leaving the laptop.

**Model:** `gemma4:12b` (released 2026-06-03, Apache 2.0) · **Engine:** Ollama (MLX on
Apple Silicon) · **UI:** Gradio + LM Studio · **Machine:** MacBook Pro M4 Max, 64 GB.

🌐 **Live results page:** https://toaayushjha.github.io/gemma4-12b-pm-workbench/

📊 **Results & verdicts:** [`results/findings.md`](results/findings.md) ·
🧮 **Raw outputs:** [`results/results.md`](results/results.md) ·
✍️ **Write-ups:** [`blog/`](blog/)

---

## TL;DR

- Gemma 4 12B is **natively multimodal** — text, image, **audio**, and video
  (frames + audio) — in a single 12B model that fits comfortably in laptop RAM.
- It runs locally at **~45 tokens/sec** on an M4 Max, **$0**, fully offline.
- The interesting, non-obvious finding for builders: **native audio/video input
  works through Ollama's OpenAI-compatible `/v1/chat/completions` endpoint using
  `input_audio` content parts** — *not* the native `/api/chat` `images`-style field.
- Per-task verdicts (where local is "good enough" vs. where I'd still reach for
  Opus) are in [`results/findings.md`](results/findings.md).

## The stack (all free, all local)

| Layer | Tool | Why |
|---|---|---|
| Engine | **Ollama** | One command to pull/run; OpenAI-compatible API on `localhost:11434` |
| Custom UI | **Gradio** (`app.py`) | PM-friendly tabs: chat, benchmark, audio, results |
| Quick GUI | **LM Studio** | Zero-setup chat + drag-in files for screenshots/demos |
| Media prep | **ffmpeg** | Video → frames @1 FPS + 16 kHz audio track |
| Harness | **Python (stdlib)** (`gemma_client.py`, `run_eval.py`) | Batch-run + log latency/tokens |
| Baseline | **Claude Opus 4.8** | Head-to-head on 7 "hero" prompts ([`comparison/`](comparison/)) |

## Quickstart (reproduce in ~30 min)

**Prerequisites:** macOS (Apple Silicon), [Ollama](https://ollama.com),
[`uv`](https://docs.astral.sh/uv/), and `ffmpeg` (`brew install ffmpeg`).

```bash
# 1. Pull the model (~7.6 GB)
ollama pull gemma4:12b

# 2. Set up the Python env
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 3. Generate the synthetic test inputs (images, audio, video — all fake data)
python make_inputs.py

# 4a. Run the full benchmark headless → results/results.md + results.csv
python run_eval.py
#   ...or a subset:
python run_eval.py --hero-only
python run_eval.py --category 06_audio

# 4b. ...or explore interactively in the workbench UI
python app.py            # opens http://127.0.0.1:7860
```

## The workbench (`app.py`)

A friendly local web app — no model code to touch:

- **💬 Chat** — text + image, streaming, with a Thinking-Mode toggle and a live
  latency / tokens-per-second readout.
- **🧪 Benchmark** — pick any task from `prompts/tasks.json`, run it, see output + speed.
- **🎙 Audio** — record/upload a clip for native speech understanding.
- **📊 Results** — render the latest `results/results.md`.

> _(Screenshots in [`results/screenshots/`](results/screenshots/).)_

## What's tested (7 PM categories, 22 tasks)

| # | Category | Example task |
|---|---|---|
| 01 | Daily workflows | Notes → stakeholder email; messy notes → action-item table; RICE |
| 02 | Orchestration | goal → plan → **valid JSON** task list → risk table; tool-routing |
| 03 | Light coding | CSV→chart script; SQL from schema; refactor; regex + tests |
| 04 | Summarizing | long PRD → TL;DR + decisions + risks (uses the **256K** context) |
| 05 | Vision (image) | read a KPI dashboard; chart→table; OCR a memo; critique a UI |
| 06 | Audio | transcribe a voice memo; 2-speaker **diarization** + decision |
| 07 | Video | summarize a screen-demo (frames + audio); list features shown |

All inputs are **synthetic / self-generated** (`make_inputs.py` + `inputs/`), so this
repo is safe to publish. See **[scoring/rubric.md](scoring/rubric.md)** for how each
task is scored and how the "local vs. Opus" verdict is decided.

## Gemma 4 12B — capability notes

- **Inputs:** text + image + **audio** (the 12B is the audio-capable size; the larger
  26B/31B are text+image only). Context window **256K**. Built-in **Thinking Mode**.
- **Encoder-free:** vision and audio project directly into the LLM backbone (no
  separate encoders) — low multimodal latency.
- **Video = frames + audio.** There's no separate video input; sample frames @1 FPS
  and pass them with the 16 kHz audio track (`gemma_client.analyze_video`).
- **Native audio plumbing (the gotcha):** use Ollama's **`/v1/chat/completions`** with
  `{"type": "input_audio", "input_audio": {"data": <b64>, "format": "wav"}}`. The
  native `/api/chat` `audio`/`audios` fields are ignored on this build (see
  `results/audio_probe.txt`).

## Privacy & data

Nothing leaves the machine. All test inputs are fabricated. No real customer or
company data is used anywhere in this repo — by design, since the findings are public.

## Project structure

```
.
├── gemma_client.py     # local client (text/image via /api/chat; audio/video via /v1)
├── run_eval.py         # headless batch runner → results/
├── app.py              # Gradio workbench UI
├── make_inputs.py      # generates all synthetic image/audio/video inputs
├── prompts/tasks.json  # the 22-task manifest
├── inputs/             # synthetic docs / images / audio / video
├── scoring/            # rubric.md + scorecard.csv
├── results/            # results.md, results.csv, findings.md, screenshots/
├── comparison/         # Gemma 4 vs Claude Opus 4.8 (hero prompts)
├── blog/               # LinkedIn + Substack drafts
└── docs/               # GitHub Pages findings site
```

## Credits & license

Built with [Claude Code](https://claude.com/claude-code). Uses Google's
[Gemma 4](https://ai.google.dev/gemma) (Apache 2.0) and the official
[`gemma-dev`](https://github.com/google-gemma/gemma-skills) skill. This is a personal
exploration, not affiliated with or endorsed by Google. Code in this repo: MIT.
