#!/usr/bin/env python3
"""
make_inputs.py — generate ALL synthetic media inputs for the eval, locally.

Images  -> matplotlib + Pillow
Audio   -> macOS `say` (TTS) + ffmpeg (to 16 kHz mono wav, Gemma 4's audio rate)
Video   -> Pillow slides + ffmpeg (slideshow + narration = a "screen demo")

Everything here is fabricated, so the resulting repo is safe to publish.
Run once after `uv pip install -r requirements.txt`:  python make_inputs.py
"""
from __future__ import annotations

import pathlib
import subprocess
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
IMG = ROOT / "inputs" / "images"
AUD = ROOT / "inputs" / "audio"
VID = ROOT / "inputs" / "video"
for d in (IMG, AUD, VID):
    d.mkdir(parents=True, exist_ok=True)

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
]


def font(size: int):
    for fp in FONT_CANDIDATES:
        if pathlib.Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:  # noqa: BLE001
                pass
    return ImageFont.load_default()


# --------------------------------------------------------------------------- #
# Images
# --------------------------------------------------------------------------- #
def make_dashboard():
    kpis = [
        ("MRR", "$128.4K", "+6.2%", "good"),
        ("Active Users", "4,820", "+3.1%", "good"),
        ("Activation Rate", "41%", "-2.0%", "bad"),
        ("Churn (monthly)", "3.8%", "+0.5%", "bad"),
        ("NPS", "47", "+4", "good"),
        ("Trial→Paid", "7.9%", "+0.3%", "good"),
    ]
    fig = plt.figure(figsize=(11, 6.5), dpi=120)
    fig.suptitle("Acme Cloud — Product Metrics (May 2026)",
                 fontsize=20, fontweight="bold", x=0.07, ha="left")
    for i, (name, val, delta, kind) in enumerate(kpis):
        ax = fig.add_axes([0.07 + (i % 3) * 0.31, 0.55 - (i // 3) * 0.24, 0.27, 0.18])
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor="#f4f6f8",
                                   edgecolor="#d0d7de", lw=1.2))
        ax.text(0.06, 0.72, name, fontsize=12, color="#57606a")
        ax.text(0.06, 0.34, val, fontsize=26, fontweight="bold", color="#1f2328")
        ax.text(0.96, 0.40, delta, fontsize=14, ha="right",
                color="#1a7f37" if kind == "good" else "#cf222e")
    ax = fig.add_axes([0.07, 0.07, 0.86, 0.18])
    weeks = ["Wk 1", "Wk 2", "Wk 3", "Wk 4"]
    signups = [210, 245, 198, 312]
    ax.bar(weeks, signups, color="#0969da")
    for x, y in zip(weeks, signups):
        ax.text(x, y + 5, str(y), ha="center", fontsize=10)
    ax.set_title("New Signups by Week", fontsize=12, loc="left")
    ax.set_ylim(0, 360)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(IMG / "dashboard.png", facecolor="white")
    plt.close(fig)
    print("✓ images/dashboard.png")


def make_chart():
    cats = ["Starter", "Pro", "Enterprise", "Add-ons"]
    vals = [5800, 9800, 7500, 1700]
    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    bars = ax.bar(cats, vals, color=["#54aeff", "#0969da", "#0a3069", "#8250df"])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 120, f"${v:,}",
                ha="center", fontsize=11, fontweight="bold")
    ax.set_title("Revenue by Product — May 2026", fontsize=15, fontweight="bold")
    ax.set_ylabel("Revenue (USD)")
    ax.set_ylim(0, 11000)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / "chart.png", facecolor="white")
    plt.close(fig)
    print("✓ images/chart.png")


def make_scanned_memo():
    text = (
        "MEMO\n\n"
        "TO:    All Product Managers\n"
        "FROM:  Maya Chen, Head of Product\n"
        "DATE:  June 12, 2026\n"
        "RE:    Q3 Roadmap Submissions\n\n"
        "Please submit your Q3 roadmap one-pagers by\n"
        "Friday, June 20.\n\n"
        "Each one-pager should include:\n"
        "  - Your top 3 objectives for the quarter\n"
        "  - The key metric you will move\n"
        "  - Any cross-team dependencies\n\n"
        "Late submissions will not be included in the\n"
        "planning review. Thank you.\n"
    )
    W, H = 900, 1150
    img = Image.new("RGB", (W, H), (243, 240, 232))
    d = ImageDraw.Draw(img)
    d.multiline_text((90, 90), text, fill=(30, 28, 26), font=font(30), spacing=12)
    img = img.rotate(-1.4, expand=False, fillcolor=(243, 240, 232))
    # light scan speckle
    import random
    random.seed(7)
    px = img.load()
    for _ in range(2600):
        x, y = random.randint(0, W - 1), random.randint(0, H - 1)
        px[x, y] = (200, 198, 190)
    img.save(IMG / "scanned_memo.png")
    print("✓ images/scanned_memo.png")


