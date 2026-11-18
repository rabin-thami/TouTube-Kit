# Stage 7 — Sources

Input: `claims.md`, `research.md`, `assets.md`.
Output: `<run>/sources.md`.

## Write sources.md

```
# Sources: <topic>

## Bibliography
- <Author or institution>. "<Title>." <Publisher/site>. <URL> (accessed <YYYY-MM-DD>)
  (every URL cited by a VERIFIED or DISPUTED claim that the script uses, deduplicated)

## Media credits
- Scene <n>: <attribution text from assets.md> — <source page URL>

## YouTube description
<one-paragraph summary of the video>

Sources:
<URL per line, same set as the bibliography>

Media credits:
<attribution text per line, one per asset, copied exactly from assets.md>
```

## Rules

- Copy attribution text exactly from assets.md. Do not shorten it.
- Do not list sources the script does not rely on in the YouTube block.
- Keep the YouTube description under 5,000 characters (YouTube's limit;
  `kit.py status` checks it). If the full source list does not fit, list each
  used claim's `source 1` as "Key sources (full bibliography in the pinned
  comment)" and keep the complete list in `## Bibliography`.

## Done when

`python3 kit.py status <run>` says the run is complete.
