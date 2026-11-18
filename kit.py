#!/usr/bin/env python3
"""History video kit helper. Python 3 stdlib only. See AGENTS.md for file formats.

Commands:
  new "<topic>" [--minutes 8-12] [--language English] [--audience "general viewers"]
  status [<run>]          which stage a run stopped at (all runs if omitted)
  recheck <run>           script.md claim tags vs claims.md; exit 1 on any problem
  approve <run> --message "approved"
  fetch-assets <run>      download assets.md file urls into <run>/assets/
  check-assets <run>      licenses, attribution, files, scene coverage
  check-urls <run>        open every claims.md source URL; exit 1 on dead links
  hooks <run>             gate and rank hooks.md candidates; print the top 2
  agents                  list other coding-agent CLIs installed (for delegation)
  delegate <run> --agent opencode [--model M] [--stages 1-2]
                          run stages headless in another agent CLI, then show status
  export <run>            stage 8: write video/plan.json (scenes, narration, shots, assets, credits)
  shots <run>             stage 8: check the Director's shot list video/shots.md
  review <run> --scene N --verdict PASS|NOTES [--notes "..."]
                          stage 8: record the Director's verdict, tied to the composition's hash
  check-render <run> [--final]
                          stage 8: shots, Director PASS, audio, compositions, licensed media, credits;
                          --final needs draft approval
  approve-draft <run> --message "approved"
  self-test               built-in fixtures for recheck/approve/assets/status/production
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import html
import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"
WPM = 150
LENGTH_TOLERANCE = 0.10
HOOK_MAX_WORDS = 40
MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024
USER_AGENT = "history-video-kit/1.0 (python-urllib; research use)"

CLAIM_HEADER = ["id", "claim", "source 1", "source 2", "status"]
ASSET_HEADER = ["scene", "description", "type", "source page", "file url",
                "license", "attribution", "file"]
STATUSES = {"VERIFIED", "DISPUTED", "UNVERIFIED"}
ASSET_TYPES = {"image", "map", "footage", "doc"}

TAG_RE = re.compile(r"\[(C\d{2,}|NF)\]")
TRAILING_TAGS_RE = re.compile(r"(?:\s*\[(?:C\d{2,}|NF)\])+\s*$")
SCENE_RE = re.compile(r"^##\s+Scene\s+(\d+)\s*:\s*(.+?)\s*$", re.I)
SENTENCE_BREAK_RE = re.compile(r"[.!?][\"')\]]*\s+[A-Z]")
# word-bounded so "undisputed", "traditional", "legendary" do not count as hedges
HEDGE_RE = re.compile(
    r"\b(?:disputed?|debated?|debates|contested|uncertain|unclear|not certain|not known"
    r"|some (?:historians|scholars|sources|experts)|sources (?:differ|disagree)"
    r"|disagree(?:s|ment)?|may have|might have|possibly|perhaps"
    r"|according to (?:tradition|legend)|legend has it|it is said|reportedly)\b",
    re.I)
SAFE_FILE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
NUMBER_RE = re.compile(r"\b\d[\d,.]*\b")
MAX_DISPUTED_PER_SCENE = 2
OUTLINE_HEADINGS = ("## Angle", "## Packaging", "## Beat sheet", "## Retention plan", "## Ending")
# criteria from skills/storytelling/references: hooks-engineering.md §3.3 + attention-retention-manual.md §4.6
HOOK_CRITERIA = ["relevance", "specificity", "curiosity", "credibility", "clarity", "payoff", "fit", "honesty"]
HOOK_HEADER = ["id", "pattern", "hook", "claims", *HOOK_CRITERIA, "total", "chosen"]
MIN_HOOKS = 5
FIRST_30S_WORDS = 75  # ~30 s at 150 wpm: YouTube's "intro" retention window
BAIT_RE = re.compile(
    r"you won'?t believe|mind[- ]?blowing|\binsane\b|\bshocking\b|nobody (?:is )?talking about"
    r"|they don'?t want you to know|will blow your mind|\bwait (?:until|till) you see\b", re.I)
STOPWORDS = {"the", "and", "that", "with", "from", "this", "into", "their", "they", "what", "when", "were",
             "have", "your", "about", "history", "story", "video", "after", "before", "built", "lost"}
LICENSE_RE = re.compile(
    r"(?:PUBLIC DOMAIN(?: MARK 1\.0)?|PD(?:-[A-Z0-9-]+)?)(?: \(PD-[A-Z0-9-]+\))?"
    r"|CC0(?: 1\.0)?(?: UNIVERSAL)?"
    r"|CC BY(?:-SA)? [1-4]\.[05](?: [A-Z]{2}| INTERNATIONAL)?")
SECOND_LEVEL = {"co", "ac", "gov", "org", "net", "edu", "com"}

STAGES = [
    (1, "Research", "stages/01-research.md"),
    (2, "Claims", "stages/02-claims.md"),
    (3, "Outline + script", "stages/03-script.md"),
    (4, "Re-check", "stages/04-recheck.md"),
    (5, "Approval gate", "stages/05-approval.md"),
    (6, "Assets", "stages/06-assets.md"),
    (7, "Sources", "stages/07-sources.md"),
]


# ---------- helpers ----------

def slugify(text):
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")[:60]
    # non-Latin topics slug to nothing; a short hash keeps different topics apart
    return slug or "topic-" + hashlib.sha256(text.encode()).hexdigest()[:8]


def site(url):
    """Registrable-ish domain, so en.wikipedia.org and de.wikipedia.org count as one site."""
    host = (urllib.parse.urlparse(url).hostname or "").lower().rstrip(".")
    parts = host.removeprefix("www.").split(".")
    # shortcut: tiny public-suffix rule (example.co.uk), upgrade to a PSL if false matches appear
    n = 3 if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in SECOND_LEVEL else 2
    return ".".join(parts[-n:])


def is_https(url):
    p = urllib.parse.urlparse(url)
    return p.scheme == "https" and bool(p.hostname)


def license_ok(lic):
    s = " ".join(lic.strip().upper().split())
    tokens = set(re.split(r"[^A-Z0-9]+", s))
    if tokens & {"NC", "ND"}:
        return False
    return bool(LICENSE_RE.fullmatch(s))


def split_row(line, lower=True):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return [c.lower() for c in cells] if lower else cells


def parse_table(text, header, name):
    """Return (rows as dicts with '_line', errors) for the table whose header matches."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.strip().startswith("|") or split_row(line) != header:
            continue
        rows, errors = [], []
        for j in range(i + 2, len(lines)):
            raw = lines[j]
            if not raw.strip().startswith("|"):
                break
            cells = split_row(raw, lower=False)
            if len(cells) != len(header):
                errors.append(f"{name}:{j + 1}: expected {len(header)} cells, got {len(cells)}")
                continue
            row = dict(zip(header, cells))
            row["_line"] = j + 1
            rows.append(row)
        else:
            j = len(lines)
        # rows after a blank line would be silently ignored; make that loud
        stray = [k + 1 for k in range(j, len(lines)) if re.match(r"\s*\|\s*\S", lines[k])]
        if stray:
            errors.append(f"{name}:{stray[0]}: table row outside the table (blank line inside the table?)")
        return rows, errors
    return [], [f"{name}: no table with header | {' | '.join(header)} |"]


def resolve_run(arg):
    p = Path(arg)
    if not (p / "run.json").is_file():
        p = RUNS / arg
    if not (p / "run.json").is_file():
        sys.exit(f"ERROR: no run found at '{arg}' (expected run.json). Try: python3 kit.py status")
    return p


def minutes_range(run):
    data = json.loads((run / "run.json").read_text())
    spec = data.get("minutes") if isinstance(data, dict) else None
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(?:-\s*(\d+(?:\.\d+)?))?\s*", str(spec))
    if not m:
        raise ValueError(f"bad minutes '{spec}'")
    lo = float(m.group(1))
    hi = float(m.group(2) or lo)
    if lo > hi:
        raise ValueError(f"bad minutes '{spec}': low end above high end")
    return lo, hi


# ---------- claims + script ----------

def load_claims(run):
    path = run / "claims.md"
    if not path.is_file():
        return {}, ["claims.md: missing"]
    rows, errors = parse_table(path.read_text(encoding="utf-8"), CLAIM_HEADER, "claims.md")
    claims = {}
    for r in rows:
        where = f"claims.md:{r['_line']}"
        cid, status = r["id"], r["status"].upper()
        if not re.fullmatch(r"C\d{2,}", cid):
            errors.append(f"{where}: bad id '{cid}' (use C01, C02, ...)")
            continue
        if cid in claims:
            errors.append(f"{where}: duplicate id {cid}")
        if status not in STATUSES:
            errors.append(f"{where}: {cid} bad status '{r['status']}'")
        if not r["claim"]:
            errors.append(f"{where}: {cid} empty claim text")
        srcs = [r["source 1"], r["source 2"]]
        for s in srcs:
            if s not in ("", "-") and not is_https(s):
                errors.append(f"{where}: {cid} source is not an https URL: {s}")
        if status == "VERIFIED":
            if not all(is_https(s) for s in srcs):
                errors.append(f"{where}: {cid} VERIFIED needs two https sources")
            elif site(srcs[0]) == site(srcs[1]):
                errors.append(f"{where}: {cid} VERIFIED sources are the same site ({site(srcs[0])}); need independent sources")
        r["status"] = status
        claims[cid] = r
    return claims, errors


def parse_script(run):
    """Return (scenes, errors). scenes: list of {n, title, line, narration: [(lineno, text, tags)]}."""
    path = run / "script.md"
    if not path.is_file():
        return [], ["script.md: missing"]
    scenes, errors = [], []
    for no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        m = SCENE_RE.match(line)
        if m:
            scenes.append({"n": int(m.group(1)), "title": m.group(2), "line": no, "narration": []})
            continue
        if not scenes or not line or line.startswith((">", "#", "<!--")) or line == "---":
            continue  # title/target lines before scene 1, notes, headings, blanks
        scenes[-1]["narration"].append((no, line, TAG_RE.findall(line)))
    if not scenes:
        errors.append("script.md: no '## Scene <n>: <title>' headings")
    return scenes, errors


