#!/usr/bin/env python3
"""Build a CapCut timeline from transparent PNG pieces (video/capcut-pieces/manifest.json).

  python3 tools/capcut.py build <run-folder> <capcut-project-folder> [--static]   (--static: no keyframes, for testing)
  python3 tools/capcut.py selftest

The CapCut project must already contain one photo segment (any image, any keyframe) made by
the installed CapCut: its JSON is cloned for every piece, so the file matches that CapCut version.
CapCut must be closed while this runs. Back up the project folder first.

Replaces all video and text segments; keeps audio tracks as they are.
"""
import copy
import json
import re
import sys
import uuid
from pathlib import Path

W, H = 1920, 1080
US = 1_000_000  # CapCut times are microseconds


def new_id():
    return str(uuid.uuid4()).upper()


def to_capcut_xy(cx, cy):
    """Pixel centre in the 1920x1080 frame -> CapCut transform (canvas centre 0,0; edges +-1; y up)."""
    return (cx - W / 2) / (W / 2), (H / 2 - cy) / (H / 2)


def fit_scale(w, h):
    """CapCut scale 1.0 fits the image inside the canvas; this scale shows it at its own pixel size."""
    return 1 / min(W / w, H / h)


def parse_motion(text):
    """Motion phrase from the manifest -> entry move: dx, dy (px offset at start), scale_from, rot_from, seconds."""
    t = text.lower()
    m = {'dx': 0.0, 'dy': 0.0, 'scale_from': 1.0, 'rot_from': None, 'dur': 0.4}
    if t.startswith('none'):
        return None
    d = re.search(r'(\d+(?:\.\d+)?) s\)', t)
    if d:
        m['dur'] = min(float(d.group(1)), 1.5)
    xy = re.search(r'x ([+-]\d+), y ([+-]\d+)', t)
    px = re.search(r'(\d+) px', t)
    n = float(px.group(1)) if px else 150.0
    if xy:
        m['dx'], m['dy'] = float(xy.group(1)), float(xy.group(2))
    elif re.search(r'from (the )?left|unroll from left|wipe reveal|grow from left', t):
        m['dx'] = -n if px else -150
    elif 'from right' in t or 'from upper right' in t:
        m['dx'] = n
    elif 'above' in t:
        m['dy'] = -n
    elif 'below' in t or 'rise' in t or 'fly up' in t:
        m['dy'] = n
    s = re.search(r'scale (\d+(?:\.\d+)?) to 1\b', t)
    if s:
        m['scale_from'] = max(float(s.group(1)), 0.05)
    elif 'pop' in t:
        m['scale_from'] = 0.6
    r = re.search(r'rotate (-?\d+(?:\.\d+)?) to', t)
    if r:
        m['rot_from'] = float(r.group(1))
    return m


def keyframe(prop, points):
    """points: [(microseconds from segment start, value)]."""
    return {'id': new_id(), 'material_id': '', 'property_type': prop,
            'keyframe_list': [{'id': new_id(), 'curveType': 'Line', 'time_offset': int(t),
                               'left_control': {'x': 0.0, 'y': 0.0}, 'right_control': {'x': 0.0, 'y': 0.0},
                               'values': [v], 'string_value': '', 'graphID': ''} for t, v in points]}


def keyframes_for(piece, x, y, scale):
    m = parse_motion(piece['motion'])
    if m is None:
        return []
    end = m['dur'] * US
    kfs = []
    if m['dx'] or m['dy']:
        # CapCut drops a keyframe track whose values do not change, and a segment with only X keyframed
        # flickers between y and -y every frame. So both axes get a track; a still axis moves by 1e-4 (0.05 px).
        eps = 1e-4
        kfs.append(keyframe('KFTypePositionX', [(0, x + m['dx'] / (W / 2) if m['dx'] else x + eps), (end, x)]))
        kfs.append(keyframe('KFTypePositionY', [(0, y - m['dy'] / (H / 2) if m['dy'] else y + eps), (end, y)]))
    if m['scale_from'] != 1.0:
        kfs.append(keyframe('KFTypeScaleX', [(0, scale * m['scale_from']), (end, scale)]))
    if m['rot_from'] is not None:
        kfs.append(keyframe('KFTypeRotation', [(0, m['rot_from']), (end, piece['rotation_deg'])]))
    return kfs


def windows_path(p):
    """/home/user/x.png -> //wsl.localhost/Ubuntu/home/user/x.png (the form CapCut stored for the sample)."""
    return '//wsl.localhost/Ubuntu' + str(Path(p).resolve())


