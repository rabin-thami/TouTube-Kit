#!/usr/bin/env python3
"""Score English hook candidates with two panels: the upstream yt-script scorer
(tools/yt-script/hookscore.py, unchanged) and the Kallaway panel (tools/kallaway_score.py).

  python3 tools/hookcheck.py <hooks.txt> [--topic "banana,cavendish"]
        one hook per line; prints both panels for each hook, ranked by the upstream verdict.
        --topic: the video's subject words, so the Kallaway panel can check the topic is named early.
  python3 tools/hookcheck.py selftest

Two guards before scoring:
- [F#]/[Q#]/[C#] fact tags are removed: the scorer counts them as words (brevity) and as capitalized
  names (specificity), so a tagged hook scores differently from the spoken line.
- Devanagari text is refused (exit 1): the scorer only reads a-z words, so a Nepali hook would get
  meaningless numbers. Evaluate those hooks in words instead (pipeline/2-script-writer.md, "Hooks").

The score is a heuristic, not a prediction of views, CTR or retention (see tools/yt-script/UPSTREAM.md).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'yt-script'))
import hookscore  # noqa: E402  upstream, unchanged
import kallaway_score  # noqa: E402  tools/kallaway_score.py

TAG = re.compile(r'\s*\[[FQC]\d+(?:\s*,\s*[FQC]\d+)*\]')
DEVANAGARI = re.compile(r'[ऀ-ॿ]')


def clean(lines):
    """Strip fact tags; refuse Devanagari hooks."""
    hooks = [TAG.sub('', l).strip() for l in lines if l.strip()]
    nepali = [h for h in hooks if DEVANAGARI.search(h)]
    if nepali:
        raise SystemExit('Devanagari hook found; the English scorer would give meaningless numbers. '
                         f'Evaluate it qualitatively instead: {nepali[0][:60]}')
    return hooks


def selftest():
    assert len(hookscore.FORMULAS) == 21, len(hookscore.FORMULAS)
    assert clean(['The banana is a clone. [F48, F63]', '']) == ['The banana is a clone.']
    try:
        clean(['English line', 'केरा एउटा क्लोन हो।'])
        raise AssertionError('Devanagari was not refused')
    except SystemExit as e:
        assert 'Devanagari' in str(e)
    spoken = hookscore.score('Your banana is a copy')[1]
    assert hookscore.score('Your banana is a copy [F48, F63]')[1] != spoken  # why clean() strips tags
    assert hookscore.score(clean(['Your banana is a copy [F48, F63]'])[0])[1] == spoken
    print('selftest passed')


if __name__ == '__main__':
    if sys.argv[1:] == ['selftest']:
        selftest()
    else:
        a = sys.argv[1:]
        topic = None
        if '--topic' in a:
            i = a.index('--topic')
            topic = [w.strip() for w in a[i + 1].split(',') if w.strip()] if i + 1 < len(a) else None
            del a[i:i + 2]
        if len(a) != 1 or not Path(a[0]).is_file():
            sys.exit(__doc__)
        hooks = clean(Path(a[0]).read_text(encoding='utf-8').splitlines())
        if not hooks:
            sys.exit('No hooks in the file (one per line).')
        rows = sorted(((hookscore.score(t), t) for t in hooks), key=lambda r: -r[0][1])
        for (parts, verdict, name, hits), t in rows:
            print('\n=== upstream yt-script panel')
            hookscore.report(t, parts, verdict, name, hits)
            print('=== Kallaway panel')
            kallaway_score.report(kallaway_score.score(t, topic), topic)
