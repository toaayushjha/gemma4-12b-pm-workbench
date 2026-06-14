# Scoring rubric — "Could a PM use local Gemma 4 12B instead of Claude Opus 4.8?"

This eval is **not** "which model is smarter." It asks a practical question for a
product manager: **for this kind of task, is a free, private, on-my-laptop model
good enough to replace the cloud model I'd normally reach for?**

Every task is scored on four 1–5 dimensions, plus a one-word verdict.

## Dimensions (1 = poor, 5 = excellent)

| Dimension | Question | 5 looks like… |
|---|---|---|
| **Quality** | Is the output correct, complete, and genuinely useful? | I'd ship/use it nearly as-is |
| **Speed** | Did it respond fast enough for the workflow? | Felt instant / faster than typing it myself |
| **Reliability** | Did it follow the format/instructions (valid JSON, table, length)? | Followed every constraint, repeatably |
| **Effort** | How much prompt-wrangling did getting a good answer take? | One prompt, no babysitting |

> Speed is also captured **objectively** by the harness (latency + tokens/sec in
> `results/results.csv`). The 1–5 score is the *felt* experience.

## Verdict (the headline)

For each task pick one:
- **✅ Local** — good enough; I'd use Gemma 4 locally for this and not miss Opus.
- **🟡 Caveats** — usable with edits / for drafts / for non-critical work.
- **❌ Opus** — I'd still reach for Claude Opus 4.8 here.

## The standing context (true for every row)

Local Gemma 4 12B always wins on three axes regardless of quality:
- **Cost:** $0 — no API bills, no subscription.
- **Privacy:** 100% local — no data leaves the laptop (matters for anything sensitive).
- **Offline:** works on a plane / with no network.

So the real question per task is: *does the quality/speed clear the bar where those
three free wins are worth it?*

## How to fill it in

1. Run `python run_eval.py` (text/image) and use the **Audio/Video** tabs in `app.py`.
2. Read each output in `results/results.md`.
3. Score in `scorecard.csv` (open in Numbers/Excel) — one row per task.
4. Roll up to a **per-category verdict** and the headline **"where local wins vs.
   where Opus still wins"** map in `results/findings.md` (built in Phase C/D).

## Reading the map (example)

| Category | Likely verdict | Why (fill after running) |
|---|---|---|
| Daily workflows (emails, notes) | ✅ Local | drafting is forgiving; privacy is a bonus |
| Summarizing | ✅ / 🟡 | 256K context helps; check factual fidelity |
| Light coding | 🟡 | fine for snippets; verify before running |
| Orchestration / strict JSON | 🟡 / ❌ | watch format adherence & multi-step drift |
| Vision (dashboards, OCR) | 🟡 / ✅ | strong on OCR; check number-reading accuracy |
| Audio (transcribe/summarize) | ? | the novel test — confirm native vs. fallback |
| Video (frames + audio) | ? | frame sampling loses motion; judge accordingly |

_(Verdicts above are hypotheses to test, not conclusions.)_
