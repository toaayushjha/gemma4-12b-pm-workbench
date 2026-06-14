# I ran a frontier AI model 100% on my laptop. Here's what it can (and can't) replace for a PM.

### A product manager with zero local-model experience puts Google's new Gemma 4 12B up against Claude Opus 4.8 — free, private, and entirely offline.

---

*Everything below ran on a MacBook Pro with no internet connection required, no API
keys, and no data ever leaving the machine. Every test input is fabricated. The full
workbench is open-source — link at the bottom.*

---

## Why I did this

I use a cloud AI model (Claude Opus 4.8) for a big chunk of my work as a product
manager — drafting updates, turning notes into action items, summarizing long docs,
sanity-checking a bit of SQL. It's excellent. But it's also a subscription, it lives in
someone else's data center, and anything I paste into it leaves my laptop.

This month Google released **Gemma 4 12B** — an open-weight model (Apache 2.0) that's
small enough to run on a laptop but genuinely multimodal: text, images, **audio**, and
video, all in one 12-billion-parameter model. I'd never run a local model in my life. So
I gave myself a weekend project: **set one up, throw my real daily workload at it, and
see where a free, private, on-device model is "good enough" to replace the cloud.**

Spoiler: further than I expected.

## The setup (about 30 minutes)

The whole local stack is free and, on a Mac, mostly a few commands:

- **Ollama** — the engine. One command pulls and runs the model: `ollama pull gemma4:12b`.
- **A simple web UI** (I built a small Gradio "workbench" with tabs for chat, the
  benchmark, and audio) plus **LM Studio** for quick drag-and-drop demos.
- **ffmpeg** — to turn a video into frames + an audio track (more on that below).

The model is a 7.6 GB download. On my M4 Max (64 GB) it loads in seconds and runs at
roughly **27 tokens/second** on text — fast enough to read along with.

> 📸 *[screenshot: `01_ollama_pull.png` — pulling the model]*
> 📸 *[screenshot: `05_workbench_chat.png` — the workbench UI]*

## What I tested

I wrote a 22-task "prompt pack" across the seven things I actually use AI for as a PM:

1. **Daily workflows** — stakeholder emails, messy-notes→action-items, exec-tone rewrites, RICE prioritization
2. **Orchestration** — multi-step plans, strict JSON output, tool-routing decisions
3. **Light coding** — Python, SQL, refactoring, regex
4. **Summarizing** — a long PRD, a support thread, a meeting transcript
5. **Vision** — reading a KPI dashboard, a chart, a scanned memo, a UI mockup
6. **Audio** — transcribing a voice memo, diarizing a two-speaker clip
7. **Video** — summarizing a screen-demo recording

Then I ran seven "hero" prompts head-to-head against Claude Opus 4.8.

**Result: 22 out of 22 tasks produced usable output.** Here's where it got interesting.

## What genuinely impressed me

**Summarizing was the standout.** I gave it a long product-requirements doc and asked
for a TL;DR, key decisions, and open risks. It not only nailed the summary — it **cited
the section IDs** (D1, FR5, OQ3…) and flagged a spec that was *actually missing* from the
doc (an undefined "target-account list"). That's the kind of read a senior PM does.

> 📸 *[screenshot: `11_results_table.png` — the results table]*

**Vision worked far better than I assumed.** Fed a screenshot of a metrics dashboard, it
listed all six KPIs with exact values and trends, then correctly singled out the one
concerning number (activation rate down 2%) with sound reasoning. It turned a bar chart
into a clean table — with the correct total — and OCR'd a deliberately messy "scanned"
memo almost perfectly.

> 📸 *[screenshot: `06_workbench_vision.png` — reading the dashboard]*

**And then the part I didn't believe until I saw it: native audio and video.** On-device,
for free, the 12B model:

- transcribed a voice memo and pulled out the action items with owners, and
- **diarized** a two-speaker clip — labeling Speaker A and Speaker B and extracting the
  decision they reached — in about 19 seconds.

> 📸 *[screenshot: `15_audio_diarization.png` — the diarized transcript]*

For video, there's a useful mental model: Gemma doesn't have a separate "video" input. You
sample frames (I used 1 per second) and pass them alongside the audio track. Given a short
product-demo recording, it walked through all five slides and wrote a release-notes
summary — using both what it *saw* in the frames and what it *heard* in the narration.

> 📸 *[screenshot: `16_video_summary.png` — the video summary]*

## The head-to-head with Opus 4.8

On four of the seven hero prompts, the outputs were effectively interchangeable. The PRD
summary was a genuine tie — both models cited sections and independently caught the same
missing spec.

Where Opus pulled ahead: **speed** (instant vs. 30–90 seconds locally) and **the last
10%** — on the dashboard task it caught one extra anomaly (a dip in weekly signups) that
Gemma didn't mention. For high-stakes or rapid back-and-forth work, that adds up.

Where local won outright: **audio and video understanding, on-device, for $0, fully
private.** For a PM's voice memos, call recordings, and screen demos, that's a real
daily-driver capability — and the cloud charges for it and sends your media off-device.

## Three things I learned

1. **The quality gap is smaller than the marketing would suggest.** For everyday PM work
   — writing, summarizing, reading documents and images — a free local model is now
   genuinely good. The decision is less "is it smart enough?" and more "is the latency
   worth the privacy?"

2. **A builder gotcha worth saving someone an afternoon:** native audio/video input
   doesn't go through Ollama's usual API field. You have to use its OpenAI-compatible
   `/v1/chat/completions` endpoint with `input_audio` content parts. The "obvious" native
   path silently ignores the audio and the model just asks you to "please provide the
   file."

3. **It has no idea it's local.** When I asked the model what it was, it cheerfully told
   me it was "running on remote servers." It was, in fact, running on my laptop with the
   Wi-Fi off. Which is the entire point.

## The honest caveats

- **Latency is the tax.** Budget 30–90 seconds for long or multimodal tasks. Great for
  "kick it off and grab coffee," less so for rapid iteration.
- **Verify code, SQL, and extracted numbers.** Quality is high but not infallible — treat
  it as a fast first draft.
- **"Video" loses motion.** Sampling frames at 1 FPS is fine for slide-style content,
  weaker for anything fast-moving.

## So, would I actually use it?

Yes — for a specific, large slice of my work. My rule of thumb now:

- **Local Gemma 4 12B** for drafting, summarizing, OCR/vision, and audio/video —
  *especially* anything I'd rather not send to a cloud.
- **Claude Opus 4.8** for speed-critical work, the highest-stakes outputs, and the
  hardest reasoning.

For a PM who handles sensitive material, "it never leaves my laptop" is a surprisingly
freeing default.

## Reproduce it yourself

I open-sourced the entire workbench — the code, the 22-task prompt pack, the synthetic
inputs, every raw output, the scoring, and the head-to-head — so you can run it in about
30 minutes:

**👉 [GitHub repo](https://github.com/toaayushjha/gemma4-12b-pm-workbench)**  ·  **[Live results page](https://toaayushjha.github.io/gemma4-12b-pm-workbench/)**

If you try it, I'd love to hear which task you'd trust to a local model first.

---

*Built with Claude Code. Uses Google Gemma 4 (Apache 2.0). A personal exploration, not
affiliated with or endorsed by Google or Anthropic. All test data is synthetic.*
