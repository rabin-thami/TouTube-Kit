#!/usr/bin/env python3
"""Kallaway hook panel: a second diagnostic next to the upstream yt-script scorer. English only.

  python3 tools/kallaway_score.py <hooks.txt> [--topic "banana,cavendish"]
  python3 tools/kallaway_score.py selftest

Five properties, 0-20 each:
  Clarity       a cold viewer gets it in 3 s: 8-22 words, no filler opener
  Specificity   numbers, dates, durations, named things; hype words cost points
  Curiosity     an open question, a gap, a promise not yet paid
  Context+Lean  the topic is named in the first 12 words (--topic), plus proof, pain or stakes
  Snapback      an expectation flipped: but / actually / instead / not what you think

Verdict 0-100 = 60% of the mean + 40% of the weakest property (both scaled to 100), the same
weakest-link rule as the upstream scorer, so keyword stuffing one property cannot hide a dead one.
A filler opener ("hey guys", "welcome back"...) caps the verdict at 40.

Formulas: the 21 upstream ones (tools/yt-script/hooks.json) plus 6 Kallaway ones
(tools/hooks-kallaway.json). The formula with the most matching patterns wins; a tie goes to the
Kallaway formula, because it is the narrower shape.

Heuristic, not a predictor: thresholds are not calibrated on real view data. A low score is a reason
to look again; a high score is not a promise of views, CTR or retention. The craft guide's three-job
test and the facts always come first.
"""
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
FORMULAS = (json.loads((TOOLS / 'hooks-kallaway.json').read_text(encoding='utf-8'))['hooks']
            + json.loads((TOOLS / 'yt-script' / 'hooks.json').read_text(encoding='utf-8'))['hooks'])
DEVANAGARI = re.compile(r'[ऀ-ॿ]')


def words_re(words):
    return re.compile(r'\b(?:' + '|'.join(re.escape(w) for w in words) + r')\b', re.I)


FILLER_OPENER = re.compile(r"^(in this video|welcome back|hey guys|what'?s up|before we (get )?started|"
                           r"don'?t forget to (like|subscribe)|make sure to subscribe)", re.I)
SPECIFIC = [re.compile(p, re.I) for p in (
    r'\b\d+(\.\d+)?\s?%', r'\b\d{2,}(,\d{3})+\b', r'\bfrom \d+\b.*\bto \d+',
    r'\b\d+\s?(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b', r'\b(1[0-9]|20)\d\d\b')]
NUMBER = re.compile(r'\b\d')
HYPE = words_re(['massive', 'huge', 'amazing', 'incredible', 'insane', 'crazy', 'shocking', 'unbelievable',
                 'mind-blowing', 'game-changer', 'tons of', 'a lot'])
CURIOUS = words_re(['why', 'how', 'what', 'secret', 'mistake', 'wrong', 'hidden', 'nobody', 'truth', 'until',
                    'almost', 'except'])
OPEN_LOOP = re.compile(r"\b(here'?s|here is|i'?ll show you|by the end|what happens|the answer)\b", re.I)
GAP = re.compile(r'\b(without|never|zero|in one|no one)\b', re.I)
LEAN = words_re(['proof', 'result', 'pain', 'mistake', 'exact', 'proven', 'real', 'failed', 'quit', 'lost',
                 'lose', 'cost', 'risk', 'died', 'dead', 'dying', 'wiped', 'killed', 'gone', 'broke', 'fail'])
SNAP = [re.compile(p, re.I) for p in (
    r'\bbut\b', r'\bactually\b', r'\bis (actually )?wrong\b', r'\beveryone (says|thinks)\b', r"\bnot\b.*\bit'?s\b",
    r'\bvs\.?\b', r'\bversus\b', r'\binstead\b', r'\bthe truth is\b', r'\bnot what you think\b', r'\byet\b',
    r'\bturns out\b')]


def clarity(h):
    n = len(h.split())
    s = 20 - (8 if n < 6 else 4 if n < 8 else 10 if n > 30 else 5 if n > 22 else 0)
    if len(re.findall(r'\band\b', h, re.I)) >= 2 and n > 18:
        s -= 3  # two promises in one breath
    return 0 if FILLER_OPENER.search(h.strip()) else max(0, min(20, s))


def specificity(h):
    s = 4 + 5 * sum(1 for p in SPECIFIC if p.search(h))
    s += 2 if NUMBER.search(h) else 0
    w = h.split()
    named = sum(1 for prev, x in zip(w, w[1:]) if x[:1].isupper() and not prev.endswith(('.', '!', '?', ':')))
    s += min(6, 3 * named)  # capitalized mid-sentence = a named thing
    return max(0, min(20, s - 3 * len(HYPE.findall(h))))


def curiosity(h):
    s = 6 + (4 if h.strip().endswith('?') else 0) + (3 if CURIOUS.search(h) else 0)
    s += (4 if OPEN_LOOP.search(h) else 0) + (3 if GAP.search(h) else 0)
    if re.search(r'\b(because|which means|so that)\b', h, re.I):
        s -= 4  # the hook answers itself
    return max(0, min(20, s))


