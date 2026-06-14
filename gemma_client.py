"""
gemma_client.py — a tiny, local-only client for evaluating Gemma 4 12B.

Design goals (PM-friendly, fully local, no paid services):
  * Talk to Ollama on http://localhost:11434 using ONLY the Python standard
    library, so the core has zero pip dependencies.
  * One shared code path for the Gradio workbench (app.py) and the batch
    runner (run_eval.py), including a single JSONL run-log with latency +
    token stats for honest, reproducible results.

Modality support:
  * text                 -> Ollama  (solid)
  * text + image(s)      -> Ollama  (solid; Gemma 4 is natively multimodal)
  * text + audio         -> see analyze_audio(): tries Ollama first, then a
                            clearly-labelled fallback. Finalised after the
                            Phase A runtime test (the model shipped 2026-06-03,
                            so local audio plumbing is brand new).
  * video                -> handled in run_eval.py as frames@1FPS (+ audio),
                            because Gemma treats "video" as image frames + the
                            audio track (no separate video input).

Env overrides: OLLAMA_URL, GEMMA_MODEL.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import pathlib
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("GEMMA_MODEL", "gemma4:12b")

ROOT = pathlib.Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)
LOG_PATH = RESULTS_DIR / "run_log.jsonl"


# --------------------------------------------------------------------------- #
# low-level helpers
# --------------------------------------------------------------------------- #
def _b64_file(path: str | pathlib.Path) -> str:
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("utf-8")


def _post(path: str, payload: dict, timeout: int = 900):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _post_json(path: str, payload: dict, timeout: int = 900) -> dict:
    return json.loads(_post(path, payload, timeout).decode("utf-8"))


def _tok_per_s(resp: dict):
    n, dur = resp.get("eval_count"), resp.get("eval_duration")
    return round(n / (dur / 1e9), 1) if (n and dur) else None


def _log(record: dict) -> dict:
    with open(LOG_PATH, "a") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def _v1_multimodal(
    prompt: str,
    *,
    image_paths: list[str] | None = None,
    audio_path: str | None = None,
    model: str = DEFAULT_MODEL,
    system: str | None = None,
    temperature: float = 0.7,
    timeout: int = 1200,
) -> dict:
    """Text + image(s) + optional audio via Ollama's OpenAI-compatible /v1
    endpoint. This is the format Gemma 4 audio (and video=frames+audio) require;
    plain images also work here. Confirmed empirically (see results/audio_probe).
    """
    content: list[dict] = [{"type": "text", "text": prompt}]
    for ip in image_paths or []:
        mime = mimetypes.guess_type(ip)[0] or "image/jpeg"
        content.append({"type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{_b64_file(ip)}"}})
    if audio_path:
        fmt = pathlib.Path(audio_path).suffix.lstrip(".").lower() or "wav"
        content.append({"type": "input_audio",
                        "input_audio": {"data": _b64_file(audio_path), "format": fmt}})
    messages = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": content}]
    payload = {"model": model, "messages": messages, "stream": False,
               "temperature": temperature}
    t0 = time.time()
    resp = _post_json("/v1/chat/completions", payload, timeout=timeout)
    dt = round(time.time() - t0, 2)
    usage = resp.get("usage", {})
    out_tok = usage.get("completion_tokens")
    return {
        "response": resp["choices"][0]["message"]["content"],
        "latency_s": dt,
        "output_tokens": out_tok,
        "prompt_tokens": usage.get("prompt_tokens"),
        "tokens_per_s": round(out_tok / dt, 1) if (out_tok and dt) else None,
    }


# --------------------------------------------------------------------------- #
# health / introspection
# --------------------------------------------------------------------------- #
def list_models() -> list[str]:
    """Names of models pulled into the local Ollama instance."""
    try:
        with urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=5) as r:
            return [m["name"] for m in json.loads(r.read()).get("models", [])]
    except Exception as exc:  # noqa: BLE001
        return [f"<ollama unreachable: {exc}>"]


def is_ready(model: str = DEFAULT_MODEL) -> bool:
    return any(model.split(":")[0] in m for m in list_models())


# --------------------------------------------------------------------------- #
# core generation (text and text+image)
# --------------------------------------------------------------------------- #
def generate(
    prompt: str,
    images: list[str] | None = None,
    *,
    model: str = DEFAULT_MODEL,
    system: str | None = None,
    think: bool | None = None,
    temperature: float = 0.7,
    num_ctx: int | None = None,
    task_id: str | None = None,
    category: str | None = None,
    log: bool = True,
) -> dict:
    """Run one non-streaming completion and return a record dict.

    `images` is a list of local file paths. `think` toggles Gemma 4 Thinking
    Mode (True / False / None=runtime default). Returns:
      {task_id, category, model, modality, think, latency_s, output_tokens,
       tokens_per_s, response, prompt_tokens}
    """
    user_msg: dict = {"role": "user", "content": prompt}
    if images:
        user_msg["images"] = [_b64_file(p) for p in images]

    messages = ([{"role": "system", "content": system}] if system else []) + [user_msg]
    payload: dict = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if num_ctx:
        payload["options"]["num_ctx"] = num_ctx
    if think is not None:
        payload["think"] = think  # Ollama ignores unknown keys on older builds

    t0 = time.time()
    try:
        resp = _post_json("/api/chat", payload)
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_URL}. Is it running? "
            f"Try `ollama serve` or open the Ollama app. ({exc})"
        ) from exc
    dt = round(time.time() - t0, 2)

    record = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_id": task_id,
        "category": category,
        "model": model,
        "modality": "image+text" if images else "text",
        "think": think,
        "latency_s": dt,
        "prompt_tokens": resp.get("prompt_eval_count"),
        "output_tokens": resp.get("eval_count"),
        "tokens_per_s": _tok_per_s(resp),
        "response": resp.get("message", {}).get("content", ""),
    }
    return _log(record) if log else record


def generate_stream(
    prompt: str,
    images: list[str] | None = None,
    *,
    model: str = DEFAULT_MODEL,
    system: str | None = None,
    think: bool | None = None,
    temperature: float = 0.7,
):
    """Yield response text incrementally (used by the Gradio UI)."""
    user_msg: dict = {"role": "user", "content": prompt}
    if images:
        user_msg["images"] = [_b64_file(p) for p in images]
    messages = ([{"role": "system", "content": system}] if system else []) + [user_msg]
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {"temperature": temperature},
    }
    if think is not None:
        payload["think"] = think

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL + "/api/chat", data=data, headers={"Content-Type": "application/json"}
    )
    acc = ""
    with urllib.request.urlopen(req, timeout=900) as resp:
        for line in resp:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            acc += obj.get("message", {}).get("content", "")
            yield acc
            if obj.get("done"):
                break


# --------------------------------------------------------------------------- #
# audio + video (native, via the /v1 input_audio path — confirmed in Phase A)
# --------------------------------------------------------------------------- #
def analyze_audio(
    prompt: str,
    audio_path: str,
    *,
    model: str = DEFAULT_MODEL,
    task_id: str | None = None,
    category: str | None = "06_audio",
    log: bool = True,
) -> dict:
    """Native speech understanding via Gemma 4 12B (Ollama /v1 input_audio)."""
    r = _v1_multimodal(prompt, audio_path=audio_path, model=model)
    record = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_id": task_id, "category": category, "model": model,
        "modality": "audio+text",
        "audio_backend": "ollama /v1 input_audio (native)",
        "latency_s": r["latency_s"], "output_tokens": r["output_tokens"],
        "tokens_per_s": r["tokens_per_s"], "response": r["response"],
    }
    return _log(record) if log else record


def analyze_video(
    prompt: str,
    video_path: str,
    *,
    model: str = DEFAULT_MODEL,
    fps: int = 1,
    max_frames: int = 12,
    with_audio: bool = True,
    task_id: str | None = None,
    category: str | None = "07_video",
    log: bool = True,
) -> dict:
    """Video understanding = frames sampled @fps (as images) + the audio track.

    Gemma 4 has no separate 'video' input; this mirrors how Google demos it
    (frames @1FPS + audio). Frames + audio are sent together via /v1.
    """
    with tempfile.TemporaryDirectory() as td:
        tdp = pathlib.Path(td)
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path), "-vf", f"fps={fps}",
             "-frames:v", str(max_frames), "-loglevel", "error",
             str(tdp / "f_%03d.jpg")], check=True)
        frames = sorted(str(p) for p in tdp.glob("f_*.jpg"))
        audio = None
        if with_audio:
            cand = tdp / "a.wav"
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-i", str(video_path), "-vn", "-ar", "16000",
                     "-ac", "1", "-loglevel", "error", str(cand)], check=True)
                audio = str(cand) if cand.exists() and cand.stat().st_size > 0 else None
            except subprocess.CalledProcessError:
                audio = None
        full = (prompt + f"\n\n(You are given {len(frames)} frames sampled at {fps} "
                f"fps from a short recording" + (", plus its audio track." if audio
                else ".") + ")")
        r = _v1_multimodal(full, image_paths=frames, audio_path=audio, model=model)
    record = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_id": task_id, "category": category, "model": model,
        "modality": f"video({len(frames)}f{'+audio' if audio else ''})",
        "latency_s": r["latency_s"], "output_tokens": r["output_tokens"],
        "tokens_per_s": r["tokens_per_s"], "response": r["response"],
    }
    return _log(record) if log else record


# --------------------------------------------------------------------------- #
# CLI smoke test:  python gemma_client.py "your prompt"
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import sys

    print("Local models:", list_models())
    q = sys.argv[1] if len(sys.argv) > 1 else "In one sentence, what are you?"
    out = generate(q, log=False)
    print(f"\n[{out['latency_s']}s | {out['tokens_per_s']} tok/s | "
          f"{out['output_tokens']} tok]\n{out['response']}")
