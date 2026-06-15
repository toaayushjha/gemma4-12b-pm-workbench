# Findings — Gemma 4 12B as a PM's local AI (vs. Claude Opus 4.8)

_MacBook Pro M4 Max, 64 GB · `gemma4:12b` via Ollama · 22 tasks, 7 categories ·
all inputs synthetic. Raw outputs: [`results.md`](results.md) · scores:
[`../scoring/scorecard.csv`](../scoring/scorecard.csv)._

## Headline

A 12B open model running **100% on a laptop, for $0, with no data leaving the
machine** handled the **large majority of everyday PM work at a quality I'd
genuinely ship** — including the things I expected it to fail: reading a dashboard,
transcribing and **diarizing** audio, and summarizing a video. **22/22 tasks
succeeded.** The real cost isn't quality — it's **latency** (30–90s on heavy tasks)
and the need to **verify** code and extracted facts.

## By the numbers

- **22 / 22** tasks completed with usable output.
- **Text speed:** ~**22–44 tok/s** (short prompts hit 40+ tok/s).
- **Latency:** text 19–77s · image 18–92s · audio 19–35s · video 30–53s.
- **Avg latency 44s · avg 24 tok/s.**
- **Cost: $0.** **Network used: none.** **Data sent to a third party: none.**

## The verdict map

| Category | Verdict | Why |
|---|---|---|
| **01 Daily workflows** (emails, notes→actions, exec rewrites, RICE) | ✅ **Use local** | Drafting is forgiving and it nailed structure, tone, and even flagged ambiguous owners. Privacy is a bonus. |
| **02 Orchestration** (multi-step, strict JSON, tool routing) | ✅ **Use local** | JSON schema adherence was clean and tool-routing was sensible. Validate JSON in prod. |
| **03 Light coding** (Python, SQL, refactor, regex) | 🟡 **With caveats** | Correct and idiomatic for snippets (nailed the O(n²) refactor + regex). **Verify before running.** |
| **04 Summarizing** (long PRD, threads, transcripts) | ✅ **Use local** | Best category. Accurate, **cited section IDs**, found a real gap. 256K context = paste whole docs. |
| **05 Vision** (dashboards, charts, OCR, UI critique) | ✅ **Use local** | Read exact KPI values, extracted a chart to a table (correct total), near-perfect OCR. Slower (≤92s). |
| **06 Audio** (transcribe, **diarize**) | ✅ **Use local** ⭐ | The surprise. Accurate transcription and clean Speaker A/B diarization, on-device, in ~20–35s. |
| **07 Video** (screen-demo summary) | 🟡 **With caveats** | Great on slide-style content via frames+audio; **motion is lost** (1 FPS) and it's the slowest. |

## Where local Gemma 4 wins

- **Summarizing & writing.** PRD review with section citations, support-thread
  condensation, meeting-transcript → decisions/owners/parking-lot. Ship-ready.
- **Audio.** Native, accurate transcription + diarization with no Whisper, no cloud.
  For a PM doing voice memos and call notes, this alone is a daily-driver feature.
- **Vision/OCR.** Read a KPI dashboard exactly, turned a bar chart into a correct
  table ($24,800 total), and OCR'd a "scanned" memo almost perfectly.
- **The unbeatable trio:** **$0**, **private**, **offline**. For anything sensitive,
  "it never leaves my laptop" outweighs a lot.

## Where I'd still reach for Claude Opus 4.8

- **Speed.** Opus replies feel instant; Gemma took 30–92s on long-output and
  multimodal tasks. For interactive, back-and-forth work that friction adds up.
- **High-stakes correctness.** For code I'll run in production or SQL on real data,
  I want the higher reliability bar (and I'd verify either way).
- **The hardest reasoning / largest contexts / agentic chains.** The 12B is strong,
  but Opus has more headroom when tasks get genuinely hard or long-horizon.

## Standout moments

- **Diarization just worked** locally: labeled two speakers and extracted the
  decision in 19s (`au2`).
- **PRD summary cited section IDs** (D1, FR5, OQ3…) and flagged a *real* missing
  spec — the undefined "target-account list" (`sum1`).
- **Chart → table** was numerically exact, including the computed total (`vi2`).
- **Refactor** correctly diagnosed O(n²) and produced the idiomatic
  `list(dict.fromkeys(l))` (`lc3`).

## Honest caveats

- **Latency is the tax.** Budget 30–90s for long or multimodal tasks. Great for
  "do this while I get coffee," less so for rapid iteration.
- **Verify code/SQL/extractions.** Quality is high but not infallible; treat as a
  fast first draft.
- **"Video" = frames + audio.** At 1 FPS you lose motion/timing nuance; fine for
  slide-style demos, weaker for fast action.
- **It doesn't know it's local.** Asked what it is, it said it runs "on remote
  servers." It has no idea it's on your laptop — which is the whole point.

## Bonus: a fully-local "ask my docs" assistant

Using **EmbeddingGemma** (300M) to index the synthetic docs and Gemma 4 12B to answer,
a tiny local RAG ([`../rag.py`](../rag.py)) answered a cross-document question —
*"what did we decide about the trial credit-card requirement, and the biggest launch
risk?"* — by pulling from both the meeting transcript and the PRD, **with citations**,
and honestly noting the docs list five risks rather than one (no hallucinated "single"
risk). A private, on-device knowledge assistant over your own files, for $0.

## Update: the latency lever — Qwen3-Coder 30B (MoE)

The biggest fix for the latency tax wasn't a Gemma setting — it was a *different model*
for text. On the 14 text tasks, **Qwen3-Coder 30B (a ~3B-active MoE) ran ~5× faster**
than Gemma 4 12B (avg **6.0s vs 28.3s**, **110 vs 46 tok/s**) and was **equal-or-better
on code, JSON/agentic, and summarizing** — it even produced a correct anchored regex
where Gemma dropped the `^…$` anchors this run. Gemma kept the edge on RICE methodology
and more polished prose, and of course on **multimodal** (Qwen is text-only).

**The setup that emerged:** Qwen3-Coder 30B as the fast, free **text / code / agent**
workhorse; Gemma 4 12B for **multimodal** (vision / audio / video). Full side-by-side:
[`compare_gemma4-12b_vs_qwen3-coder-30b.md`](compare_gemma4-12b_vs_qwen3-coder-30b.md).

## Bottom line

For a PM, **Gemma 4 12B is a credible, private, free daily driver for most writing,
summarizing, vision, and audio work** — keep Opus 4.8 for speed, the hardest
reasoning, and anything you'd ship without a second look. The gap is smaller than I
expected, and for sensitive material the local-first tradeoff is easy to make.
