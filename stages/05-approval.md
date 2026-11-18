# Stage 5 — Approval gate (hard stop)

Input: `script.md`, `claims.md` (recheck must pass).
Output: `<run>/approval.json`.

## Do

1. Run `python3 kit.py recheck <run>`. It must pass.
2. Show the user the full text of `script.md` and `claims.md` (or, if your
   interface can open files, give both paths and a short summary: word count,
   estimated minutes, claim counts by status).
   Run `python3 kit.py hooks <run>` and show the **top 2 hooks** with their
   scores and patterns. If the user picks the other one, set it as `chosen`
   in hooks.md, make it Scene 1, re-run recheck, and ask again.
3. Ask: **Reply "approved" to continue to assets, or tell me what to change.**
4. **Stop. End your turn.** Do not search for assets or write any other file.
5. When the user replies:
   - exactly "approved" (any case, optional punctuation): run
     `python3 kit.py approve <run> --message "<their reply>"`
   - anything else: treat it as change requests. Edit, re-run recheck, and
     go back to step 2.

`kit.py approve` refuses anything other than "approved" and refuses if recheck
fails. Any later edit to script.md or claims.md voids approval;
`kit.py status` then sends you back here.

## Done when

`python3 kit.py status <run>` reports stage 6 (Assets) as next.