def recheck(run):
    """Return (errors, warnings, summary)."""
    claims, errors = load_claims(run)
    scenes, serr = parse_script(run)
    errors += serr
    warnings, used, words = [], set(), 0

    for i, sc in enumerate(scenes, 1):
        if sc["n"] != i:
            errors.append(f"script.md:{sc['line']}: scene numbered {sc['n']}, expected {i}")
        if not sc["narration"]:
            errors.append(f"script.md:{sc['line']}: scene {sc['n']} has no narration")
        disputed_lines = 0
        for no, text, tags in sc["narration"]:
            where = f"script.md:{no}"
            if not TRAILING_TAGS_RE.search(text):
                errors.append(f"{where}: narration line has no claim tag at the end: {text[:70]}")
            spoken = " ".join(TAG_RE.sub(" ", text).split())
            words += len(spoken.split())
            if SENTENCE_BREAK_RE.search(spoken):
                warnings.append(f"{where}: looks like more than one sentence; use one sentence per line")
            if len(NUMBER_RE.findall(spoken)) > 1:
                warnings.append(f"{where}: more than one number in a line; keep the one that matters")
            disputed_lines += any(claims.get(t, {}).get("status") == "DISPUTED" for t in tags)
            for tag in tags:
                if tag == "NF":
                    continue
                used.add(tag)
                c = claims.get(tag)
                if c is None:
                    errors.append(f"{where}: [{tag}] not found in claims.md")
                elif c["status"] == "UNVERIFIED":
                    errors.append(f"{where}: [{tag}] is UNVERIFIED and must not be in the script")
                elif c["status"] == "DISPUTED" and not HEDGE_RE.search(spoken):
                    errors.append(f"{where}: [{tag}] is DISPUTED but the line does not say so")
        if disputed_lines > MAX_DISPUTED_PER_SCENE:
            warnings.append(f"script.md:{sc['line']}: scene {sc['n']} has {disputed_lines} DISPUTED lines; "
                            f"more than {MAX_DISPUTED_PER_SCENE} stalls the story")

    if scenes:
        hook = scenes[0]
        hook_words = sum(len(TAG_RE.sub(" ", t).split()) for _, t, _ in hook["narration"])
        if "hook" not in hook["title"].lower():
            errors.append(f"script.md:{hook['line']}: scene 1 title must contain 'Hook'")
        if hook_words > HOOK_MAX_WORDS:
            errors.append(f"script.md:{hook['line']}: hook is {hook_words} words; max {HOOK_MAX_WORDS} (15 s)")
        try:
            lo, hi = minutes_range(run)
            wmin, wmax = int(lo * WPM * (1 - LENGTH_TOLERANCE)), int(hi * WPM * (1 + LENGTH_TOLERANCE))
            if not wmin <= words <= wmax:
                errors.append(f"script.md: {words} narration words; target {wmin}-{wmax} for {lo:g}-{hi:g} min at {WPM} wpm")
        except (ValueError, KeyError, OSError, TypeError) as e:
            errors.append(f"run.json: {e}")
    if scenes and not used:
        errors.append("script.md: no line cites a claim; every factual line needs a [Cxx] tag")
    oerr = check_outline(run)
    if oerr:
        warnings.append(f"{oerr} (stage 3 writes outline.md before the script)")
    if scenes:
        spoken = lambda t: " ".join(TAG_RE.sub(" ", t).split())
        norm = lambda t: " ".join(re.sub(r"[^\w]+", " ", t.lower()).split())
        hook_text = " ".join(spoken(t) for _, t, _ in scenes[0]["narration"])
        if (run / "hooks.md").is_file():
            _, hrows, herr = check_hooks(run, claims)
            warnings += [f"{e} (fix before stage 5)" for e in herr]
            chosen = [r for r in hrows if r["chosen"].lower() == "yes"]
            if len(chosen) == 1 and norm(chosen[0]["hook"]) != norm(hook_text):
                errors.append(f"script.md:{scenes[0]['line']}: scene 1 narration is not the chosen hook "
                              f"{chosen[0]['id']} in hooks.md")
        else:
            warnings.append("hooks.md: missing (stage 3 writes the hook lab first)")
        m = re.search(r"^#\s+(.+)$", (run / "script.md").read_text(encoding="utf-8"), re.M)
        first = " ".join(" ".join(spoken(t) for sc in scenes for _, t, _ in sc["narration"]).split()[:FIRST_30S_WORDS])
        if m and not content_words(m.group(1)) & content_words(first):
            warnings.append(f"script.md: the first {FIRST_30S_WORDS} words (~30 s) never touch the title's key words; "
                            "confirm the title's promise early")
        q_exits = sum(1 for sc in scenes[1:] if sc["narration"] and spoken(sc["narration"][-1][1]).endswith("?"))
        if q_exits * 2 > len(scenes) - 1:  # scenes after the hook; at most half may end on a question
            warnings.append(f"script.md: {q_exits} of {len(scenes) - 1} scenes after the hook end on a question; vary exits "
                            "(consequence, contradiction, reveal)")

    summary = {"scenes": len(scenes), "words": words, "minutes": round(words / WPM, 1),
               "claims_used": len(used),
               "claims_by_status": {s: sum(c["status"] == s for c in claims.values()) for s in sorted(STATUSES)}}
    return errors, warnings, summary


def content_words(text):
    return {w for w in re.findall(r"[a-z]+", text.lower()) if len(w) >= 4 and w not in STOPWORDS}


def check_hooks(run, claims=None):
    """Validate hooks.md. Return (title, rows ranked best-first with 'rejected' reasons, file errors).
    Gates only reject what code can judge honestly; the 0-2 scores are the writer's editorial judgement."""
    path = run / "hooks.md"
    if not path.is_file():
        return "", [], ["hooks.md: missing"]
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^Title:\s*(.+?)\s*$", text, re.M)
    title = m.group(1) if m else ""
    rows, errors = parse_table(text, HOOK_HEADER, "hooks.md")
    if not title:
        errors.append("hooks.md: missing 'Title: ...' line")
    if claims is None:
        claims, _ = load_claims(run)
    for r in rows:
        why = []
        try:
            scores = [int(r[c]) for c in HOOK_CRITERIA]
        except ValueError:
            errors.append(f"hooks.md:{r['_line']}: {r['id']} scores must be whole numbers 0-2")
            scores = [0] * len(HOOK_CRITERIA)
        if any(s not in (0, 1, 2) for s in scores):
            errors.append(f"hooks.md:{r['_line']}: {r['id']} scores must be 0, 1 or 2")
        if r["total"] != str(sum(scores)):
            errors.append(f"hooks.md:{r['_line']}: {r['id']} total {r['total']} != sum of scores {sum(scores)}")
        r["score"] = sum(scores)
        if 0 in scores:
            why.append("a criterion scored 0: " + ", ".join(c for c, s in zip(HOOK_CRITERIA, scores) if s == 0))
        hook = r["hook"]
        if len(hook.split()) > HOOK_MAX_WORDS:
            why.append(f"{len(hook.split())} words; max {HOOK_MAX_WORDS}")
        if len(NUMBER_RE.findall(hook)) > 1:
            why.append("more than one number")
        if BAIT_RE.search(hook):
            why.append("clickbait phrase")
        tags = [t for t in TAG_RE.findall(r["claims"]) if t != "NF"]
        if not tags:
            why.append("no claim tags; a hook states facts and needs [Cxx]")
        for t in tags:
            c = claims.get(t)
            if c is None:
                why.append(f"[{t}] not in claims.md")
            elif c["status"] == "UNVERIFIED":
                why.append(f"[{t}] is UNVERIFIED")
            elif c["status"] == "DISPUTED" and not HEDGE_RE.search(hook):
                why.append(f"[{t}] is DISPUTED but the hook does not say so")
        if title and not content_words(title) & content_words(hook):
            why.append("shares no key word with the title (does not confirm the click)")
        r["rejected"] = why
    chosen = [r for r in rows if r["chosen"].lower() == "yes"]
    if len(rows) < MIN_HOOKS:
        errors.append(f"hooks.md: {len(rows)} hooks; write at least {MIN_HOOKS}")
    if len(chosen) != 1:
        errors.append(f"hooks.md: mark exactly one row chosen = yes (found {len(chosen)})")
    elif chosen[0]["rejected"]:
        errors.append(f"hooks.md: chosen hook {chosen[0]['id']} fails a gate: {'; '.join(chosen[0]['rejected'])}")
    rows.sort(key=lambda r: (bool(r["rejected"]), -r["score"]))
    return title, rows, errors


def check_outline(run):
    """Return None if outline.md has every required heading, else the problem."""
    path = run / "outline.md"
    if not path.is_file():
        return "outline.md: missing"
    text = path.read_text(encoding="utf-8")
    missing = [h for h in OUTLINE_HEADINGS if h not in text]
    return f"outline.md: missing {', '.join(missing)}" if missing else None


# ---------- approval ----------

def content_hashes(run):
    return {n: hashlib.sha256((run / n).read_bytes()).hexdigest() for n in ("script.md", "claims.md")}


def approval_state(run):
    """Return 'valid', 'missing', or 'void'."""
    path = run / "approval.json"
    if not path.is_file():
        return "missing"
    try:
        saved = json.loads(path.read_text())["sha256"]
        return "valid" if saved == content_hashes(run) else "void"
    except (ValueError, KeyError, OSError, TypeError):
        return "void"


def approve(run, message):
    """Return None on success, else the refusal reason."""
    if os.environ.get("KIT_DELEGATED"):
        return "refused: delegated agents cannot approve; only the user can"
    if message.strip().rstrip(".!").strip().lower() != "approved":
        return f"refused: user reply was '{message}', not 'approved'"
    errors, _, _ = recheck(run)
    if errors:
        return "refused: recheck fails; run `python3 kit.py recheck` first"
    (run / "approval.json").write_text(json.dumps({
        "approved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "user_message": message,
        "sha256": content_hashes(run),
    }, indent=2) + "\n")
    return None