def context_lean(h, topic):
    first = ' '.join(h.split()[:12])
    if topic:
        ctx = 10 if words_re(topic).search(first) else 3 if words_re(topic).search(h) else 0
    else:
        ctx = 5  # topic not given: neutral, reported as unchecked
    return max(0, min(20, 6 + ctx + (4 if LEAN.search(h) else 0)))


def snapback(h):
    s = 6 + (8 if any(p.search(h) for p in SNAP) else 0)
    s += 3 if re.search(r'\beveryone\b.*\b(but|actually)\b', h, re.I) else 0
    s += 3 if re.search(r'\b(was|used to)\b.*\b(now|today)\b', h, re.I) else 0
    return max(0, min(20, s))


def classify(h):
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f['match'] if re.search(p, h, re.I))
        if n > hits:  # strict: earlier (Kallaway) formulas win ties
            best, hits = f, n
    return best, hits


def score(h, topic=None):
    if DEVANAGARI.search(h):
        raise SystemExit('Devanagari hook: this scorer is English only. Evaluate it qualitatively.')
    h = h.strip()
    parts = {'Clarity': clarity(h), 'Specificity': specificity(h), 'Curiosity': curiosity(h),
             'Context+Lean': context_lean(h, topic), 'Snapback': snapback(h)}
    vals = [v * 5 for v in parts.values()]
    verdict = round(0.6 * sum(vals) / len(vals) + 0.4 * min(vals))
    if FILLER_OPENER.search(h):
        verdict = min(verdict, 40)
    f, hits = classify(h)
    return {'hook': h, 'parts': parts, 'verdict': verdict, 'formula': f, 'hits': hits,
            'grade': 'SHIP' if verdict >= 75 else 'STRONG - fix the weakest property' if verdict >= 60
            else 'REWRITE - one property is leaking'}


FIX = {'Clarity': 'one idea in 8-22 words; drop any greeting or intro',
       'Specificity': 'swap an adjective for a number, a date or a name from the facts',
       'Curiosity': 'leave the answer out; end on the open question',
       'Context+Lean': 'name the topic in the first sentence, then the proof, pain or stakes',
       'Snapback': 'set up the expected idea, then flip it (but / actually / instead)'}


def report(r, topic):
    print(f"\n  {r['hook']}\n  {'-' * min(72, max(20, len(r['hook'])))}")
    for k, v in r['parts'].items():
        print(f"    {k:<13} {v:2d}/20  {'#' * v}")
    print(f"    {'VERDICT':<13} {r['verdict']:3d}    {r['grade']}")
    f = r['formula']
    print(f"    formula       {f['name'] + ' (' + str(r['hits']) + ' matched)' if f else 'none matched'}")
    if f:
        print(f"    fails when    {f['fails_when']}")
    low = min(r['parts'], key=r['parts'].get)
    print(f"    weakest       {low} - {FIX[low]}")
    if not topic:
        print('    note          no --topic given: Context was not checked')


def selftest():
    assert len(FORMULAS) == 27, len(FORMULAS)
    k = {f['id']: f for f in FORMULAS}
    for fid in [i for i in k if i.startswith('kallaway-') and i != 'kallaway-triple-alignment']:
        got = classify(k[fid]['example'])[0]
        assert got and got['id'] == fid, (fid, got and got['id'])
    stuffed = score("But actually, everyone thinks the truth is shocking, but why? Here's how. Real proof!")
    assert stuffed['verdict'] < 75, stuffed  # keyword stuffing must not reach SHIP
    real = score('Every 12 hours, this clock empties itself in about 40 seconds. Why?', ['clock'])
    assert real['verdict'] > stuffed['verdict'], (real['verdict'], stuffed['verdict'])
    filler = score('Hey guys welcome back, today: why your channel views went from 10 to 10,000 in 30 days?')
    assert filler['verdict'] <= 40 and filler['parts']['Clarity'] == 0, filler
    assert curiosity('It somehow works') == curiosity('It works')  # whole words only
    doc = 'In 1950 a fungus wiped out the most popular banana. Yours could be next.'
    assert score(doc, ['banana'])['parts']['Context+Lean'] > score(doc, ['mouse'])['parts']['Context+Lean']
    assert score(doc)['parts']['Specificity'] > score('A fungus wiped out a banana. Yours could be next.')['parts']['Specificity']
    try:
        score('केरा एउटा क्लोन हो।')
        raise AssertionError('Devanagari was not refused')
    except SystemExit:
        pass
    print('selftest passed')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['selftest']:
        selftest()
        sys.exit()
    topic = None
    if '--topic' in a:
        i = a.index('--topic')
        topic = [w.strip() for w in a[i + 1].split(',') if w.strip()]
        del a[i:i + 2]
    if len(a) != 1 or not Path(a[0]).is_file():
        sys.exit(__doc__)
    for r in sorted((score(l, topic) for l in Path(a[0]).read_text(encoding='utf-8').splitlines() if l.strip()),
                    key=lambda r: -r['verdict']):
        report(r, topic)
