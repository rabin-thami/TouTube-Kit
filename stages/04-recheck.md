# Stage 4 — Re-check

Input: `script.md`, `claims.md`.
Output: none (a pass/fail report).

## Do

Run:

```
python3 kit.py recheck <run>
```

It fails (exit 1, every problem listed) when:

- a tag in script.md has no row in claims.md
- a tagged claim is `UNVERIFIED`
- a line uses a `DISPUTED` claim without saying it is disputed
- a `VERIFIED` claim lacks two `https` sources on different domains
- a narration line has no tag
- scene 1 is not a Hook of 40 words or fewer
- total narration words are outside the target length (150 words/min, ±10%)

It warns, without failing, about lines that look like more than one sentence.

On failure: fix `script.md` (or go back to stage 2 to verify a claim), then
run it again. Never weaken a claim's status to make the check pass.

## Done when

`recheck` prints `RECHECK PASSED` and exits 0.
