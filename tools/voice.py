#!/usr/bin/env python3
"""Stage 8 voiceover: video/plan.json -> video/audio/sNN.wav + sNN.words.json, then video/captions.srt.

Run with the TTS venv:  .venv-tts/bin/python tools/voice.py <run> --engine kokoro [--voice am_michael] [--scenes 1,3]
Engines: kokoro (local), windows (Windows TTS via powershell.exe, WSL only).
Narration text comes from plan.json unchanged; words.json "lines" must equal it (kit.py check-render).
"""
import argparse
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
SR = 24000
LEAD, GAP, TAIL = 0.30, 0.35, 0.60  # seconds of silence: scene start, between lines, scene end
CUE_WORDS = 8  # caption chunk size


def resolve_run(arg):
    p = Path(arg)
    return p if (p / "run.json").is_file() else ROOT / "runs" / arg


# ---------- engines: text -> (float32 audio at SR, [{"w", "s", "e"}] relative to that audio) ----------

class Kokoro:
    def __init__(self, voice):
        from kokoro import KPipeline
        self.pipe, self.voice = KPipeline(lang_code="a"), voice  # American English

    def say(self, text):
        audio, words, offset = [], [], 0.0
        for r in self.pipe(text, voice=self.voice):
            for tok in r.tokens or []:
                if tok.start_ts is not None and any(c.isalnum() for c in tok.text):
                    words.append({"w": tok.text, "s": offset + tok.start_ts, "e": offset + tok.end_ts})
            a = r.audio.numpy().astype(np.float32)
            audio.append(a)
            offset += len(a) / SR
        return np.concatenate(audio), words


class Windows:
    def __init__(self, voice):
        self.voice = voice
        temp = subprocess.run(["cmd.exe", "/c", "echo %TEMP%"], capture_output=True, text=True,
                              cwd="/mnt/c").stdout.strip()
        self.dir = Path(subprocess.run(["wslpath", temp], capture_output=True, text=True).stdout.strip()) / "eo-tts"
        self.dir.mkdir(exist_ok=True)
        (self.dir / "wintts.ps1").write_bytes((ROOT / "tools" / "wintts.ps1").read_bytes())
        self.win = subprocess.run(["wslpath", "-w", str(self.dir)], capture_output=True, text=True).stdout.strip()

    def say(self, text):
        (self.dir / "line.txt").write_text(text, encoding="utf-8")
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", rf"{self.win}\wintts.ps1",
             rf"{self.win}\line.txt", rf"{self.win}\line.wav", self.voice],
            capture_output=True, text=True, check=True).stdout
        audio, sr = sf.read(self.dir / "line.wav", dtype="float32")
        assert sr == SR, f"Windows TTS wrote {sr} Hz, expected {SR}"
        starts = [json.loads(l) for l in out.splitlines() if l.startswith("{")]
        end = len(audio) / SR
        return audio, [{"w": w["w"], "s": w["ms"] / 1000, "e": (starts[i + 1]["ms"] / 1000 if i + 1 < len(starts) else end)}
                       for i, w in enumerate(starts)]


ENGINES = {"kokoro": (Kokoro, "am_michael"), "windows": (Windows, "Microsoft David Desktop")}


# ---------- scenes + captions ----------

def scene_lines(scene):
    return [b["text"] for b in scene["beats"] if b["kind"] == "line"]


def voice_scene(engine, lines):
    """Return (audio, words) for one scene: lead silence, lines with gaps, tail silence."""
    silence = lambda sec: np.zeros(int(sec * SR), dtype=np.float32)
    parts, words, t = [silence(LEAD)], [], LEAD
    for i, line in enumerate(lines):
        audio, ws = engine.say(line)
        words += [{"w": w["w"], "s": round(t + w["s"], 3), "e": round(t + w["e"], 3), "line": i} for w in ws]
        parts += [audio, silence(GAP if i + 1 < len(lines) else TAIL)]
        t += len(audio) / SR + (GAP if i + 1 < len(lines) else TAIL)
    return np.concatenate(parts), words


