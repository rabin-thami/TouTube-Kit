# Stage 2 — Claims

Input: `research.md`.
Output: `<run>/claims.md` (format: AGENTS.md → File contracts → claims.md).

## Do

1. Turn every fact you may use in the script into one atomic claim:
   one date, one number, one cause, or one event per claim.
2. For each claim, find two **independent** sources that agree:
   - different domains (kit.py enforces this)
   - not one copying the other; two Wikipedia language editions, or a site
     quoting Wikipedia, do not count as independent
3. Open both pages and confirm each one actually states the claim.
4. Set the status:
   - `VERIFIED`: both sources agree on the claim as worded
   - `DISPUTED`: credible sources disagree. Word the claim as the
     disagreement, e.g. "Sources differ on whether X happened in 1440 or 1450."
   - `UNVERIFIED`: only one source, or sources too weak. Keep the row (it
     documents what was checked) but the script must not use it.
5. If sources agree only on a vaguer version ("by 1455" vs "in 1455"),
   reword the claim to the version both support and mark it VERIFIED.

## Rules

- Never fill a source cell with a URL you did not open. Use `-` instead.
- No `|` characters inside cells.
- Include the 3+ surprising facts from research.md as claims.

## Done when

- `python3 kit.py check-urls <run>` prints `URLS OK` (no dead source links;
  `WARN` lines are sites that block scripts, so confirm those by hand), and
- `python3 kit.py status <run>` reports stage 3 (Script) as next.