def make_ui_mock():
    W, H = 380, 760
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 28], fill=(245, 245, 247))
    d.text((12, 6), "9:41", fill=(0, 0, 0), font=font(14))
    d.rectangle([0, 28, W, 92], fill=(0, 122, 255))
    d.text((20, 48), "Settings", fill=(255, 255, 255), font=font(26))
    d.text((W - 34, 40), "x", fill=(255, 255, 255), font=font(16))  # tiny close target
    rows = ["Account", "Notifications", "Privacy", "Billing", "Help & Support"]
    y = 110
    for r in rows:
        d.text((22, y), r, fill=(20, 20, 20), font=font(20))
        d.line([16, y + 38, W - 16, y + 38], fill=(235, 235, 235))
        y += 56
    # low-contrast destructive action + cramped primary button
    d.text((22, y + 16), "Delete account", fill=(225, 225, 225), font=font(18))
    d.rectangle([110, H - 70, 270, H - 40], fill=(0, 122, 255))
    d.text((150, H - 66), "Save", fill=(255, 255, 255), font=font(16))
    img.save(IMG / "ui_mock.png")
    print("✓ images/ui_mock.png")


# --------------------------------------------------------------------------- #
# Audio (macOS `say` -> 16 kHz mono wav)
# --------------------------------------------------------------------------- #
def _say_to_wav(text: str, out_wav: pathlib.Path, voice: str | None):
    with tempfile.TemporaryDirectory() as td:
        aiff = pathlib.Path(td) / "tts.aiff"
        cmd = ["say"] + (["-v", voice] if voice else []) + ["-o", str(aiff), text]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:  # voice missing -> default voice
            subprocess.run(["say", "-o", str(aiff), text], check=True)
        subprocess.run(["ffmpeg", "-y", "-i", str(aiff), "-ar", "16000",
                        "-ac", "1", "-loglevel", "error", str(out_wav)], check=True)


def make_audio():
    memo = ("Hey team, quick voice memo after the BrightWave call. They're happy "
            "with the billing fix, but they want CSV export for invoices by the end "
            "of the month. Priya, can you scope that this week? Also, let's add "
            "invoice page latency to our monitoring so we catch this earlier next "
            "time. I'll update the roadmap doc. Thanks.")
    _say_to_wav(memo, AUD / "voice_memo.wav", "Alex")
    print("✓ audio/voice_memo.wav")

    a = "Should we ship the free trial without requiring a credit card?"
    b = ("Yes, no credit card. It lifts sign-ups a lot. But we should add upgrade "
         "nudges on day seven and day twelve to protect conversion.")
    a2 = "Agreed. Decision: a fourteen day trial, no card, with those two nudges."
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td)
        _say_to_wav(a, p / "a1.wav", "Alex")
        _say_to_wav(b, p / "b1.wav", "Samantha")
        _say_to_wav(a2, p / "a2.wav", "Alex")
        concat = p / "list.txt"
        concat.write_text("".join(f"file '{p / f}'\n" for f in
                                  ["a1.wav", "b1.wav", "a2.wav"]))
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i",
                        str(concat), "-ar", "16000", "-ac", "1", "-loglevel",
                        "error", str(AUD / "two_speaker.wav")], check=True)
    print("✓ audio/two_speaker.wav")


# --------------------------------------------------------------------------- #
# Video (slides + narration -> mp4)
# --------------------------------------------------------------------------- #
def _slide(text_lines, path: pathlib.Path, accent=(9, 105, 218)):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=accent)
    y = 240
    for i, line in enumerate(text_lines):
        f = font(64 if i == 0 else 40)
        col = (31, 35, 40) if i == 0 else (87, 96, 106)
        d.text((100, y), line, fill=col, font=f)
        y += 90 if i == 0 else 64
    img.save(path)


def make_video():
    slides = [
        ["Acme Cloud", "Product Demo — May 2026"],
        ["1. Dashboard", "See your KPIs at a glance"],
        ["2. Create Automation", "Start from a template"],
        ["3. Invite Your Team", "Collaborate in a shared workspace"],
        ["4. Upgrade In-Product", "Self-serve checkout with Stripe"],
    ]
    narration = ("Welcome to Acme Cloud. First, the dashboard shows your key metrics "
                 "at a glance. Next, create an automation from a template. Then invite "
                 "your team to collaborate. Finally, upgrade in product when you're "
                 "ready, with self serve checkout.")
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td)
        for i, s in enumerate(slides):
            _slide(s, p / f"s{i:02d}.png")
        narr = p / "narr.wav"
        _say_to_wav(narration, narr, "Samantha")
        # 2.5s per slide
        listfile = p / "frames.txt"
        listfile.write_text("".join(
            f"file '{p / f's{i:02d}.png'}'\nduration 2.5\n" for i in range(len(slides))
        ) + f"file '{p / f's{len(slides)-1:02d}.png'}'\n")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
            "-i", str(narr), "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", "-r", "25", "-loglevel", "error",
            str(VID / "demo.mp4")], check=True)
    print("✓ video/demo.mp4")


if __name__ == "__main__":
    for fn in (make_dashboard, make_chart, make_scanned_memo, make_ui_mock,
               make_audio, make_video):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            print(f"✗ {fn.__name__}: {exc}")
    print("\nDone. Inputs in inputs/{images,audio,video}/")
