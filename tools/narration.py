#!/usr/bin/env python3
"""Narration tools for steps 6 and 7 of the video pipeline.

  python3 tools/narration.py split    <run-folder>   script-final.md -> voiceover/chapters.json + chNN.txt
  python3 tools/narration.py tts      <run-folder> --provider elevenlabs|openrouter --voice <id> --model <id> [--format pcm]
                                                     chNN.txt -> chNN.mp3 (+ chNN.alignment.json from ElevenLabs)
  python3 tools/narration.py timeline <run-folder>   voiceover/* -> timeline.json
  python3 tools/narration.py selftest

Keys are read from ELEVENLABS_API_KEY or OPENROUTER_API_KEY environment variables only.
OpenRouter returns audio without timings, so its scene times are estimated (see time_at).
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

CHAPTER = re.compile(r'^###\s+Chapter\s+(\d+):\s*(.*?)\s*(?:\([^)]*\))?\s*$')
VISUAL = re.compile(r'^\[visual:\s*(.*?)\]\s*$')
TAG = re.compile(r'\s*\[[FQC]\d+(?:\s*,\s*[FQC]\d+)*\]')
PAUSE = '[pause]'
# shortcut: an ellipsis makes most voices pause; switch to the model's break tag if pauses sound too short
PAUSE_SPOKEN = '...'
MAX_CHARS = 5000  # stay under the per-request text limit; chapters are far shorter


def parse(md):
    """Narration markdown -> [{n, title, text, markers: [{offset, visual}]}]."""
    lines = md.splitlines()
    if '## Narration' in (l.strip() for l in lines):  # script.md: use only the Narration section
        lines = lines[[l.strip() for l in lines].index('## Narration') + 1:]
    chapters = []
    for raw in lines:
        line = raw.strip()
        if line.startswith('## '):
            break
        m = CHAPTER.match(line)
        if m:
            chapters.append({'n': int(m.group(1)), 'title': m.group(2), 'text': '', 'markers': []})
            continue
        if not line or not chapters:
            continue
        ch = chapters[-1]
        v = VISUAL.match(line)
        if v:
            ch['markers'].append({'offset': len(ch['text']), 'visual': v.group(1)})
            continue
        if '[visual:' in line:
            sys.exit(f'Visual note inside a narration line (put it on its own line): {line[:80]}')
        spoken = re.sub(r'\s+', ' ', TAG.sub('', line).replace(PAUSE, PAUSE_SPOKEN)).strip()
        if spoken:
            ch['text'] += (' ' if ch['text'] else '') + spoken
    if not chapters:
        sys.exit('No "### Chapter N: title" headings found.')
    return chapters


def split(run):
    src = run / 'script-final.md'
    if not src.exists():
        sys.exit(f'{src} not found. Write it at approval (AGENTS.md, Step 4).')
    chapters = parse(src.read_text(encoding='utf-8'))
    vo = run / 'voiceover'
    vo.mkdir(exist_ok=True)
    for ch in chapters:
        if len(ch['text']) > MAX_CHARS:
            sys.exit(f"Chapter {ch['n']} has {len(ch['text'])} characters; split it (limit {MAX_CHARS}).")
        (vo / f"ch{ch['n']:02d}.txt").write_text(ch['text'] + '\n', encoding='utf-8')
    (vo / 'chapters.json').write_text(json.dumps(chapters, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"{len(chapters)} chapters, {sum(len(c['markers']) for c in chapters)} visual notes -> {vo}")


PROVIDERS = {'elevenlabs': 'ELEVENLABS_API_KEY', 'openrouter': 'OPENROUTER_API_KEY'}


def pcm_params(content_type):
    """'audio/pcm;rate=44100;channels=1' -> (44100, 1). Rate differs by model, so never assume it."""
    params = dict(p.strip().split('=', 1) for p in content_type.split(';')[1:] if '=' in p)
    if 'rate' not in params:
        raise ValueError(f'pcm response has no sample rate in Content-Type: {content_type!r}')
    return int(params['rate']), int(params.get('channels', 1))


def pcm_to_mp3(pcm, rate, channels):
    """16-bit little-endian pcm -> mp3 bytes via ffmpeg."""
    out = subprocess.run(['ffmpeg', '-v', 'error', '-f', 's16le', '-ar', str(rate), '-ac', str(channels), '-i', 'pipe:0',
                          '-c:a', 'libmp3lame', '-b:a', '128k', '-f', 'mp3', 'pipe:1'],
                         input=pcm, capture_output=True)
    if out.returncode != 0:
        raise ValueError(f'ffmpeg could not convert pcm: {out.stderr[:300]!r}')
    return out.stdout


def request(provider, key, voice, model, text, fmt='mp3'):
    """One chapter -> (mp3 bytes, alignment or None)."""
    if provider == 'elevenlabs':
        req = urllib.request.Request(
            f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128',
            data=json.dumps({'text': text, 'model_id': model}).encode(),
            headers={'xi-api-key': key, 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
        return base64.b64decode(data['audio_base64']), data['alignment']
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/audio/speech',
        data=json.dumps({'model': model, 'input': text, 'voice': voice, 'response_format': fmt}).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        if not r.headers.get('Content-Type', '').startswith('audio/'):
            raise ValueError(f"expected audio, got {r.headers.get('Content-Type')}: {r.read(300)!r}")
        body = r.read()
        ctype = r.headers.get('Content-Type', '')
    return (pcm_to_mp3(body, *pcm_params(ctype)) if fmt == 'pcm' else body), None


def env_key(name):
    """Key from the environment, else from the project's git-ignored .env (NAME=value lines)."""
    if os.environ.get(name):
        return os.environ[name]
    env = Path(__file__).resolve().parent.parent / '.env'
    if env.exists():
        for line in env.read_text(encoding='utf-8').splitlines():
            k, sep, v = line.partition('=')
            if sep and k.strip() == name:
                return v.strip().strip('"\'') or None
    return None


