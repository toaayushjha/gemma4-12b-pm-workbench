# Screenshot checklist (for the blog + Pages site)

Capture these into `results/screenshots/` (suggested filenames in `code`). Keep them
clean — light theme, no personal/company data visible (everything here is synthetic).

## Setup / "it's really local"
- [ ] `01_ollama_pull.png` — terminal showing `ollama pull gemma4:12b` completing (7.6 GB).
- [ ] `02_ollama_show.png` — `ollama show gemma4:12b` showing **Capabilities: vision, audio**.
- [ ] `03_offline.png` — (optional, great visual) Wi-Fi turned OFF + a working chat reply,
      to prove it runs with no network.
- [ ] `04_activity_monitor.png` — Activity Monitor / `asitop` showing GPU + RAM while
      generating (proves it's using local silicon, not the cloud).

## The workbench (`app.py`)
- [ ] `05_workbench_chat.png` — the Chat tab with a reply + the latency/tok-s readout.
- [ ] `06_workbench_vision.png` — drag the `dashboard.png` in and ask for KPIs; show the answer.
- [ ] `07_workbench_audio.png` — the Audio tab with a transcript + summary.
- [ ] `08_workbench_benchmark.png` — the Benchmark tab dropdown + an output.

## LM Studio (the no-code GUI)
- [ ] `09_lmstudio_model.png` — LM Studio with Gemma 4 12B loaded (model card visible).
- [ ] `10_lmstudio_image.png` — an image prompt answered in LM Studio.

## Results / "the receipts"
- [ ] `11_results_table.png` — `results/results.md` rendered (the per-task table).
- [ ] `12_speed_chart.png` — the latency/tokens-per-sec chart from the Pages site.
- [ ] `13_verdict_map.png` — the "where local wins vs. where Opus wins" map.

## Head-to-head
- [ ] `14_gemma_vs_opus.png` — a side-by-side of one hero prompt (Gemma left, Opus right).

## Hero capability shots (the "wow")
- [ ] `15_audio_diarization.png` — the 2-speaker diarized transcript.
- [ ] `16_video_summary.png` — the demo-video summary (frames + audio).
- [ ] `17_ocr_memo.png` — the scanned-memo OCR result next to the source image.

> Tip: on macOS, `Cmd-Shift-5` → "Capture Selected Portion" for tight crops. For the
> side-by-side, take two shots and stitch, or use the Pages site's comparison section.
