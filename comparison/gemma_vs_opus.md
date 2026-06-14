# Head-to-head: Gemma 4 12B (local) vs. Claude Opus 4.8 — 7 hero prompts

Same prompt, same synthetic input, run on both. Gemma 4 12B ran locally on a
MacBook Pro (M4 Max) via Ollama; Opus 4.8 answers are in
[`opus_baseline.md`](opus_baseline.md); Gemma's full outputs are in
[`../results/results.md`](../results/results.md).

**Scoring key:** 🟰 quality tie · 🔵 Opus better · 🟢 local good enough to ship.
Remember the standing context: local is **$0, private, offline**.

| # | Hero task | Gemma 4 12B (local) | Opus 4.8 | Verdict |
|---|---|---|---|---|
| dw1 | Stakeholder email | Clean, scannable, all 5 points, clear ask (30s) | Same structure, slightly tighter | 🟰 / 🟢 ship local |
| or1 | Plan → JSON → risks | Valid JSON, solid plan + risk table (72s) | JSON tied to PRD specifics (state machine, soft-lock) | 🔵 Opus more specific · 🟢 local usable |
| lc1 | Python CSV + chart | Runnable, correct top-3 logic (57s) | Runnable, reads file vs. inlined string | 🟰 verify either |
| sum1 | Summarize long PRD | **Cited section IDs**, found the missing-spec gap (72s) | Same gap, same citations | 🟰 genuinely at parity |
| vi1 | Read dashboard | All 6 KPIs exact, right "most concerning" (92s) | Same, **also caught the Wk-3 signup dip**, instant | 🔵 Opus (speed + extra catch) · 🟢 quality tie |
| au1 | Voice memo → actions | **Native on-device transcription** + actions (35s) | Same task (needs file upload in app) | 🟢 **local win** (native, free, private) |
| vd1 | Summarize demo video | All 5 slides from **frames + audio** (53s) | Same task (needs upload) | 🟢 **local win** (on-device video) |

## Read-out

- **Quality parity is the story.** On 4 of 7 heroes the outputs are effectively
  interchangeable. The summarization parity (`sum1`) was the biggest surprise — both
  cited section IDs and independently flagged the same missing spec.
- **Opus's edge is speed + the last 10%.** It replies instantly and occasionally
  catches one more thing (the Wk-3 signup dip in `vi1`), which matters most for
  high-stakes or rapid-iteration work.
- **Gemma's edge is structural, not quality:** it did native **audio and video**
  understanding **on-device for $0**, fully private. For a PM's voice memos, call
  recordings, and screen demos, that's a daily-driver capability the cloud charges
  for and sends off-device.

**If I had to draw the line:** use **local Gemma 4 12B** for drafting, summarizing,
OCR/vision, and audio/video — especially anything sensitive. Keep **Opus 4.8** for
speed-critical, highest-stakes, or hardest-reasoning work.