def tts(run, provider, voice, model, fmt='mp3'):
    key = env_key(PROVIDERS[provider])
    if not key:
        sys.exit(f'Put {PROVIDERS[provider]}=... in the project .env file (git-ignored) or your environment.')
    vo = run / 'voiceover'
    chapters = json.loads((vo / 'chapters.json').read_text(encoding='utf-8'))
    for ch in chapters:
        stem = f"ch{ch['n']:02d}"
        mp3, align = vo / f'{stem}.mp3', vo / f'{stem}.alignment.json'
        if mp3.exists():
            print(f'{stem}: already done, skipped (delete {mp3.name} to redo; each call costs credits)')
            continue
        try:
            audio, alignment = request(provider, key, voice, model, ch['text'], fmt)
        except urllib.error.HTTPError as e:
            sys.exit(f"{stem}: {provider} error {e.code}: {e.read()[:500].decode(errors='replace')}")
        except (urllib.error.URLError, ValueError, KeyError) as e:
            sys.exit(f'{stem}: {provider} failed: {e}')
        if alignment is not None:  # write timings first, so a saved mp3 always has its timings
            align.write_text(json.dumps(alignment, ensure_ascii=False), encoding='utf-8')
        elif align.exists():
            align.unlink()  # stale timings from another voice would give wrong scene times
        mp3.write_bytes(audio)
        print(f'{stem}: {mp3.name} written' + ('' if alignment else ' (no word timings: scene times will be estimated)'))


def duration(mp3, alignment):
    try:
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                              '-of', 'csv=p=0', str(mp3)], capture_output=True, text=True, check=True)
        return float(out.stdout.strip())
    except (OSError, subprocess.CalledProcessError, ValueError):
        if alignment is None:
            sys.exit(f'Cannot read the length of {mp3}: install ffprobe (part of FFmpeg).')
        return alignment['character_end_times_seconds'][-1]


def time_at(text, alignment, offset, total):
    """Seconds when the first spoken character at or after `offset` starts."""
    # shortcut: with no timings (OpenRouter), place by character position; drift resets each chapter.
    # Upgrade: get word timings from a transcription model if scenes land visibly off the voice.
    if alignment is None or len(alignment['characters']) != len(text):
        return total * offset / max(len(text), 1)
    chars, starts = alignment['characters'], alignment['character_start_times_seconds']
    for i in range(offset, len(chars)):
        if not chars[i].isspace():
            return starts[i]
    return total


def build_timeline(chapters, alignments, durations):
    scenes, out_chapters, clock, n = [], [], 0.0, 0
    for ch, al, dur in zip(chapters, alignments, durations):
        marks = list(ch['markers'])
        if not marks or marks[0]['offset'] > 0:  # narration before the first note gets no planned visual
            marks.insert(0, {'offset': 0, 'visual': None})
        for i, mk in enumerate(marks):
            end_off = marks[i + 1]['offset'] if i + 1 < len(marks) else len(ch['text'])
            start = time_at(ch['text'], al, mk['offset'], dur)
            end = time_at(ch['text'], al, end_off, dur) if i + 1 < len(marks) else dur
            if mk['visual'] is not None:
                n += 1
            scenes.append({'scene': n if mk['visual'] is not None else None, 'chapter': ch['n'],
                           'start': round(clock + start, 3), 'end': round(clock + end, 3),
                           'visual': mk['visual'], 'narration': ch['text'][mk['offset']:end_off].strip()})
        if scenes and scenes[-len(marks)]['start'] > clock:  # first scene of a chapter starts with its audio
            scenes[-len(marks)]['start'] = round(clock, 3)
        out_chapters.append({'chapter': ch['n'], 'title': ch['title'], 'audio': f"voiceover/ch{ch['n']:02d}.mp3",
                             'start': round(clock, 3), 'duration': round(dur, 3)})
        clock += dur
    return {'total_seconds': round(clock, 3), 'chapters': out_chapters, 'scenes': scenes}


