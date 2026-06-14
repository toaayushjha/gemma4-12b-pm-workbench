# LinkedIn post (draft)

> Format for LinkedIn: short lines, white space, no markdown headers. Paste the body
> below. Suggested hero image: `results/screenshots/13_verdict_map.png` (the verdict
> map) or a carousel of 3–4 screenshots. Link the repo/site in the first comment
> (LinkedIn suppresses reach on posts with outbound links in the body).

---

I gave an AI a product manager's entire daily workload — and it ran 100% on my laptop. No cloud. No API bill. No data ever leaving my machine.

Here's what surprised me. 👇

This month Google released **Gemma 4 12B** — a frontier open model (Apache 2.0) small enough to run on a laptop. I'd never run a local model before, so I set one up on my MacBook Pro and ran 22 real PM tasks against it across 7 categories — then compared it head-to-head with the cloud model I use every day, Claude Opus 4.8.

The setup took about 30 minutes. Total cost: $0.

What it handled — at quality I'd genuinely ship:

✍️ Turned messy meeting notes into a clean action-item table (and flagged the ambiguous owners I'd glossed over)
📄 Summarized a long PRD — and cited the exact section IDs, then caught a spec that was actually missing
📊 Read a KPI dashboard screenshot and correctly called out the one concerning metric
🎙️ Transcribed a voice memo AND diarized a two-speaker clip (Speaker A / Speaker B) — natively, on-device
🎬 Summarized a screen-demo video from its frames + audio

That audio and video part? Running locally, for free, on a 12B model. I did not expect that.

The honest catch:
⏱️ Speed. Cloud replies feel instant; locally I waited 30–90 seconds on the heavy tasks.
🔍 Trust-but-verify on code and any extracted numbers.

My takeaway as a PM:
→ For drafting, summarizing, OCR/vision, and audio — local is now a real daily driver, especially for anything sensitive.
→ For speed, the highest-stakes work, and the hardest reasoning — I still reach for Opus.

The gap is smaller than I expected. And "it never leaves my laptop" changes the calculus for a lot of work.

I open-sourced the whole workbench — code, the 22-task prompt pack, every output, and the scoring — so you can reproduce it in ~30 minutes. Link in comments.

What would you run on a private, local model first?

#AI #ProductManagement #LocalLLM #Gemma #OpenSource #OnDeviceAI

---

**First-comment link** (post as a reply to your own post so reach isn't suppressed):
Repo → https://github.com/toaayushjha/gemma4-12b-pm-workbench
Live results → https://toaayushjha.github.io/gemma4-12b-pm-workbench/