def srt_time(sec):
    ms = round(sec * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def line_cues(text, words, offset):
    """Split one line into CUE_WORDS-word captions, timed from that line's words by position."""
    tokens = text.split()
    if not words:
        return []
    cues = []
    size = math.ceil(len(tokens) / math.ceil(len(tokens) / CUE_WORDS))  # equal chunks, no one-word orphan
    for a in range(0, len(tokens), size):
        b = min(a + size, len(tokens))
        first = words[min(len(words) - 1, a * len(words) // len(tokens))]
        last = words[min(len(words) - 1, math.ceil(b * len(words) / len(tokens)) - 1)]
        cues.append((offset + first["s"], offset + last["e"], " ".join(tokens[a:b])))
    return cues


def write_srt(audio_dir, scenes, out):
    cues, offset = [], 0.0
    for sc in scenes:
        n = f"s{sc['n']:02d}"
        data = json.loads((audio_dir / f"{n}.words.json").read_text(encoding="utf-8"))
        for i, line in enumerate(data["lines"]):
            cues += line_cues(line, [w for w in data["words"] if w["line"] == i], offset)
        offset += sf.info(audio_dir / f"{n}.wav").duration  # scenes play back to back
    out.write_text("".join(f"{k}\n{srt_time(s)} --> {srt_time(e)}\n{t}\n\n" for k, (s, e, t) in enumerate(cues, 1)),
                   encoding="utf-8")
    return len(cues), offset


def self_test():
    assert srt_time(3725.5) == "01:02:05,500" and srt_time(0.0004) == "00:00:00,000"
    ws = [{"w": str(i), "s": i, "e": i + 0.5} for i in range(10)]
    cues = line_cues(" ".join("abcdefghij"), ws, 100)
    assert [(c[0], c[1]) for c in cues] == [(100, 104.5), (105, 109.5)], cues
    assert cues[1][2] == "f g h i j"
    two = line_cues("one two three four", ws[:2], 0)  # fewer timed words than tokens: proportional
    assert two == [(0, 1.5, "one two three four")], two
    assert line_cues("no timings", [], 0) == []
    print("voice.py self-test passed")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("run", nargs="?")
    p.add_argument("--engine", choices=sorted(ENGINES), default="kokoro")
    p.add_argument("--voice")
    p.add_argument("--scenes", help="comma-separated scene numbers (default: all)")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        return self_test()
    if not a.run:
        p.error("run is required")
    video = resolve_run(a.run) / "video"
    plan = json.loads((video / "plan.json").read_text(encoding="utf-8"))  # missing = run `kit.py export` first
    cls, default_voice = ENGINES[a.engine]
    voice = a.voice or default_voice
    engine = cls(voice)
    wanted = {int(x) for x in a.scenes.split(",")} if a.scenes else None
    (video / "audio").mkdir(exist_ok=True)
    for sc in plan["scenes"]:
        if wanted and sc["n"] not in wanted:
            continue
        lines = scene_lines(sc)
        audio, words = voice_scene(engine, lines)
        n = f"s{sc['n']:02d}"
        sf.write(video / "audio" / f"{n}.wav", audio, SR, subtype="PCM_16")
        (video / "audio" / f"{n}.words.json").write_text(json.dumps(
            {"engine": a.engine, "voice": voice, "lines": lines, "words": words}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"{n}: {len(audio) / SR:.1f}s, {len(lines)} lines, {len(words)} timed words")
    if all((video / "audio" / f"s{sc['n']:02d}.words.json").is_file() for sc in plan["scenes"]):
        count, total = write_srt(video / "audio", plan["scenes"], video / "captions.srt")
        print(f"captions.srt: {count} cues, voiceover total {total / 60:.1f} min")


if __name__ == "__main__":
    sys.exit(main())