def timeline(run):
    vo = run / 'voiceover'
    chapters = json.loads((vo / 'chapters.json').read_text(encoding='utf-8'))
    alignments, durations = [], []
    for ch in chapters:
        stem = f"ch{ch['n']:02d}"
        if not (vo / f'{stem}.mp3').exists():
            sys.exit(f'{vo / stem}.mp3 missing. Run the tts step first.')
        align_file = vo / f'{stem}.alignment.json'
        al = json.loads(align_file.read_text(encoding='utf-8')) if align_file.exists() else None
        if al is None:
            print(f'note: {stem} has no word timings; its scene times are estimated by position')
        elif len(al['characters']) != len(ch['text']):
            print(f'warning: {stem} alignment has {len(al["characters"])} characters, text has '
                  f'{len(ch["text"])}; scene times for this chapter are estimated by position')
        alignments.append(al)
        durations.append(duration(vo / f'{stem}.mp3', al))
    tl = build_timeline(chapters, alignments, durations)
    tl['timings'] = 'word' if all(alignments) else ('estimated' if not any(alignments) else 'mixed')
    (run / 'timeline.json').write_text(json.dumps(tl, indent=2, ensure_ascii=False), encoding='utf-8')
    missing = sum(1 for s in tl['scenes'] if s['visual'] is None)
    print(f"timeline.json: {len(tl['scenes'])} scenes, {tl['total_seconds']:.1f} s"
          + (f', {missing} stretch(es) of narration with no visual note' if missing else ''))


def selftest():
    md = """# Script: Test
## Narration
### Chapter 1: One (0:00)

[visual: banana close-up]

The banana is a copy. [F48, F63]

[visual: split screen]

Cut one open. [pause] No seeds. [F8]

### Chapter 2: Two (~1:00)

Before any note.

[visual: map]

Kuk Swamp. [F1]

## Self-check
| ignored | |
"""
    chs = parse(md)
    assert [c['n'] for c in chs] == [1, 2]
    assert chs[0]['text'] == 'The banana is a copy. Cut one open. ... No seeds.', chs[0]['text']
    assert chs[0]['markers'][0]['offset'] == 0 and chs[0]['markers'][1]['offset'] == len('The banana is a copy.')
    # fake alignment: every character lasts 0.1 s
    als = [{'characters': list(c['text']),
            'character_start_times_seconds': [i * 0.1 for i in range(len(c['text']))],
            'character_end_times_seconds': [(i + 1) * 0.1 for i in range(len(c['text']))]} for c in chs]
    durs = [len(c['text']) * 0.1 + 0.5 for c in chs]
    tl = build_timeline(chs, als, durs)
    s = tl['scenes']
    assert [x['scene'] for x in s] == [1, 2, None, 3], s
    assert s[0]['start'] == 0 and abs(s[1]['start'] - 2.2) < 1e-6, s  # "Cut" starts at char 22
    assert s[1]['end'] == round(durs[0], 3)
    assert s[2]['start'] == round(durs[0], 3) and s[2]['visual'] is None
    assert abs(s[3]['start'] - (durs[0] + len('Before any note. ') * 0.1)) < 1e-6
    assert abs(tl['total_seconds'] - sum(durs)) < 1e-6
    # no timings (OpenRouter): scenes placed by character position
    est = build_timeline(chs, [None, None], durs)['scenes']
    assert est[0]['start'] == 0
    assert abs(est[1]['start'] - durs[0] * chs[0]['markers'][1]['offset'] / len(chs[0]['text'])) < 1e-3, est
    assert est[1]['end'] == round(durs[0], 3) and est[2]['start'] == round(durs[0], 3)
    assert pcm_params('audio/pcm;rate=44100;channels=1') == (44100, 1)
    assert pcm_params('audio/pcm; rate=24000') == (24000, 1)
    print('selftest passed')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('command', choices=['split', 'tts', 'timeline', 'selftest'])
    p.add_argument('run', nargs='?', type=Path)
    p.add_argument('--provider', choices=list(PROVIDERS))
    p.add_argument('--voice')
    p.add_argument('--model')
    p.add_argument('--format', choices=['mp3', 'pcm'], default='mp3',
                   help='OpenRouter audio format; use pcm for models that only return pcm (e.g. HeyGen)')
    a = p.parse_args()
    if a.command == 'selftest':
        return selftest()
    if not a.run or not a.run.is_dir():
        sys.exit('Give the run folder, e.g. runs/2026-11-14-banana-history')
    if a.command == 'split':
        split(a.run)
    elif a.command == 'tts':
        if not (a.provider and a.voice and a.model):
            sys.exit('tts needs --provider, --voice and --model (from the Voice line in brief.md).')
        tts(a.run, a.provider, a.voice, a.model, a.format)
    else:
        timeline(a.run)


if __name__ == '__main__':
    main()
