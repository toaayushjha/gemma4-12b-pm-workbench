# LinkedIn posts (drafts — paste into LinkedIn yourself)

> Format for LinkedIn: short lines, white space, no markdown headers. Put the repo/site
> link in the **first comment** (LinkedIn suppresses reach on posts with outbound links in
> the body). Suggested hero image: the model line-up table from the site, or
> `results/screenshots/site_full.png`.
>
> Links for the first comment:
> Repo → https://github.com/toaayushjha/gemma4-12b-pm-workbench
> Live results → https://toaayushjha.github.io/gemma4-12b-pm-workbench/

---

## ▶ Post A — Local model showdown + my pick (post this one)

I tried to replace my daily cloud-AI habit with models running 100% on my laptop. I benchmarked four. Here's the setup I'm keeping. 👇

The rig: a MacBook Pro (M4 Max, 64 GB). Everything local — no API bills, no data ever leaving the machine. The yardstick: Claude Opus 4.8, what I use every day as a PM.

The contenders (all free, all open, all local):
• Gemma 4 12B — Google's new multimodal model (text + image + audio + video)
• Qwen3-Coder 30B — a Mixture-of-Experts (only ~3B active per token)
• Qwen3-Coder-Next 80B — the big one

What 14 real PM tasks showed (emails, notes→action items, summaries, SQL, JSON, code):

⚡ Speed — the 30B MoE ran ~5× faster than Gemma (110 vs 46 tokens/sec).
🧠 Quality — on everyday text and code, local was at parity with what I'd get from the cloud.
🐘 Bigger ≠ better — the 80B was actually SLOWER per token than the 30B and ate 45 GB of RAM, for a quality edge so small it wasn't worth it (it even flubbed a multi-part task and leaked a stray non-English token into JSON).
🎙️ The exception — Gemma 4 12B does on-device audio: transcription AND speaker diarization, plus video. The Qwen coders are text-only.

My setup going forward:
✅ Qwen3-Coder 30B (MoE) → default for most daily text + code. Fast, free, private.
✅ Gemma 4 12B → audio + vision.
✅ Claude Opus 4.8 → reserved for the hardest 10–20%.

The part that surprised me as a non-engineer: for a huge share of daily PM work, a free model on a laptop is now genuinely good enough — and "it never leaves my device" is a feature, not a compromise.

Full benchmark, the workbench code, and every raw output are open-source (link in the comments).

What would you run locally first?

#AI #ProductManagement #LocalLLM #OpenSource #Qwen #Gemma #OnDeviceAI

---

## ▶ Post B — Gemma vs Opus (alternate angle)

I gave an AI a product manager's entire daily workload — and it ran 100% on my laptop. No cloud. No API bill. No data ever leaving my machine.

Here's what surprised me. 👇

This month Google released **Gemma 4 12B** — a frontier open model small enough to run on a laptop. I'd never run a local model before, so I set one up on my MacBook Pro and ran 22 real PM tasks against it, then compared it head-to-head with the cloud model I use every day, Claude Opus 4.8.

Setup took ~30 minutes. Total cost: $0.

What it handled at quality I'd genuinely ship:
✍️ Messy meeting notes → a clean action-item table (it even flagged the ambiguous owners)
📄 A long PRD → summary that cited section IDs and caught a missing spec
📊 A KPI dashboard screenshot → the one metric I should worry about
🎙️ A voice memo transcribed AND a two-speaker clip diarized — natively, on-device
🎬 A screen-demo video summarized from its frames + audio

The honest catch: speed (30–90s on heavy tasks) and trust-but-verify on code.

My takeaway: for drafting, summarizing, OCR/vision, and audio, local is now a real daily driver — especially for anything sensitive. I still reach for Opus on the hardest, highest-stakes work.

Open-sourced the whole thing so you can reproduce it (link in comments).

#AI #ProductManagement #LocalLLM #Gemma #OpenSource #OnDeviceAI
