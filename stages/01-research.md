# Stage 1 — Research

Input: `run.json` (topic, minutes, language, audience).
Output: `<run>/research.md`.

## Do

1. Search the web for the topic. Open and read each source before you use it.
2. Prefer, in order:
   - primary sources and digitised originals (archives, national libraries)
   - museums and their collection pages
   - academic work (journals, university presses, university sites)
   - reputable encyclopedias (Britannica, national biographies, Smarthistory)
   Wikipedia may guide you to sources but must not be the only source for a fact.
   No unsourced blogs, content farms, forums, social media, or AI-written pages.
3. Collect enough for the target length (about 150 words/min). For 8-12 min,
   aim for 25-40 distinct facts.

## Write research.md

```
# Research: <topic>

## Timeline
- <date or period> — <event>. Source: <URL>

## Key people
- <name> (<dates if sourced>) — <role>. Source: <URL>

## Turning points
- <what changed and why it mattered>. Source: <URL>

## Causes and effects
- Cause: ... / Effect: ... Source: <URL>

## Surprising facts
- (at least 3) ... Source: <URL>

## Disagreements and myths
- <where sources disagree or a popular story is wrong>. Sources: <URL>, <URL>

## Sources consulted
- <Title> — <publisher/institution> — <URL>
```

## Rules

- Every bullet ends with at least one source URL you actually opened.
- Record dates exactly as the source gives them ("c. 1450", "by 1455").
  Do not sharpen vague dates.
- Quotes: only if copied verbatim from a source that prints them, with that URL.
  Otherwise paraphrase.
- Note when two sources disagree. Do not pick a winner silently.

## Done when

`python3 kit.py status <run>` reports stage 2 (Claims) as next.
