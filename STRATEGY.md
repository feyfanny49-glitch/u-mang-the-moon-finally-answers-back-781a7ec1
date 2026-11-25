# STRATEGY.md — The Moon Finally Answers Back

Competition `u-mang-the-moon-finally-answers-back-781a7ec1` (make.fun, program/v1, source bundle entry).
Bundle `06be9cd951533af59b34de1797988325f87ff555ad94ac7682d6e900ef595ad2`. Anchor commit kept:
`ee594e4` (makefun anchor, drand round 34263006), then `695d7b5` (LICENSE: MIT).

## 1. The exact deliverable

One file: `/output/entry.txt`.

- One single line of text, **1 to 240 characters**, UTF-8, not only white space.
- Written by the repository's entrypoint at grading time — `main.py` at the repo root
  (the python3.13 runtime: `python:3.13-slim`, python 3.13.17, stdlib only, no network,
  no secrets, nothing read from outside this repository).
- The bytes are a constant inside `main.py`. No trailing newline: the file is exactly the
  line, so a char-counting gate and a byte-counting gate both see the same 135 characters.
- `/output` must hold only that artifact, so the writer creates nothing else there.

Not a deliverable: no image, no dashboard, no README badges (the `repo_readme` /
`repo_about` checks apply to GitHub repository entries only; this is a source bundle entry).

## 2. How the entry is scored

Gate (sealed scorer, server side): `/output/entry.txt` is UTF-8 text, 1..240 chars, not only
white space → `Valid` = 1 or 0. Invalid entries are listed with 0, no rate, no prize.

Judge: `z-ai/glm-5.3-flash` on OpenRouter, reasoning effort high, ≤12,100 output tokens per
verdict, briefed as a comedy editor with a soft spot for the night sky and no patience for a
joke that needs explaining. Two entries at a time, A and B, each exactly as submitted, two
calls per game (one in each order), verdict naming A or B with a margin 1–5 and no tie. A
call gives the pick `0.5 + margin/10` and the other entry the rest; more than half wins.

The brief's criteria, most important first — the entry must satisfy them in this order:

1. Speaks as the Moon answering the wishes, howls and late-night promises of everyone
   staring up at it, and loses to any line the Moon says back.
2. Is funny on one read, a real laugh rather than a polite smile.
3. Sounds like the Moon's own voice, wry and old and a little tired of being wished upon.
4. Lands as a comeback in one read, with the turn arriving before the line ends.
5. Stays inside 240 characters and wastes none of them. *A line that explains its own joke
   has already lost the laugh. Length for its own sake does not count.*

Prizes go to the top five places only (1st $0.70, 2nd $0.50, 3rd $0.35, 4th $0.25,
5th $0.20), so the target is the top of a field of hundreds of lines per hour, not merely a
valid entry. The field on 25 Nov 2026 07:4x UTC held ~640 submissions in the hour, ~620 in
flight, and 3 fixed anchor texts (weak → strong) judged alongside every entry.

## 3. Hard caps and constraints

- 1 ≤ chars ≤ 240; UTF-8; not only white space; no trailing newline.
- File mode must not be 0600 (`tempfile.mkstemp` creates 0600 and the gate refuses that):
  the writer chmods the temp file to 0644 *before* `os.replace`, and re-checks the final mode.
- Runtime limits: 1 cpu, 512 MB, 64 pids, 60 s wall. The writer finishes in milliseconds.
- `Force_Last`, `max_per_day: 5`, `transcripts_required: true`, `strategy_note_required: false`,
  `license: osi`, `min_authored_coverage: 0`, `env_secrets: false`.
- Everything the entry runs ships in this repository: nothing is fetched, read from the
  network, from git history, or from an environment secret.

## 4. Plan to maximize the score (and what was done)

1. **Read the brief as an order of operations, not a wish list.** The line must first *be the
   Moon's reply* (criterion 1), then be funny (2), in voice (3), a comeback that turns before
   the end (4), with nothing wasted (5). The chosen line opens by promising the answer the
   contest's title sets up and then delivers a turn, so criteria 1 and 4 are structural, not
   decoration.
2. **Scan the public field, then refuse to look like it.** The newest judged rival texts were
   read from the public make.fun site (reference only, nothing copied; the entry holds no
   other entry's text). In the sample the same two jokes dominate: *"I am a rock, not a
   wishing well / not customer service"* and *"four billion years of your wishes, howls and
   2 a.m. promises"*. The words `man in the moon`, `flag`, `front yard`, `trespass`, `1972`
   and `Apollo` appear in none of them. The chosen angle is therefore new to the heat: the
   phrase the Moon is best known by is the one it has never been allowed to correct.
3. **One laugh, one turn, no scaffolding.** The Moon finally answers back, and the answer is
   a pedantic correction — then the reveal lands the complaint: one guy, one night, and his
   flag is still in the Moon's front yard. The joke is the reversal of a nursery image into
   an unsolved property dispute, which is exactly the register of criterion 3: old, wry, and
   tired of being both wished upon and named after a trespasser.
4. **Spend the budget.** 135 characters, three sentences, no clause that does not carry a
   beat: the promise of an answer, the correction, the landlord's ledger. The turn arrives
   before the line ends, so a judge reading once gets the laugh on the first pass.
5. **Make the artifact boring.** `main.py` writes the exact bytes atomically
   (`mkstemp` → write → fsync → chmod 0644 → `os.replace`), then verifies what landed:
   exact bytes, valid UTF-8, 1..240 characters, not only white space, mode 0644, and exits
   non-zero with a message if any check fails. A judged entry that fails its own gate is a
   zero, so this is where the effort goes after the wording.
6. **Keep the entrypoint legible to the reviewers**: the line is a module-level constant, and
   the writer/verifier is plain stdlib Python that any reader can check in one screen.

## 5. Risks accepted

- The correction angle depends on the judge knowing the phrase "the man in the moon" — a
  universal English idiom, so the cost is one beat, not an explanation (the line never
  explains the idiom; it argues with it).
- Humour is a coin toss; the mitigations are the ones the brief names: it is the Moon's reply,
  it turns before the end, and it looks like nothing else in the field.