def build(draft, pieces, piece_dir, static=False):
    """Return a new draft dict with one video segment per piece; audio tracks kept."""
    d = copy.deepcopy(draft)
    mats = d['materials']
    video_segs = [s for t in d['tracks'] if t['type'] == 'video' for s in t['segments']]
    if not video_segs:
        sys.exit('The CapCut project has no photo segment to copy. Add one image in CapCut, save, close.')
    tpl_seg = video_segs[0]
    by_id = {m['id']: (k, m) for k, v in mats.items() if isinstance(v, list) for m in v if isinstance(m, dict) and 'id' in m}
    tpl_mat = by_id[tpl_seg['material_id']][1]
    tpl_refs = [by_id[r] for r in tpl_seg['extra_material_refs'] if r in by_id]

    audio_tracks = [t for t in d['tracks'] if t['type'] == 'audio']
    tpl_track = {k: v for k, v in next(t for t in draft['tracks'] if t['type'] == 'video').items() if k != 'segments'}
    layers = sorted({p['layer_order'] for p in pieces})
    tracks = {lo: dict(copy.deepcopy(tpl_track), id=new_id(), segments=[]) for lo in layers}
    mats['videos'] = []
    for kind, _ in tpl_refs:
        mats[kind] = [m for m in mats[kind] if m['id'] not in tpl_seg['extra_material_refs']]
    mats['texts'] = []
    mats['material_animations'] = []

    end_us = 0
    for p in pieces:
        mat = copy.deepcopy(tpl_mat)
        mat.update(id=new_id(), path=windows_path(piece_dir / p['file']), width=p['width'], height=p['height'],
                   material_name=p['file'])
        mats['videos'].append(mat)
        refs = []
        for kind, ref in tpl_refs:
            r = dict(copy.deepcopy(ref), id=new_id())
            mats[kind].append(r)
            refs.append(r['id'])
        start, dur = int(p['appear_s'] * US), int((p['leave_s'] - p['appear_s']) * US)
        x, y = to_capcut_xy(p['center_x'], p['center_y'])
        scale = fit_scale(p['width'], p['height'])
        seg = copy.deepcopy(tpl_seg)
        seg.update(id=new_id(), material_id=mat['id'], extra_material_refs=refs,
                   source_timerange={'start': 0, 'duration': dur}, target_timerange={'start': start, 'duration': dur},
                   render_index=p['layer_order'], track_render_index=layers.index(p['layer_order']),
                   common_keyframes=[] if static else keyframes_for(p, x, y, scale), keyframe_refs=[])
        seg['clip'] = dict(seg['clip'], scale={'x': scale, 'y': scale}, rotation=float(p['rotation_deg']),
                           transform={'x': x, 'y': y}, alpha=1.0)
        tracks[p['layer_order']]['segments'].append(seg)
        end_us = max(end_us, start + dur)
    for t in tracks.values():
        t['segments'].sort(key=lambda s: s['target_timerange']['start'])
        for a, b in zip(t['segments'], t['segments'][1:]):
            if a['target_timerange']['start'] + a['target_timerange']['duration'] > b['target_timerange']['start']:
                sys.exit(f"Two pieces overlap on layer track: {a['material_id']} / {b['material_id']}")
    d['tracks'] = [tracks[lo] for lo in layers] + audio_tracks
    d['duration'] = max(end_us, d.get('duration', 0) if audio_tracks else 0)
    return d


def overlap_safe(pieces):
    """Pieces that share a layer_order but overlap in time go to extra layers (e.g. 7 clone bananas)."""
    out, busy = [], {}
    for p in sorted(pieces, key=lambda p: (p['layer_order'], p['appear_s'])):
        lo = p['layer_order']
        while any(not (p['appear_s'] >= e or p['leave_s'] <= s) for s, e in busy.get(lo, [])):
            lo += 0.01
        busy.setdefault(lo, []).append((p['appear_s'], p['leave_s']))
        out.append(dict(p, layer_order=lo))
    return out


def main_build(run, project, static=False):
    piece_dir = run / 'video' / 'capcut-pieces'
    pieces = overlap_safe(json.loads((piece_dir / 'manifest.json').read_text(encoding='utf-8')))
    target = project / 'draft_content.json'
    if (project / '.locked').exists():
        sys.exit('CapCut has this project open (.locked exists). Close CapCut fully, then run again.')
    draft = json.loads(target.read_text(encoding='utf-8'))
    new = build(draft, pieces, piece_dir.resolve(), static)
    tmp = target.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(new, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    tmp.replace(target)
    n = sum(len(t['segments']) for t in new['tracks'] if t['type'] == 'video')
    print(f"{target}: {n} pieces on {sum(t['type'] == 'video' for t in new['tracks'])} video tracks, "
          f"{new['duration'] / US:.1f} s")


def selftest():
    assert to_capcut_xy(960, 540) == (0, 0) and to_capcut_xy(1920, 0) == (1, 1)
    assert fit_scale(1920, 1080) == 1 and abs(fit_scale(550, 308) - 550 / 1920) < 1e-9
    m = parse_motion('slide in from left 1200 px, settle (power4.out, 0.49 s)')
    assert m['dx'] == -1200 and m['dur'] == 0.49
    m = parse_motion('drop in from 900 px above, rotate -9 to -3, slight overshoot (0.6 s)')
    assert m['dy'] == -900 and m['rot_from'] == -9
    assert parse_motion('stamp in: scale 1.4 to 1 with fade, 3 steps (0.25 s)')['scale_from'] == 1.4
    assert parse_motion('fly in from upper right (x +500, y -200), rotate 60 to -6')['dx'] == 500
    assert parse_motion('none (static paper background)') is None
    props = [k['property_type'] for k in keyframes_for(
        {'motion': 'slide in from left 100 px (0.3 s)', 'rotation_deg': 0}, 0.0, 0.0, 1.0)]
    assert props == ['KFTypePositionX', 'KFTypePositionY'], props
    ky = keyframes_for({'motion': 'slide in from left 100 px (0.3 s)', 'rotation_deg': 0}, 0.0, 0.5, 1.0)[1]
    vals = [k['values'][0] for k in ky['keyframe_list']]
    assert vals[0] != vals[1] and abs(vals[0] - vals[1]) < 1e-3, vals  # still axis must not be a constant track
    ps = overlap_safe([{'layer_order': 9, 'appear_s': 0, 'leave_s': 2}, {'layer_order': 9, 'appear_s': 1, 'leave_s': 2}])
    assert ps[0]['layer_order'] != ps[1]['layer_order']
    print('selftest passed')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'selftest':
        selftest()
    elif len(sys.argv) in (4, 5) and sys.argv[1] == 'build':
        main_build(Path(sys.argv[2]), Path(sys.argv[3]), static=sys.argv[4:] == ['--static'])
    else:
        sys.exit(__doc__)
