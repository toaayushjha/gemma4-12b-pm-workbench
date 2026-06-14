"""Diagnostic: find the working way to pass audio to gemma4:12b on Ollama."""
import base64, json, subprocess, urllib.request

AUDIO = "inputs/audio/voice_memo.wav"
b64 = base64.b64encode(open(AUDIO, "rb").read()).decode()
KEYS = ["brightwave", "bright wave", "billing", "invoice", "priya", "roadmap", "memo", "monitor"]


def score(t: str) -> int:
    tl = (t or "").lower()
    return sum(k in tl for k in KEYS)


def post(url, payload, timeout=300):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout).read().decode()


results = []

# 1) OpenAI-compatible /v1 input_audio
try:
    p = {"model": "gemma4:12b", "stream": False, "messages": [{"role": "user", "content": [
        {"type": "text", "text": "Transcribe this audio word for word."},
        {"type": "input_audio", "input_audio": {"data": b64, "format": "wav"}}]}]}
    c = json.loads(post("http://localhost:11434/v1/chat/completions", p))["choices"][0]["message"]["content"]
    results.append(("v1 input_audio", score(c), c[:500]))
except Exception as e:
    results.append(("v1 input_audio", -1, str(e)[:250]))

# 2) native /api/chat with audio: [ {data, format} ]
try:
    p = {"model": "gemma4:12b", "stream": False, "messages": [
        {"role": "user", "content": "Transcribe this audio word for word.",
         "audio": [{"data": b64, "format": "wav"}]}]}
    c = json.loads(post("http://localhost:11434/api/chat", p))["message"]["content"]
    results.append(("api/chat audio[dict]", score(c), c[:500]))
except Exception as e:
    results.append(("api/chat audio[dict]", -1, str(e)[:250]))

# 3) native /api/chat with audios: [b64]
try:
    p = {"model": "gemma4:12b", "stream": False, "messages": [
        {"role": "user", "content": "Transcribe this audio word for word.", "audios": [b64]}]}
    c = json.loads(post("http://localhost:11434/api/chat", p))["message"]["content"]
    results.append(("api/chat audios[b64]", score(c), c[:500]))
except Exception as e:
    results.append(("api/chat audios[b64]", -1, str(e)[:250]))

# 4) CLI path-detection (the reference behavior)
try:
    out = subprocess.run(["ollama", "run", "gemma4:12b",
                          f"Transcribe the speech in {AUDIO} word for word."],
                         capture_output=True, text=True, timeout=300)
    results.append(("CLI path", score(out.stdout), (out.stdout or out.stderr)[:500]))
except Exception as e:
    results.append(("CLI path", -1, str(e)[:250]))

print("\n========== AUDIO PROBE RESULTS ==========")
for name, sc, sample in results:
    verdict = "✅ WORKS" if sc and sc > 0 else ("⚠️ ignored/empty" if sc == 0 else "❌ error")
    print(f"\n### {name}  ->  {verdict} (keyword score={sc})")
    print(sample)
print("\n========== END ==========")
