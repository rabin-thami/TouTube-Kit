#!/usr/bin/env python3
"""Stage 8 step 4: animatic = one still frame per shot from video/shots.md, timed to the voice.

Run:  python3 tools/animatic.py <run>
Writes video/animatic/frames/<shot>.png, video/animatic/sheet.png (contact sheet), video/animatic.mp4.
A shot starts at the first word of its first line (the scene's first shot at 0) and ends where the
next shot starts; the last shot runs to the end of the scene's wav. Needs Pillow and ffmpeg.
"""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kit  # noqa: E402  (shots.md parser and run helpers)

W, H = 1920, 1080
PAPER, INK, SOFT, YELLOW, RED = "#F6F5EA", "#201E18", "#393733", "#F0E136", "#7D3130"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wav_seconds(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def timed_shots(run):
    """{scene: (wav seconds, [(row, start, end)])}, times in seconds from the scene start."""
    errors, _ = kit.check_shots(run)
    if errors:
        sys.exit("shots.md does not pass `kit.py shots`; fix it first")
    rows, _ = kit.parse_table((run / "video/shots.md").read_text(encoding="utf-8"), kit.SHOT_HEADER, "shots.md")
    by_scene = {}
    for r in rows:
        by_scene.setdefault(int(r["scene"]), []).append(r)
    out = {}
    for n, shots in sorted(by_scene.items()):
        audio = run / "video/audio" / f"s{n:02d}"
        words = json.loads(audio.with_suffix(".words.json").read_text(encoding="utf-8"))["words"]
        total = wav_seconds(audio.with_suffix(".wav"))
        starts = []
        for i, r in enumerate(shots):
            # shortcut: hold shots (lines "-") are not timed yet; add when a shot list uses them
            if r["lines"] == "-":
                sys.exit(f"{r['shot']}: hold shots (lines '-') are not supported by the animatic yet")
            k = int(r["lines"].split("-")[0]) - 1  # 0-based line index
            starts.append(0.0 if i == 0 else next(w["s"] for w in words if w["line"] == k))
        ends = starts[1:] + [total]
        out[n] = (total, list(zip(shots, starts, ends)))
    return out


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def frame(run, r, start, end):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((60, 40), f"{r['shot']}  {r['type']}  {end - start:4.1f} s  lines {r['lines']}", font=font(SANS, 30), fill=RED)
    d.text((W - 60, 40), f"-> {r['transition']}", font=font(SANS, 30), fill=RED, anchor="ra")
    files = [] if r["assets"] in ("", "-") else [a.strip() for a in r["assets"].split(",")]
    box_top, box_h = 110, 640
    if files:
        slot = (W - 120) // len(files)
        for i, f in enumerate(files):
            im = Image.open(run / "assets" / f).convert("RGB")
            if r["type"].upper() in ("ARCHIVAL", "DETAIL") and "colour" not in r["visual"].lower():
                im = ImageOps.grayscale(im).convert("RGB")  # family B: black-and-white grade
            im.thumbnail((slot - 40, box_h))
            x = 60 + i * slot + (slot - im.width) // 2
            y = box_top + (box_h - im.height) // 2
            d.rectangle((x - 6, y - 6, x + im.width + 5, y + im.height + 5), fill="white", outline=INK, width=2)
            img.paste(im, (x, y))
    else:  # pure graphic: describe it in the frame
        d.rectangle((60, box_top, W - 60, box_top + box_h), outline=SOFT, width=3)
        d.text((90, box_top + 25), "GRAPHIC", font=font(SANS, 28), fill=SOFT)
        y = box_top + 80
        for ln in wrap(d, r["visual"], font(FONT, 40), W - 180)[:11]:
            d.text((90, y), ln, font=font(FONT, 40), fill=INK)
            y += 52
    y = box_top + box_h + 25
    if r["text"] not in ("", "-"):  # on-screen text, highlighted like a type-on label
        f = font(BOLD, 46)
        for ln in wrap(d, r["text"], f, W - 160)[:2]:
            x1 = 60 + d.textlength(ln, font=f)
            d.rectangle((52, y - 4, x1 + 8, y + 56), fill=YELLOW)
            d.text((60, y), ln, font=f, fill=INK)
            y += 66
    f = font(SANS, 26)
    for label, val in (("Takeaway", r["takeaway"]), ("Camera", r["camera"]), ("Sound", r["sound"])):
        for ln in wrap(d, f"{label}: {val}", f, W - 120)[:2]:
            if y > H - 40:
                break
            d.text((60, y), ln, font=f, fill=SOFT)
            y += 32
    return img


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    run = kit.resolve_run(sys.argv[1])
    out = run / "video/animatic"
    (out / "frames").mkdir(parents=True, exist_ok=True)
    scenes = timed_shots(run)
    concat, thumbs, wavs = [], [], []
    for n, (total, shots) in scenes.items():
        wavs.append(run / "video/audio" / f"s{n:02d}.wav")
        for r, s, e in shots:
            assert e > s, f"{r['shot']} has no screen time"
            p = out / "frames" / f"{r['shot']}.png"
            im = frame(run, r, s, e)
            im.save(p)
            thumbs.append(im.resize((384, 216)))
            concat += [f"file '{p.resolve()}'", f"duration {e - s:.3f}"]
    concat.append(concat[-2])  # concat demuxer: repeat the last file so its duration is honoured
    cols = 6
    sheet = Image.new("RGB", (cols * 384, -(-len(thumbs) // cols) * 216), PAPER)
    for i, t in enumerate(thumbs):
        sheet.paste(t, ((i % cols) * 384, (i // cols) * 216))
    sheet.save(out / "sheet.png")
    with tempfile.TemporaryDirectory() as tmp:
        lst, alst = Path(tmp, "frames.txt"), Path(tmp, "audio.txt")
        lst.write_text("\n".join(concat) + "\n")
        alst.write_text("".join(f"file '{w.resolve()}'\n" for w in wavs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                        "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-f", "concat", "-safe", "0", "-i", str(alst),
                        "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
                        "-c:a", "aac", "-b:a", "128k", "-shortest", str(run / "video/animatic.mp4")], check=True)
    n_shots = sum(len(s) for _, s in scenes.values())
    minutes = sum(t for t, _ in scenes.values()) / 60
    print(f"ANIMATIC: {n_shots} shots, {minutes:.1f} min -> video/animatic.mp4, video/animatic/sheet.png")


if __name__ == "__main__":
    main()