# ---------- assets ----------

def load_assets(run):
    path = run / "assets.md"
    if not path.is_file():
        return [], ["assets.md: missing"]
    return parse_table(path.read_text(encoding="utf-8"), ASSET_HEADER, "assets.md")


def check_assets(run):
    rows, errors = load_assets(run)
    scenes, _ = parse_script(run)
    scene_ids = {sc["n"] for sc in scenes}
    covered = set()
    if not rows and not errors:
        errors.append("assets.md: table has no rows")
    for r in rows:
        where = f"assets.md:{r['_line']}"
        if not r["scene"].isdigit() or int(r["scene"]) not in scene_ids:
            errors.append(f"{where}: scene '{r['scene']}' is not a scene in script.md")
        else:
            covered.add(int(r["scene"]))
        if r["type"].lower() not in ASSET_TYPES:
            errors.append(f"{where}: type '{r['type']}' not one of {sorted(ASSET_TYPES)}")
        if not license_ok(r["license"]):
            errors.append(f"{where}: license '{r['license']}' not allowed (Public domain, CC0, CC BY, CC BY-SA)")
        if not r["attribution"]:
            errors.append(f"{where}: empty attribution")
        if not r["description"]:
            errors.append(f"{where}: empty description")
        for col in ("source page", "file url"):
            if not is_https(r[col]):
                errors.append(f"{where}: {col} is not an https URL")
        f = run / "assets" / r["file"]
        if not SAFE_FILE_RE.fullmatch(r["file"]):
            errors.append(f"{where}: unsafe file name '{r['file']}'")
        elif not f.is_file() or f.stat().st_size == 0:
            errors.append(f"{where}: assets/{r['file']} not downloaded (run fetch-assets)")
    for n in sorted(scene_ids - covered):
        errors.append(f"assets.md: scene {n} has no asset")
    return errors


def fetch_assets(run):
    if approval_state(run) != "valid":
        return ["refused: script is not approved (stage 5); assets come after approval"]
    rows, errors = load_assets(run)
    (run / "assets").mkdir(exist_ok=True)
    seen = set()
    for r in rows:
        name, url = r["file"], r["file url"]
        if not SAFE_FILE_RE.fullmatch(name) or not is_https(url):
            errors.append(f"assets.md:{r['_line']}: skipped (unsafe file name or non-https url)")
            continue
        if not license_ok(r["license"]):
            errors.append(f"assets.md:{r['_line']}: skipped {name}: license '{r['license']}' not allowed")
            continue
        if name in seen:
            errors.append(f"assets.md:{r['_line']}: duplicate file name {name}")
            continue
        seen.add(name)
        dest = run / "assets" / name
        if dest.is_file() and dest.stat().st_size > 0:
            print(f"  have  {name}", flush=True)
            continue
        tmp = dest.with_name(dest.name + ".part")
        try:
            total = download(url, tmp)
            tmp.replace(dest)
            print(f"  got   {name} ({total // 1024} KB)", flush=True)
        except (OSError, ValueError, http.client.HTTPException) as e:
            tmp.unlink(missing_ok=True)
            errors.append(f"assets.md:{r['_line']}: download failed for {name}: {e}")
        time.sleep(1)  # be polite: media hosts (Wikimedia) rate-limit bursts with HTTP 429
    return errors


class HttpsOnlyRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse redirects that leave https (e.g. to http://169.254.169.254/ or http://localhost)."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not is_https(newurl):
            raise urllib.error.URLError(f"refused redirect to non-https URL: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(HttpsOnlyRedirect)


def download(url, dest, retries=4):
    """Stream url to dest with a size cap; retry HTTP 429 honoring Retry-After. Return bytes written."""
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with OPENER.open(req, timeout=60) as resp, open(dest, "wb") as out:
                total = 0
                while chunk := resp.read(1 << 16):
                    total += len(chunk)
                    if total > MAX_DOWNLOAD_BYTES:
                        raise ValueError(f"larger than {MAX_DOWNLOAD_BYTES >> 20} MB; use a smaller file url")
                    out.write(chunk)
            return total
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == retries:
                raise
            ra = e.headers.get("Retry-After", "")
            wait = min(int(ra) if ra.isdigit() else 15 * (attempt + 1), 120)
            print(f"  429   rate-limited, retrying in {wait}s", flush=True)
            time.sleep(wait)


# ---------- source URLs ----------

def claim_urls(run):
    claims, _ = load_claims(run)
    return sorted({s for c in claims.values() for s in (c["source 1"], c["source 2"]) if is_https(s)})


def url_status(url):
    """Return ('ok' | 'blocked' | 'dead', detail)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with OPENER.open(req, timeout=20) as resp:
            return "ok", resp.status
    except urllib.error.HTTPError as e:  # before OSError: HTTPError subclasses it
        return ("blocked" if e.code in (401, 403, 429) else "dead"), e.code
    except (OSError, ValueError, http.client.HTTPException) as e:
        return "dead", str(e)[:80]


# ---------- delegation to other agent CLIs ----------

# name: (default model or None = the CLI's own default, headless argv builder)
# shortcut: only opencode's flags were checked here; codex/gemini follow their docs, test before relying on them
AGENT_CLIS = {
    "opencode": ("opencode-go/deepseek-v4-pro",
                 lambda m, p: ["opencode", "run", "--auto", "--title", "history-video-kit", *(["-m", m] if m else []), p]),
    "codex": (None, lambda m, p: ["codex", "exec", "--full-auto", *(["-m", m] if m else []), p]),
    "gemini": (None, lambda m, p: ["gemini", "--yolo", *(["-m", m] if m else []), "-p", p]),
    "agy": ("gemini-3.8-flash-medium",  # Google Antigravity CLI; list models: agy models
            lambda m, p: ["agy", "-p", p, "--dangerously-skip-permissions", *(["--model", m] if m else [])]),
}

DELEGATE_PROMPT = (
    "Read AGENTS.md and follow it. You are a delegated worker for run folder {run}. "
    "Do ONLY these stages: {names}. "
    "First read any notes*.md file in {run}/ and reuse its verified quotes and URLs. "
    "Write files only inside {run}/. Never invent facts, quotes, dates or URLs. "
    "After each stage run `python3 kit.py status {run}`. "
    "After claims.md, run `python3 kit.py check-urls {run}` and fix every FAIL. "
    "Do not start any other stage, and never run kit.py approve. "
    "If a stage needs work from a stage you were not given (for example a new claim), "
    "do not do it: write what is missing at the end of your reply and stop. Stop when done."
)


def parse_stages(spec):
    m = re.fullmatch(r"(\d)(?:-(\d))?", spec)
    if not m:
        raise ValueError("--stages must look like 1 or 1-2")
    lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
    stages = list(range(lo, hi + 1))
    if not stages or stages[0] < 1 or stages[-1] > 7:
        raise ValueError("--stages must be within 1-7")
    if 5 in stages:
        raise ValueError("stage 5 (approval gate) needs the user; it cannot be delegated")
    return stages


# ---------- status ----------

def run_stage(run):
    """Return (next stage number, or None if complete; note)."""
    research = run / "research.md"
    if not research.is_file() or "https://" not in research.read_text(encoding="utf-8"):
        return 1, "research.md missing or has no source URLs"
    claims, cerr = load_claims(run)
    if cerr or not claims:
        return 2, (cerr[0] if cerr else "claims.md has no rows")
    oerr = check_outline(run)
    if oerr:
        return 3, oerr
    _, _, herr = check_hooks(run, claims)
    if herr:
        return 3, herr[0]
    if not (run / "script.md").is_file():
        return 3, "script.md missing"
    errors, _, _ = recheck(run)
    if errors:
        return 4, f"recheck fails ({len(errors)} problems): {errors[0]}"
    state = approval_state(run)
    if state != "valid":
        return 5, ("approval void: script.md or claims.md changed after approval"
                   if state == "void" else "waiting for the user to reply 'approved'")
    if not (run / "assets.md").is_file():
        return 6, "assets.md missing"
    aerr = check_assets(run)
    if aerr:
        return 6, f"check-assets fails ({len(aerr)} problems): {aerr[0]}"
    src = run / "sources.md"
    if not src.is_file():
        return 7, "sources.md missing"
    text = src.read_text(encoding="utf-8")
    for heading in ("## Bibliography", "## YouTube description"):
        if heading not in text:
            return 7, f"sources.md missing '{heading}'"
    bib, desc = text.split("## YouTube description", 1)
    if len(desc) > 5000:
        return 7, f"YouTube description is {len(desc)} characters; YouTube's limit is 5000"
    for r in load_assets(run)[0]:
        if r["attribution"] not in desc:
            return 7, f"YouTube description lacks attribution for {r['file']}"
    used = set(TAG_RE.findall((run / "script.md").read_text(encoding="utf-8")))
    for cid in sorted(used - {"NF"}):
        for url in (claims[cid]["source 1"], claims[cid]["source 2"]):
            if is_https(url) and url not in bib:
                return 7, f"Bibliography lacks {url} (cited by {cid})"
    return None, "all stages done"


# ---------- production (stage 8: voiceover + render) ----------

NOTE_RE = re.compile(r"^>\s*(VISUAL|TEXT|SOUND|NOTE)\s*(?:\[([A-Z-]+)\])?\s*:\s*(.*?)\s*$")
STRIP_TAGS_RE = re.compile(r"\s*\[(?:C\d{2,}|NF)\]")
MEDIA_REF_RE = re.compile(r"""<(?:img|image|video)\b[^>]*?\b(?:src|href)=["']([^"']+)["']""", re.I)


def script_beats(run):
    """Scenes in file order: {n, title, beats: [{kind, tag?, text}]}; kind 'line' is narration without tags."""
    scenes = []
    for raw in (run / "script.md").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        m = SCENE_RE.match(line)
        if m:
            scenes.append({"n": int(m.group(1)), "title": m.group(2), "beats": []})
        elif scenes and (nm := NOTE_RE.match(line)):
            beat = {"kind": nm.group(1), "text": nm.group(3)}
            if nm.group(2):
                beat["tag"] = nm.group(2)
            scenes[-1]["beats"].append(beat)
        elif scenes and line and not line.startswith((">", "#", "<!--")) and line != "---":
            scenes[-1]["beats"].append({"kind": "line", "text": STRIP_TAGS_RE.sub("", line).strip()})
    return scenes


def scene_lines(scene):
    return [b["text"] for b in scene["beats"] if b["kind"] == "line"]


def export_plan(run):
    """Write video/plan.json for a COMPLETE run. Return None on success, else the refusal reason."""
    stage, note = run_stage(run)
    if stage is not None:
        return f"refused: run is not complete (stage {stage}: {note})"
    scenes = script_beats(run)
    assets = load_assets(run)[0]
    for sc in scenes:
        sc["assets"] = [{k: r[k] for k in ("file", "description", "type", "license", "attribution")}
                        for r in assets if r["scene"] == str(sc["n"])]
    plan = {"script_sha256": content_hashes(run)["script.md"], "scenes": scenes,
            "credits": list(dict.fromkeys(r["attribution"] for r in assets))}
    (run / "video").mkdir(exist_ok=True)
    (run / "video" / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return None


SHOT_HEADER = ["shot", "scene", "lines", "takeaway", "type", "visual", "framing", "camera",
               "text", "transition", "sound", "assets"]
SHOT_TYPES = {"ARCHIVAL", "RECONSTRUCTION", "MAP", "TIMELINE", "DIAGRAM", "DETAIL", "B-ROLL", "TITLE"}
TRANSITIONS = {"cut", "zoom-through", "match-cut", "fade"}
NEEDS_ASSET = {"ARCHIVAL", "DETAIL"}
READ_WPS = 3.0  # on-screen words a viewer reads per second, plus READ_PAD seconds to find the text
READ_PAD = 0.5
LONG_SHOT = 20.0
REVIEW_HEADER = ["scene", "verdict", "composition", "reviewed", "notes"]


def load_plan(run):
    """Return (plan, error). Error if plan.json is missing, unreadable or stale."""
    try:
        plan = json.loads((run / "video" / "plan.json").read_text(encoding="utf-8"))
        stale = plan["script_sha256"] != content_hashes(run)["script.md"]
    except (OSError, ValueError, KeyError, TypeError):
        return None, "video/plan.json missing or unreadable; run `kit.py export`"
    return (None, "video/plan.json is stale: script.md changed; run `kit.py export`") if stale else (plan, None)


def wav_seconds(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def line_span(run, scene_n, first, last):
    """Seconds (start, end) of narration lines first..last (1-based) in scene_n's wav, or None without timings."""
    audio = run / "video" / "audio"
    try:
        words = json.loads((audio / f"s{scene_n:02d}.words.json").read_text(encoding="utf-8"))["words"]
        total = wav_seconds(audio / f"s{scene_n:02d}.wav")
    except (OSError, ValueError, KeyError, TypeError, EOFError, wave.Error):
        return None
    starts = {}
    for w in words:
        starts.setdefault(w["line"], w["s"])
    if first - 1 not in starts:
        return None
    return starts[first - 1], starts.get(last, total)  # next line's first word, or the end of the wav


def check_shots(run):
    """Return (errors, warnings) for video/shots.md, the Director's shot list."""
    plan, err = load_plan(run)
    if err:
        return [err], []
    path = run / "video" / "shots.md"
    if not path.is_file():
        return ["video/shots.md missing (the Director writes it; see stages/08-production.md)"], []
    rows, errors = parse_table(path.read_text(encoding="utf-8"), SHOT_HEADER, "shots.md")
    warnings, seen = [], set()
    scenes = {sc["n"]: len(scene_lines(sc)) for sc in plan["scenes"]}
    files = {r["file"] for r in load_assets(run)[0]}
    covered = {n: 0 for n in scenes}  # last narration line covered so far, per scene
    for r in rows:
        where = f"shots.md:{r['_line']}"
        sid = r["shot"]
        m = re.fullmatch(r"S(\d{2})-(\d{2})", sid)
        if not m:
            errors.append(f"{where}: bad shot id '{sid}' (use S03-01 = scene 3, shot 1)")
            continue
        if sid in seen:
            errors.append(f"{where}: duplicate shot {sid}")
        seen.add(sid)
        if not r["scene"].isdigit() or int(r["scene"]) not in scenes or int(r["scene"]) != int(m.group(1)):
            errors.append(f"{where}: {sid} scene '{r['scene']}' is not a scene in plan.json or does not match its id")
            continue
        n = int(r["scene"])
        for col in ("takeaway", "visual", "framing", "camera"):
            if r[col] in ("", "-"):
                errors.append(f"{where}: {sid} empty {col}")
        if any("vox" in v.lower() for k, v in r.items() if k != "_line"):
            errors.append(f"{where}: {sid} names Vox; take nothing from the reference videos")
        kind = r["type"].upper()
        if kind not in SHOT_TYPES:
            errors.append(f"{where}: {sid} type '{r['type']}' not one of {sorted(SHOT_TYPES)}")
        if kind == "RECONSTRUCTION" and "reconstruction" not in r["text"].lower():
            errors.append(f"{where}: {sid} RECONSTRUCTION needs on-screen text 'Reconstruction'")
        if r["transition"].lower() not in TRANSITIONS:
            errors.append(f"{where}: {sid} transition '{r['transition']}' not one of {sorted(TRANSITIONS)}")
        used = [] if r["assets"] in ("", "-") else [a.strip() for a in r["assets"].split(",")]
        for a in used:
            if a not in files:
                errors.append(f"{where}: {sid} asset '{a}' is not in assets.md")
        if kind in NEEDS_ASSET and not used:
            errors.append(f"{where}: {sid} {kind} shot needs a licensed asset from assets.md")
        if r["lines"] in ("", "-"):
            continue  # a hold or title shot with no narration
        lm = re.fullmatch(r"(\d+)(?:-(\d+))?", r["lines"])
        if not lm:
            errors.append(f"{where}: {sid} lines '{r['lines']}' must look like 3 or 3-5 or -")
            continue
        first, last = int(lm.group(1)), int(lm.group(2) or lm.group(1))
        if first != covered[n] + 1 or last < first or last > scenes[n]:
            errors.append(f"{where}: {sid} lines {r['lines']}: expected to start at line {covered[n] + 1} "
                          f"of scene {n} ({scenes[n]} lines), in order, no gaps or overlaps")
            continue
        covered[n] = last
        span = line_span(run, n, first, last)
        if span:
            dur = span[1] - span[0]
            words = 0 if r["text"] in ("", "-") else len(r["text"].split())
            need = words / READ_WPS + READ_PAD if words else 0
            if dur < need:
                errors.append(f"{where}: {sid} text needs {need:.1f}s to read; the shot lasts {dur:.1f}s")
            if dur > LONG_SHOT:
                warnings.append(f"{where}: {sid} lasts {dur:.0f}s; consider a second shot or a camera move")
    for n, total in scenes.items():
        if covered[n] != total:
            errors.append(f"shots.md: scene {n} narration lines {covered[n] + 1}-{total} have no shot")
    return errors, warnings


def composition_hash(run, n):
    p = run / "video" / "compositions" / f"s{n:02d}.html"
    return file_hash(p)[:12] if p.is_file() else "-"


def load_reviews(run):
    path = run / "video" / "review.md"
    if not path.is_file():
        return {}
    rows, _ = parse_table(path.read_text(encoding="utf-8"), REVIEW_HEADER, "review.md")
    return {r["scene"]: r for r in rows}


def record_review(run, scene, verdict, notes):
    """Director's verdict for one scene, tied to the composition it saw. Return None or the refusal reason."""
    plan, err = load_plan(run)
    if err:
        return f"refused: {err}"
    if scene not in {sc["n"] for sc in plan["scenes"]}:
        return f"refused: scene {scene} is not in plan.json"
    if verdict not in ("PASS", "NOTES"):
        return "refused: verdict must be PASS or NOTES"
    if verdict == "NOTES" and not notes.strip():
        return "refused: NOTES needs the notes (shot, timecode, note type, wanted result)"
    if composition_hash(run, scene) == "-":
        return f"refused: video/compositions/s{scene:02d}.html missing; nothing to review"
    reviews = load_reviews(run)
    reviews[str(scene)] = {"scene": str(scene), "verdict": verdict, "composition": composition_hash(run, scene),
                           "reviewed": datetime.date.today().isoformat(),
                           "notes": " ".join(notes.replace("|", "/").split()) or "-"}
    table = ["# Director review", "",
             "Written by `kit.py review`. A PASS holds only for the composition hash it names.", "",
             "| " + " | ".join(REVIEW_HEADER) + " |", "|" + "---|" * len(REVIEW_HEADER)]
    for key in sorted(reviews, key=int):
        table.append("| " + " | ".join(reviews[key][h] for h in REVIEW_HEADER) + " |")
    (run / "video" / "review.md").write_text("\n".join(table) + "\n", encoding="utf-8")
    return None


def check_render(run, final=False):
    """Errors that block a render. final=True also needs a valid draft approval."""
    stage, note = run_stage(run)
    if stage is not None:
        return [f"run is not complete (stage {stage}: {note})"]
    video = run / "video"
    plan, err = load_plan(run)
    if err:
        return [err]
    errors = check_shots(run)[0]
    reviews = load_reviews(run)
    for sc in plan["scenes"]:
        rv = reviews.get(str(sc["n"]))
        if not rv or rv["verdict"] != "PASS":
            errors.append(f"scene {sc['n']}: no Director PASS in video/review.md")
        elif rv["composition"] != composition_hash(run, sc["n"]):
            errors.append(f"scene {sc['n']}: composition changed after the Director's PASS; review again")
    for sc in plan["scenes"]:
        n = f"s{sc['n']:02d}"
        if not (video / "audio" / f"{n}.wav").is_file():
            errors.append(f"video/audio/{n}.wav missing (scene {sc['n']})")
        try:
            spoken = json.loads((video / "audio" / f"{n}.words.json").read_text(encoding="utf-8"))["lines"]
        except (OSError, ValueError, KeyError, TypeError):
            errors.append(f"video/audio/{n}.words.json missing or unreadable (scene {sc['n']})")
            continue
        if spoken != scene_lines(sc):
            errors.append(f"scene {sc['n']}: voiceover text differs from the approved narration; regenerate the audio")
        comp = video / "compositions" / f"{n}.html"
        if not comp.is_file():
            errors.append(f"video/compositions/{n}.html missing (scene {sc['n']})")
        elif any(b.get("tag") == "RECONSTRUCTION" for b in sc["beats"]) and \
                "reconstruction" not in comp.read_text(encoding="utf-8").lower():
            errors.append(f"video/compositions/{n}.html: RECONSTRUCTION shot needs an on-screen 'Reconstruction' label")
    allowed = {f"../assets/{r['file']}" for r in load_assets(run)[0]}
    for page in sorted(video.glob("compositions/*.html")):
        for ref in MEDIA_REF_RE.findall(page.read_text(encoding="utf-8")):
            if not ref.startswith("data:") and ref not in allowed:
                errors.append(f"video/compositions/{page.name}: media '{ref}' is not a licensed file from assets.md")
    credits = video / "compositions" / "credits.html"
    if not credits.is_file():
        errors.append("video/compositions/credits.html missing")
    else:
        text = html.unescape(credits.read_text(encoding="utf-8"))
        errors += [f"credits.html lacks attribution: {a}" for a in plan["credits"] if a not in text]
    if final and not errors:
        state = draft_approval_state(run)
        if state != "valid":
            errors.append("draft not approved by the user" if state == "missing"
                          else "draft approval void: draft.mp4 or script.md changed after approval")
    return errors


def draft_hashes(run):
    return {"draft.mp4": file_hash(run / "video" / "draft.mp4"), "script.md": content_hashes(run)["script.md"]}


def draft_approval_state(run):
    """Return 'valid', 'missing', or 'void' for video/render-approval.json."""
    path = run / "video" / "render-approval.json"
    if not path.is_file():
        return "missing"
    try:
        return "valid" if json.loads(path.read_text())["sha256"] == draft_hashes(run) else "void"
    except (ValueError, KeyError, OSError, TypeError):
        return "void"


def approve_draft(run, message):
    """Return None on success, else the refusal reason."""
    if os.environ.get("KIT_DELEGATED"):
        return "refused: delegated agents cannot approve; only the user can"
    if message.strip().rstrip(".!").strip().lower() != "approved":
        return f"refused: user reply was '{message}', not 'approved'"
    if not (run / "video" / "draft.mp4").is_file():
        return "refused: video/draft.mp4 missing; render the draft first"
    errors = check_render(run)
    if errors:
        return f"refused: check-render fails: {errors[0]}"
    (run / "video" / "render-approval.json").write_text(json.dumps({
        "approved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "user_message": message,
        "sha256": draft_hashes(run),
    }, indent=2) + "\n")
    return None


def production_state(run):
    """One-line production status for a COMPLETE run."""
    if not (run / "video" / "plan.json").is_file():
        return "not started: read stages/08-production.md"
    errors = check_render(run)
    if errors:
        return f"in progress ({len(errors)} open): {errors[0]}"
    if draft_approval_state(run) != "valid":
        return "draft render waiting for the user's 'approved' (kit.py approve-draft)"
    final = run / "video" / "final.mp4"
    return "final rendered: video/final.mp4" if final.is_file() else "draft approved: render the final"


def print_status(run):
    stage, note = run_stage(run)
    print(run.name)
    if stage is None:
        print("  COMPLETE (stages 1-7).")
        print(f"  Production: {production_state(run)}")
        return
    for n, name, _ in STAGES:
        mark = "done" if n < stage else ("NEXT" if n == stage else "    ")
        print(f"  [{mark}] {n}. {name}")
    n, name, prompt = STAGES[stage - 1]
    print(f"  Stopped at stage {n} ({name}): {note}")
    print(f"  Resume: read {prompt} and continue run {run.name}")


# ---------- commands ----------

def cmd_new(a):
    if not re.fullmatch(r"\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?", a.minutes):
        sys.exit("ERROR: --minutes must look like 10 or 8-12")
    lo, _, hi = a.minutes.partition("-")
    if hi and float(lo) > float(hi):
        sys.exit("ERROR: --minutes low end is above the high end")
    run = RUNS / f"{datetime.date.today().isoformat()}-{slugify(a.topic)}"
    if (run / "run.json").is_file():
        print(f"Run already exists: {run.relative_to(ROOT)}")
        print_status(run)
        return 0
    run.mkdir(parents=True, exist_ok=True)
    (run / "run.json").write_text(json.dumps({
        "topic": a.topic, "minutes": a.minutes, "language": a.language,
        "audience": a.audience, "created": datetime.date.today().isoformat(),
    }, indent=2) + "\n")
    print(f"Created {run.relative_to(ROOT)}")
    print("Next: read stages/01-research.md")
    return 0


def cmd_status(a):
    if a.run:
        print_status(resolve_run(a.run))
        return 0
    runs = sorted(p for p in RUNS.glob("*") if (p / "run.json").is_file()) if RUNS.is_dir() else []
    if not runs:
        print('No runs yet. Start one: python3 kit.py new "History of <X>"')
    for run in runs:
        try:
            print_status(run)
        except (ValueError, OSError) as e:  # one corrupt run must not hide the others
            print(f"{run.name}\n  ERROR reading run: {e}")
    return 0


def cmd_recheck(a):
    errors, warnings, s = recheck(resolve_run(a.run))
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}", file=sys.stderr)
    print(f"{s['scenes']} scenes, {s['words']} words (~{s['minutes']} min), "
          f"{s['claims_used']} claims used; claims.md: {s['claims_by_status']}")
    if errors:
        print(f"RECHECK FAILED: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print("RECHECK PASSED")
    return 0


def cmd_approve(a):
    err = approve(resolve_run(a.run), a.message)
    if err:
        print(f"APPROVAL {err}", file=sys.stderr)
        return 1
    print("APPROVED: approval.json written. Next: stages/06-assets.md")
    return 0


def cmd_export(a):
    err = export_plan(resolve_run(a.run))
    if err:
        print(f"EXPORT {err}", file=sys.stderr)
        return 1
    print("EXPORTED: video/plan.json written. Next: voiceover (stages/08-production.md)")
    return 0


def cmd_check_render(a):
    errors = check_render(resolve_run(a.run), final=a.final)
    for e in errors:
        print(f"FAIL  {e}", file=sys.stderr)
    if errors:
        print(f"CHECK-RENDER FAILED: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print("CHECK-RENDER PASSED" + (" (final render allowed)" if a.final else ""))
    return 0


def cmd_shots(a):
    errors, warnings = check_shots(resolve_run(a.run))
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}", file=sys.stderr)
    if errors:
        print(f"SHOTS FAILED: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print("SHOTS PASSED")
    return 0


def cmd_review(a):
    err = record_review(resolve_run(a.run), a.scene, a.verdict, a.notes)
    if err:
        print(f"REVIEW {err}", file=sys.stderr)
        return 1
    print(f"REVIEW recorded: scene {a.scene} {a.verdict} (video/review.md)")
    return 0


def cmd_approve_draft(a):
    err = approve_draft(resolve_run(a.run), a.message)
    if err:
        print(f"DRAFT APPROVAL {err}", file=sys.stderr)
        return 1
    print("DRAFT APPROVED: video/render-approval.json written. Next: final render")
    return 0


def cmd_fetch(a):
    errors = fetch_assets(resolve_run(a.run))
    for e in errors:
        print(f"FAIL  {e}", file=sys.stderr)
    return 1 if errors else 0


def cmd_check_assets(a):
    errors = check_assets(resolve_run(a.run))
    for e in errors:
        print(f"FAIL  {e}", file=sys.stderr)
    if errors:
        print(f"ASSETS FAILED: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print("ASSETS OK")
    return 0


def cmd_check_urls(a):
    run = resolve_run(a.run)
    _, cerr = load_claims(run)
    urls = claim_urls(run)
    if cerr or not urls:
        for e in cerr or ["claims.md has no https source URLs"]:
            print(f"FAIL  {e}", file=sys.stderr)
        print("URLS FAILED", file=sys.stderr)
        return 1
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        results = list(pool.map(url_status, urls))
    dead = 0
    for url, (state, detail) in zip(urls, results):
        if state == "dead":
            dead += 1
            print(f"FAIL  {url} ({detail})", file=sys.stderr)
        elif state == "blocked":
            print(f"WARN  {url} ({detail}: site blocks scripts; confirm by hand it exists and says the claim)")
    print(f"{len(urls)} URLs checked, {dead} dead")
    if dead:
        print("URLS FAILED", file=sys.stderr)
        return 1
    print("URLS OK")
    return 0


def cmd_hooks(a):
    run = resolve_run(a.run)
    title, rows, errors = check_hooks(run)
    print(f"Title: {title or '(none)'}")
    for r in rows:
        mark = "REJECTED" if r["rejected"] else f"{r['score']:>2}/{2 * len(HOOK_CRITERIA)}"
        star = " *chosen*" if r["chosen"].lower() == "yes" else ""
        print(f"  {r['id']:<4} {mark:<8} {r['pattern']}{star}\n       {r['hook']}")
        for why in r["rejected"]:
            print(f"       - {why}")
    top = [r for r in rows if not r["rejected"]][:2]
    if top:
        print("Top 2 for the approval gate: " + ", ".join(f"{r['id']} ({r['score']})" for r in top))
    for e in errors:
        print(f"FAIL  {e}", file=sys.stderr)
    if errors:
        print("HOOKS FAILED", file=sys.stderr)
        return 1
    print("HOOKS OK")
    return 0


def cmd_agents(_a):
    found = False
    for name, (model, _) in AGENT_CLIS.items():
        path = shutil.which(name)
        found |= bool(path)
        print(f"  {name:9} {'installed: ' + path if path else 'not installed'}"
              f"   default model: {model or '(CLI default)'}")
    if not found:
        print("No other agent CLI found; the current agent does all stages.")
    return 0


STAGE_OUTPUTS = {1: ["research.md"], 2: ["claims.md"], 3: ["hooks.md", "outline.md", "script.md"],
                 4: [], 6: ["assets.md"], 7: ["sources.md"]}
DELEGATE_TIMEOUT = 45 * 60  # seconds per model; a hung CLI falls through to the next model


def file_hash(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def guarded_hashes(run, stages=()):
    """Files a delegated agent must not touch: the kit, the approval record, and the
    outputs of earlier stages it was not given (e.g. claims.md during a stage-3 run)."""
    paths = [ROOT / "kit.py", ROOT / "AGENTS.md", ROOT / "CLAUDE.md", run / "approval.json",
             *sorted((ROOT / "stages").glob("*.md")), *sorted((ROOT / "skills").rglob("*.md")),
             *[run / f for n in (1, 2) if stages and n not in stages for f in STAGE_OUTPUTS[n]]]
    return {str(p): file_hash(p) for p in paths}


def delegate_chain(run, stages, models, build, prompt, log, label="agent"):
    """Try each model in order until one exits 0 AND writes every output of its stages.
    Return (exit code, model that succeeded or None)."""
    outputs = [run / f for n in stages for f in STAGE_OUTPUTS.get(n, [])]
    before = guarded_hashes(run, stages)
    env = {**os.environ, "KIT_DELEGATED": "1"}  # kit.py approve/delegate refuse inside the child
    rc = 1
    for model in models:
        out_before = {p: file_hash(p) for p in outputs}
        print(f"Trying {label} with model {model or 'CLI default'} ...", flush=True)
        with open(log, "a", encoding="utf-8") as out:
            out.write(f"\n===== {datetime.datetime.now().isoformat(timespec='seconds')} model={model} =====\n")
            out.flush()
            try:
                rc = subprocess.run(build(model, prompt), cwd=ROOT, env=env, stdout=out,
                                    stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                    timeout=DELEGATE_TIMEOUT).returncode
            except subprocess.TimeoutExpired:
                rc = 124
            except OSError as e:  # CLI vanished or not executable
                out.write(f"launch failed: {e}\n")
                rc = 127
        written = all(file_hash(p) != out_before[p] for p in outputs)
        print(f"  exit {rc}; outputs {'written' if written else 'NOT written'}", flush=True)
        changed = [p for p, h in guarded_hashes(run, stages).items() if before[p] != h]
        if changed:
            print("FAIL  delegated agent changed protected files; review before continuing:", file=sys.stderr)
            for p in changed:
                print(f"FAIL    {p}", file=sys.stderr)
            return 1, None
        if rc == 0 and written:
            return 0, model
    print("FAIL  every model failed (error, rate limit, timeout, or no output); "
          "the orchestrating agent must do these stages itself", file=sys.stderr)
    return rc or 1, None


def cmd_delegate(a):
    if os.environ.get("KIT_DELEGATED"):
        sys.exit("ERROR: already running as a delegated agent; delegation cannot nest")
    run = resolve_run(a.run)
    try:
        stages = parse_stages(a.stages)
    except ValueError as e:
        sys.exit(f"ERROR: {e}")
    if stages[-1] >= 6 and approval_state(run) != "valid":
        sys.exit("ERROR: stages 6-7 need a valid approval (stage 5) first")
    if a.agent not in AGENT_CLIS or not shutil.which(a.agent):
        sys.exit(f"ERROR: agent CLI '{a.agent}' not installed. See: python3 kit.py agents")
    default_model, build = AGENT_CLIS[a.agent]
    models = [m.strip() for m in a.model.split(",") if m.strip()] if a.model else [default_model]
    names = ", ".join(f"{n} {STAGES[n - 1][1]} ({STAGES[n - 1][2]})" for n in stages)
    rel = run.resolve().relative_to(ROOT) if run.resolve().is_relative_to(ROOT) else run
    log = run / f"delegate-{a.agent}.log"
    print(f"Delegating stages {a.stages} to {a.agent}; models in order: {', '.join(m or 'default' for m in models)}; log: {log}")
    rc, used = delegate_chain(run, stages, models, build, DELEGATE_PROMPT.format(run=rel, names=names), log, a.agent)
    if used is not None:
        print(f"Done with {a.agent} model {used or 'CLI default'}")
    print_status(run)
    return rc


# ---------- self-test ----------

def cmd_self_test(_a):
    checks = 0

    def expect(cond, label):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(f"self-test failed: {label}")

    good_claims = (
        "| id | claim | source 1 | source 2 | status |\n"
        "|----|-------|----------|----------|--------|\n"
        "| C01 | Fact one. | https://www.britannica.com/a | https://www.loc.gov/b | VERIFIED |\n"
        "| C02 | Sources differ on a date. | https://en.wikipedia.org/x | https://www.bl.uk/y | DISPUTED |\n"
        "| C03 | Weak fact. | https://example.org/z | - | UNVERIFIED |\n"
    )
    same_site = "| C04 | Same-site fact. | https://en.wikipedia.org/a | https://de.wikipedia.org/b | VERIFIED |\n"
    filler = "This sentence carries exactly ten words of verified narration here."  # 10 words
    body = "\n".join(f"{filler} [C01]" for _ in range(13))  # 130 words
    good_script = (
        "# Test video\n\nTarget: 1 min, English, general viewers\n\n"
        "## Scene 1: Hook\n> VISUAL: a page\nWhat changed everything in one year? [NF]\n\n"
        "## Scene 2: Story\n" + body + "\n"
        "Historians still debate the exact year it happened. [C02]\n"
    )  # 7 + 130 + 8 = 145 words; target 135-165

    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp) / "2000-01-01-test"
        run.mkdir()

        def write(name, text):
            (run / name).write_text(text, encoding="utf-8")

        def errs():
            return recheck(run)[0]

        write("run.json", json.dumps({"topic": "Test", "minutes": "1"}))
        expect(run_stage(run)[0] == 1, "status: empty run is at stage 1")
        write("research.md", "- fact. Source: https://www.loc.gov/b\n")
        expect(run_stage(run)[0] == 2, "status: stage 2 after research")
        write("claims.md", good_claims + same_site)
        expect(run_stage(run)[0] == 2, "status: stays at stage 2 while claims.md has errors")
        write("claims.md", good_claims)
        expect(run_stage(run)[0] == 3, "status: stage 3 after claims")

        write("script.md", good_script)
        expect(errs() == [], f"good script passes, got {errs()}")
        expect(run_stage(run)[0] == 3 and "outline" in run_stage(run)[1], "status: stage 3 until outline.md exists")
        write("outline.md", "## Angle\n## Packaging\n")
        expect("Beat sheet" in (check_outline(run) or ""), "outline missing headings is reported")
        write("outline.md", "\n".join(OUTLINE_HEADINGS) + "\n")
        expect(run_stage(run)[0] == 3 and "hooks.md" in run_stage(run)[1], "status: stage 3 until hooks.md exists")
        hrow = lambda i, hook, claims="[C01]", sc="2", chosen="no": (
            f"| H{i} | contradiction | {hook} | {claims} | " + " | ".join([sc] * len(HOOK_CRITERIA))
            + f" | {int(sc) * len(HOOK_CRITERIA)} | {chosen} |\n")
        hhead = "Title: What changed everything\n\n| " + " | ".join(HOOK_HEADER) + " |\n|" + "---|" * len(HOOK_HEADER) + "\n"
        good_hooks = hhead + hrow(1, "What changed everything in one year?", chosen="yes") + "".join(
            hrow(i, f"Everything changed in a single year, version {i}.") for i in range(2, 6))
        write("hooks.md", good_hooks)
        expect(check_hooks(run)[2] == [], f"good hooks pass: {check_hooks(run)[2]}")
        expect(run_stage(run)[0] == 5, "status: stage 5 when recheck passes, not approved")
        rejected = lambda text: {r["id"]: r["rejected"] for r in check_hooks(run)[1]}
        for label, row, needle in [
            ("bait", hrow(6, "You won't believe what changed everything."), "clickbait"),
            ("unverified", hrow(6, "Everything changed that year.", "[C03]"), "UNVERIFIED"),
            ("untagged", hrow(6, "Everything changed that year.", "-"), "no claim tags"),
            ("zero score", hrow(6, "Everything changed that year.", sc="0"), "scored 0"),
            ("off-title", hrow(6, "A monk printed a book.", "[C01]"), "title"),
            ("two numbers", hrow(6, "Everything changed in 1450 and 1455.", "[C01]"), "more than one number"),
        ]:
            write("hooks.md", good_hooks + row)
            expect(any(needle in w for w in rejected(None).get("H6", [])), f"hook gate rejects {label}")
        for label, text, needle in [
            ("too few", hhead + hrow(1, "What changed everything in one year?", chosen="yes"), "at least"),
            ("two chosen", good_hooks.replace("version 2. | [C01] | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 16 | no",
                                              "version 2. | [C01] | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 16 | yes"), "exactly one"),
            ("bad total", good_hooks.replace("| 16 | yes |", "| 15 | yes |"), "total"),
        ]:
            write("hooks.md", text)
            expect(any(needle in e for e in check_hooks(run)[2]), f"hooks.md file check catches {label}")
        write("hooks.md", good_hooks.replace("What changed everything in one year?", "Everything changed that year?"))
        expect(any("not the chosen hook" in e for e in errs()), "recheck: scene 1 must match the chosen hook")
        write("hooks.md", good_hooks)
        qs = good_script.replace("exact year it happened. [C02]", "exact year it happened? [C02]")
        write("script.md", qs)
        expect(any("end on a question" in w for w in recheck(run)[1]), "warns when most scenes end on a question")
        write("script.md", good_script)
        warns = lambda: recheck(run)[1]
        expect(not any("number" in w for w in warns()), "no number warning on clean script")
        write("script.md", good_script.replace("What changed everything in one year?",
                                               "What changed in 1450 and 1455?"))
        expect(any("more than one number" in w for w in warns()), "warns on two numbers in a line")
        heavy = good_script.replace("[C01]\n", "[C01]\nHistorians still debate this point too. [C02]\n", 3)
        write("script.md", heavy)
        expect(any("DISPUTED lines" in w for w in warns()), "warns on more than 2 DISPUTED lines in a scene")
        write("script.md", good_script)

        cases = [
            ("missing id", good_script.replace("[C02]", "[C99]"), "C99"),
            ("unverified", good_script.replace("[C02]", "[C03]"), "UNVERIFIED"),
            ("disputed unhedged", good_script.replace("Historians still debate", "Everyone knows"), "DISPUTED"),
            ("untagged line", good_script.replace("year? [NF]", "year?"), "no claim tag"),
            ("tag mid-line only", good_script.replace("year? [NF]", "year [NF] now?"), "no claim tag"),
            ("no hook", good_script.replace("Scene 1: Hook", "Scene 1: Intro"), "Hook"),
            ("long hook", good_script.replace("What changed", " ".join(["word"] * 40) + " What changed"), "hook is"),
            ("too short", good_script.replace(body, filler + " [C01]"), "narration words"),
            ("scene gap", good_script.replace("Scene 2:", "Scene 3:"), "expected 2"),
        ]
        for label, text, needle in cases:
            write("script.md", text)
            expect(any(needle in e for e in errs()), f"recheck catches {label}: {errs()}")
        write("script.md", good_script)

        write("claims.md", good_claims + same_site)
        expect(any("same site" in e for e in errs()), "same-site VERIFIED sources rejected")
        write("claims.md", good_claims.replace("| C02 |", "| C01 |", 1))
        expect(any("duplicate" in e for e in errs()), "duplicate claim id rejected")
        write("claims.md", good_claims)
        expect(site("https://a.nationalarchives.gov.uk/x") != site("https://www.bl.uk/y"), "site(): gov.uk vs bl.uk differ")
        expect(site("https://en.wikipedia.org/a") == site("https://de.wikipedia.org/b"), "site(): wikipedia editions match")
        expect(len(claim_urls(run)) == 5, f"claim_urls finds 5 https sources, skips '-', got {claim_urls(run)}")
        expect(parse_stages("1-2") == [1, 2], "parse_stages('1-2')")

        # review fixes: hedges, NF-only scripts, tables, run.json shape, site(), slugify
        for text, needle in [
            (good_script.replace("Historians still debate the exact year", "It is undisputed which year"), "DISPUTED"),
            (good_script.replace("Historians still debate the exact year", "The traditional legendary year is when"), "DISPUTED"),
            (good_script.replace("[C01]", "[NF]").replace("[C02]", "[NF]"), "no line cites a claim"),
        ]:
            write("script.md", text)
            expect(any(needle in e for e in errs()), f"recheck catches {needle!r} case: {errs()}")
        write("script.md", good_script)
        write("claims.md", good_claims.replace("| C02 |", "\n| C02 |"))
        expect(any("outside the table" in e for e in errs()), "blank line inside table is reported")
        write("claims.md", good_claims)
        write("run.json", "[]")
        expect(any("run.json" in e for e in errs()), "run.json of wrong shape is an error, not a crash")
        write("run.json", json.dumps({"topic": "Test", "minutes": "12-8"}))
        expect(any("low end" in e for e in errs()), "reversed minutes range is an error")
        write("run.json", json.dumps({"topic": "Test", "minutes": "1"}))
        expect(site("https://example.com./a") == site("https://www.example.com/b"), "site(): trailing dot")
        expect(slugify("印刷術") != slugify("活字") and slugify("印刷術").startswith("topic-"), "slugify: non-Latin topics differ")
        expect(fetch_assets(run)[0].startswith("refused"), "fetch-assets refuses before approval")
        # delegate_chain: falls through failing / silent models, stops at the first that writes outputs
        saved = {n: (run / n).read_text(encoding="utf-8") for n in STAGE_OUTPUTS[3]}
        fake = ("import sys,pathlib; r=pathlib.Path(sys.argv[1]); m=sys.argv[2]\n"
                "if m=='bad': sys.exit(1)\n"
                f"if m=='good': [(r/n).write_text((r/n).read_text()+'\\n') for n in {STAGE_OUTPUTS[3]!r}]\n")
        build = lambda m, p: [sys.executable, "-I", "-c", fake, str(run), m]
        tried = []
        trace = lambda m, p: (tried.append(m), build(m, p))[1]
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc, used = delegate_chain(run, [3], ["bad", "silent", "good", "never"], trace, "p", Path(tmp) / "log")
        expect((rc, used, tried) == (0, "good", ["bad", "silent", "good"]), f"chain falls through to first good model: {rc, used, tried}")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc, used = delegate_chain(run, [3], ["bad", "silent"], build, "p", Path(tmp) / "log")
        expect(rc != 0 and used is None, "chain fails when no model writes outputs")
        for n, t in saved.items():
            write(n, t)
        os.environ["KIT_DELEGATED"] = "1"
        try:
            expect(approve(run, "approved") is not None, "approve refuses inside a delegated agent")
        finally:
            del os.environ["KIT_DELEGATED"]
        write("approval.json", "[]")
        expect(approval_state(run) == "void", "approval.json of wrong shape is void, not a crash")
        (run / "approval.json").unlink()
        for spec in ("4-6", "5", "0-2", "8", "x"):
            try:
                parse_stages(spec)
                expect(False, f"parse_stages rejects {spec!r}")
            except ValueError:
                expect(True, f"parse_stages rejects {spec!r}")

        # approval
        expect(approve(run, "looks good") is not None, "approve refuses non-'approved' reply")
        expect(approval_state(run) == "missing", "no approval file after refusal")
        expect(approve(run, "Approved.") is None, "approve accepts 'Approved.'")
        expect(run_stage(run)[0] == 6, "status: stage 6 after approval")
        write("script.md", good_script + "One more line of narration added later on. [C01]\n")
        expect(approval_state(run) == "void", "editing script voids approval")
        expect(run_stage(run)[0] == 5, "status: back to stage 5 after edit")
        write("script.md", good_script)
        expect(approval_state(run) == "valid", "restoring approved text restores approval")

        # assets
        for lic, ok in [("Public domain", True), ("CC0", True), ("CC BY 4.0", True), ("CC BY-SA 3.0", True),
                        ("PD-US", True), ("CC BY-SA 2.0 DE", True), ("CC BY-NC 4.0", False),
                        ("CC BY-NC-SA 4.0", False), ("CC BY-ND 2.0", False), ("All rights reserved", False),
                        ("", False), ("Fair use", False), ("CC BY 2.5", True), ("CC BY-SA 2.5", True),
                        ("CC BY 4.0 International", True), ("Public domain (PD-Art)", True),
                        ("Public domain (non-commercial use only)", False),
                        ("PD but permission required", False), ("CC BY 4.0 ANY", False)]:
            expect(license_ok(lic) == ok, f"license_ok({lic!r}) == {ok}")
        head = "| " + " | ".join(ASSET_HEADER) + " |\n|" + "---|" * len(ASSET_HEADER) + "\n"
        row = ("| {s} | A page | image | https://commons.wikimedia.org/wiki/File:A.jpg | "
               "https://upload.wikimedia.org/a.jpg | {lic} | \"A\" by B, {lic}, via Wikimedia Commons | {f} |\n")
        (run / "assets").mkdir()
        (run / "assets" / "s01-a.jpg").write_bytes(b"x")
        (run / "assets" / "s02-a.jpg").write_bytes(b"x")
        good_assets = head + row.format(s=1, lic="Public domain", f="s01-a.jpg") + row.format(s=2, lic="CC BY-SA 4.0", f="s02-a.jpg")
        write("assets.md", good_assets)
        expect(check_assets(run) == [], f"good assets pass: {check_assets(run)}")
        bad = [
            ("NC license", good_assets.replace("CC BY-SA 4.0", "CC BY-NC 4.0"), "not allowed"),
            ("missing file", good_assets.replace("s02-a.jpg", "s02-b.jpg"), "not downloaded"),
            ("uncovered scene", head + row.format(s=1, lic="CC0", f="s01-a.jpg"), "scene 2 has no asset"),
            ("path traversal", good_assets.replace("s02-a.jpg", "../evil.jpg"), "unsafe file name"),
            ("bad scene", good_assets.replace("| 2 |", "| 9 |"), "not a scene"),
        ]
        for label, text, needle in bad:
            write("assets.md", text)
            expect(any(needle in e for e in check_assets(run)), f"check-assets catches {label}")
        write("assets.md", good_assets)

        # sources + completion
        expect(run_stage(run)[0] == 7, "status: stage 7 after assets")
        write("sources.md", "## Bibliography\n- x\n## YouTube description\n\"A\" by B, Public domain, via Wikimedia Commons\n")
        expect(run_stage(run)[0] == 7, "status: stage 7 when an attribution is missing")
        write("sources.md", "## Bibliography\n- https://www.britannica.com/a https://www.loc.gov/b https://en.wikipedia.org/x https://www.bl.uk/y\n## YouTube description\n"
              "\"A\" by B, Public domain, via Wikimedia Commons\n\"A\" by B, CC BY-SA 4.0, via Wikimedia Commons\n")
        expect(run_stage(run)[0] is None, f"status: complete, got {run_stage(run)}")

        # production (stage 8)
        video = run / "video"
        expect("not started" in production_state(run), "production: not started before export")
        expect(export_plan(run) is None, "export succeeds on a complete run")
        plan = json.loads((video / "plan.json").read_text(encoding="utf-8"))
        expect(scene_lines(plan["scenes"][0]) == ["What changed everything in one year?"], "export strips claim tags")
        expect(plan["scenes"][0]["beats"][0] == {"kind": "VISUAL", "text": "a page"}, "export keeps visual notes")
        expect(len(plan["credits"]) == 2 and plan["scenes"][1]["assets"][0]["file"] == "s02-a.jpg", "export maps assets")
        expect(any("s01.wav missing" in e for e in check_render(run)), "check-render: missing audio")
        (video / "audio").mkdir()
        (video / "compositions").mkdir()
        for sc in plan["scenes"]:
            n = f"s{sc['n']:02d}"
            (video / "audio" / f"{n}.wav").write_bytes(b"x")
            (video / "audio" / f"{n}.words.json").write_text(json.dumps({"lines": scene_lines(sc), "words": []}))
            (video / "compositions" / f"{n}.html").write_text(f'<img src="../assets/{n}-a.jpg">')
        expect(any("credits.html missing" in e for e in check_render(run)), "check-render: missing credits")
        (video / "compositions" / "credits.html").write_text(
            "".join(f"<p>{html.escape(c)}</p>" for c in plan["credits"]))

        # Director: shot list + review
        shead = "| " + " | ".join(SHOT_HEADER) + " |\n|" + "---|" * len(SHOT_HEADER) + "\n"
        srow = lambda sid, sc, lines, kind="ARCHIVAL", text="-", tr="cut", assets="s01-a.jpg": (
            f"| {sid} | {sc} | {lines} | The year mattered | {kind} | A page | close-up | slow push in "
            f"| {text} | {tr} | paper rustle | {assets} |\n")
        good_shots = shead + srow("S01-01", 1, "1") + srow("S02-01", 2, "1-7", "MAP", assets="-") + \
            srow("S02-02", 2, "8-14", assets="s02-a.jpg") + srow("S02-03", 2, "-", "TITLE", "Mainz, 1455", assets="-")
        expect(any("shots.md missing" in e for e in check_shots(run)[0]), "shots: missing file")
        write("video/shots.md", good_shots)
        expect(check_shots(run) == ([], []), f"good shot list passes: {check_shots(run)}")
        for label, text, needle in [
            ("gap", good_shots.replace("| 8-14 |", "| 9-14 |"), "expected to start at line 8"),
            ("uncovered", good_shots.replace("| 8-14 |", "| 8-13 |"), "14-14 have no shot"),
            ("bad type", good_shots.replace("| MAP |", "| SPLASH |"), "type 'SPLASH'"),
            ("bad transition", good_shots.replace("| cut |", "| star-wipe |", 1), "transition"),
            ("unlisted asset", good_shots.replace("s02-a.jpg", "evil.jpg"), "not in assets.md"),
            ("archival without asset", good_shots.replace("| s01-a.jpg |", "| - |"), "needs a licensed asset"),
            ("reconstruction unlabelled", good_shots.replace("| ARCHIVAL | A page", "| RECONSTRUCTION | A page", 1),
             "Reconstruction"),
            ("empty camera", good_shots.replace("slow push in", "-", 1), "empty camera"),
            ("vox", good_shots.replace("A page", "Vox-style page", 1), "Vox"),
            ("duplicate", good_shots + srow("S01-01", 1, "-"), "duplicate"),
        ]:
            write("video/shots.md", text)
            expect(any(needle in e for e in check_shots(run)[0]), f"shots catches {label}: {check_shots(run)[0]}")
        write("video/shots.md", good_shots)
        with wave.open(str(video / "audio" / "s01.wav"), "wb") as w:  # 1.5 s of silence, line 1 spoken 0.3-1.0 s
            w.setnchannels(1), w.setsampwidth(2), w.setframerate(8000), w.writeframes(b"\0\0" * 12000)
        s01_words = (video / "audio" / "s01.words.json").read_text()
        (video / "audio" / "s01.words.json").write_text(json.dumps(
            {"lines": scene_lines(plan["scenes"][0]), "words": [{"w": "What", "s": 0.3, "e": 1.0, "line": 0}]}))
        expect(check_shots(run)[0] == [], "short shot without text passes the reading check")
        write("video/shots.md", good_shots.replace("| slow push in | - | cut | paper rustle | s01-a.jpg |",
                                                   "| slow push in | " + " ".join(["word"] * 10)
                                                   + " | cut | paper rustle | s01-a.jpg |"))
        expect(any("to read" in e for e in check_shots(run)[0]), "shots: text too long for the shot's time")
        write("video/shots.md", good_shots)
        (video / "audio" / "s01.words.json").write_text(s01_words)
        expect(any("no Director PASS" in e for e in check_render(run)), "check-render needs a Director PASS")
        expect("NOTES needs" in (record_review(run, 1, "NOTES", "") or ""), "review: NOTES needs notes")
        expect(record_review(run, 9, "PASS", "") is not None, "review: unknown scene refused")
        expect(record_review(run, 1, "NOTES", "S01-01 0:02 design: headline too small") is None, "review: NOTES ok")
        expect(any("no Director PASS" in e for e in check_render(run)), "NOTES is not a PASS")
        expect(record_review(run, 1, "PASS", "") is None and record_review(run, 2, "PASS", "") is None, "review: PASS")
        good_words = (video / "audio" / "s02.words.json").read_text()
        (video / "audio" / "s02.words.json").write_text(json.dumps({"lines": ["Something else."], "words": []}))
        expect(any("differs" in e for e in check_render(run)), "check-render: voiceover text must match narration")
        (video / "audio" / "s02.words.json").write_text(good_words)
        (video / "compositions" / "s02.html").write_text('<img src="../assets/evil.jpg">')
        expect(any("not a licensed file" in e for e in check_render(run)), "check-render: unlisted media")
        expect(any("changed after the Director" in e for e in check_render(run)), "editing a scene voids its PASS")
        (video / "compositions" / "s02.html").write_text('<img src="../assets/s02-a.jpg">')
        good_plan = (video / "plan.json").read_text(encoding="utf-8")
        plan["scenes"][0]["beats"][0]["tag"] = "RECONSTRUCTION"
        (video / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
        expect(any("Reconstruction" in e for e in check_render(run)), "check-render: RECONSTRUCTION needs a label")
        (video / "plan.json").write_text(good_plan, encoding="utf-8")
        expect(any("not approved" in e for e in check_render(run, final=True)), "final render needs draft approval")
        expect("missing" in (approve_draft(run, "approved") or ""), "approve-draft refuses without draft.mp4")
        (video / "draft.mp4").write_bytes(b"draft")
        expect(approve_draft(run, "looks fine") is not None, "approve-draft refuses non-'approved' reply")
        expect("waiting" in production_state(run), "production: waiting for draft approval")
        expect(approve_draft(run, "approved") is None, "approve-draft accepts 'approved'")
        expect(check_render(run, final=True) == [], "final render allowed after draft approval")
        (video / "draft.mp4").write_bytes(b"draft v2")
        expect(any("void" in e for e in check_render(run, final=True)), "re-rendered draft voids draft approval")
        (video / "draft.mp4").write_bytes(b"draft")
        script = (run / "script.md").read_text(encoding="utf-8")
        write("script.md", script.replace("year? [NF]", "year, really? [NF]"))
        expect(any("not complete" in e or "stale" in e for e in check_render(run)), "script edit blocks the render")
        write("script.md", script)
        expect("draft approved" in production_state(run), f"production: draft approved, got {production_state(run)}")

    print(f"SELF-TEST PASSED ({checks} checks)")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="History video kit helper (see AGENTS.md)")
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="create a run folder")
    n.add_argument("topic")
    n.add_argument("--minutes", default="8-12")
    n.add_argument("--language", default="English")
    n.add_argument("--audience", default="general viewers")
    n.set_defaults(func=cmd_new)
    s = sub.add_parser("status", help="show which stage a run stopped at")
    s.add_argument("run", nargs="?")
    s.set_defaults(func=cmd_status)
    for name, func, hlp in [("recheck", cmd_recheck, "check script claims against claims.md"),
                            ("fetch-assets", cmd_fetch, "download asset files"),
                            ("check-assets", cmd_check_assets, "check asset licenses and files"),
                            ("check-urls", cmd_check_urls, "open every claims.md source URL"),
                            ("hooks", cmd_hooks, "gate and rank the hook candidates in hooks.md")]:
        c = sub.add_parser(name, help=hlp)
        c.add_argument("run")
        c.set_defaults(func=func)
    ap = sub.add_parser("approve", help="record the user's approval")
    ap.add_argument("run")
    ap.add_argument("--message", required=True, help="the user's reply, verbatim")
    ap.set_defaults(func=cmd_approve)
    e = sub.add_parser("export", help="write video/plan.json for a complete run (stage 8)")
    e.add_argument("run")
    e.set_defaults(func=cmd_export)
    cr = sub.add_parser("check-render", help="check render inputs; --final also needs draft approval")
    cr.add_argument("run")
    cr.add_argument("--final", action="store_true")
    cr.set_defaults(func=cmd_check_render)
    sh = sub.add_parser("shots", help="check the Director's shot list video/shots.md (stage 8)")
    sh.add_argument("run")
    sh.set_defaults(func=cmd_shots)
    rv = sub.add_parser("review", help="record the Director's verdict for one scene (stage 8)")
    rv.add_argument("run")
    rv.add_argument("--scene", type=int, required=True)
    rv.add_argument("--verdict", required=True, choices=["PASS", "NOTES"])
    rv.add_argument("--notes", default="", help="specific notes: shot, timecode, note type, wanted result")
    rv.set_defaults(func=cmd_review)
    ad = sub.add_parser("approve-draft", help="record the user's approval of video/draft.mp4")
    ad.add_argument("run")
    ad.add_argument("--message", required=True, help="the user's reply, verbatim")
    ad.set_defaults(func=cmd_approve_draft)
    g = sub.add_parser("agents", help="list other agent CLIs installed")
    g.set_defaults(func=cmd_agents)
    d = sub.add_parser("delegate", help="run stages in another agent CLI")
    d.add_argument("run")
    d.add_argument("--agent", default="opencode", choices=sorted(AGENT_CLIS))
    d.add_argument("--model", help="provider/model for that CLI (default: per-agent default)")
    d.add_argument("--stages", default="1-2")
    d.set_defaults(func=cmd_delegate)
    t = sub.add_parser("self-test", help="run built-in tests")
    t.set_defaults(func=cmd_self_test)
    a = p.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
