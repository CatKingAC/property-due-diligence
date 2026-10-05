# Review Log — property-due-diligence plugin

Five sequential review→revise rounds on the first full draft. Each round
lists its focus, genuine findings, and the changes made. Rubber-stamping
any round would have been a failure; every round changed the draft.

---

## Round 1 — Scope & structure
**Focus:** Is the workflow complete? Anything missing vs. the real research
it was modeled on?

**Findings:**
1. No existence gate: `normalize_address.py` validates *format* only.
   Nothing stops the workflow from "researching" a well-formed but
   nonexistent address.
2. Zoning/land-use not captured anywhere, though assessors publish it and
   it answers "is this really residential?".
3. Template §2 lacks a "Listing agent / brokerage" row, though the real
   report recorded it.
4. No valuation sanity-check step (the real workflow did
   assessed-value-vs-list-price math); template never prompts for it.
5. No listing-legitimacy check — fake listings / owner-impersonation scams
   are a real buyer risk and cheap to cover as a checklist item.

**Changes:**
- `SKILL.md` Step 1: added existence gate — if neither the assessor nor
  any aggregator returns the parcel, STOP and tell the user; never research
  a neighboring address as a proxy.
- `SKILL.md` Step 1: record zoning/land-use from the assessor.
- `report-template.md` §2: added "Zoning / land use" and
  "Listing agent / brokerage" rows, plus an optional "Valuation sanity
  check (inference — show the math)" bullet.
- `report-template.md` §6: added default item "confirm the listing is
  legitimate — contact the listing brokerage directly; beware
  rental/owner-impersonation scams".

---

## Round 2 — Data sources
**Focus:** Is each source correct, accessible, legal? How is
state/county variance handled?

**Findings (URL verification via curl, 2026-10-05):**
- 200 OK: publicrecords.netronline.com, nsopw.gov,
  nces.ed.gov/ccd/schoolsearch, spotcrime.com, crimemapping.com
- msc.fema.gov: connection failed from this network (000) — real official
  site, known slow/bot-sensitive; keep, with fallback note.
- census.gov/quickfacts and crimegrade.org: 403 bot-block — real sites;
  keep, since the skill runs in Claude Code with browser access.
- No fabricated URLs found; all eight check out as real.
- Missing: county GIS/parcel viewer (visual lot-boundary confirmation,
  linked from most assessor sites).
- Deed-office naming varies by state (Register of Deeds in TN, County
  Recorder in CA, Clerk of Court in FL) — the doc said only "Register of
  Deeds / Recorder".

**Changes:**
- `data-sources.md` §1: added county GIS/parcel viewer bullet.
- `data-sources.md` §2: added state naming-variance note for deed offices.
- `data-sources.md` intro: added explicit note that some sites bot-block
  automated access — on fetch failure, record the attempt and fall back
  to manual steps (already the skill's pattern; now stated up front).

---

## Round 3 — Verification honesty
**Focus:** Are the rules hard enough? Edge cases defined?

**Findings:**
1. No "as of" dates: listing price, listing status, and tax-paid status
   change over time; the report only carries a report date.
2. Weak rule: "2+ aggregators agreeing = verified" — aggregators syndicate
   the *same* MLS feed, so agreement is not independence.
3. The fictional example's Wyoming 9.5% inference paragraph is convoluted
   and distracts from the point it was illustrating.

**Changes:**
- `verification-rules.md`: new rule — time-sensitive facts (price,
  listing status, tax paid/delinquent) carry "as of <date read>".
- `verification-rules.md`: strengthened — for MLS-sourced facts,
  aggregator agreement counts as ONE source; `verified` requires
  assessor/official confirmation (or an explicit MLS# from the feed).
- `examples/sample-report.md`: rewrote the inference bullet as a short,
  clean illustration.

---

## Round 4 — Executability
**Focus:** Can Claude Code actually run each step? Concrete enough?

**Findings:**
1. Script paths in SKILL.md are bare relative paths with no anchor —
   ambiguous about what they're relative to.
2. (Found by actually running the scripts, pre-review) `fail()` passed
   `indent=2` to `print()` instead of `json.dumps()` — crashed on every
   error path.
3. (Found by testing) house numbers like "221B" wrongly triggered the
   "no house number" warning.

**Changes:**
- `SKILL.md` Workflow intro: "Scripts live in this skill's `scripts/`
  directory — resolve relative to this SKILL.md's location."
- `scripts/normalize_address.py`: fixed the `fail()` crash; fixed the
  house-number regex to accept alphanumeric numbers (`^\d+[A-Za-z]?\s`).
- Both scripts re-run green after the fixes (valid input, bad input,
  non-US input, scaffold generation incl. JSON sidecar).

---

## Round 5 — Adversarial
**Focus:** Template completeness; privacy; prompt injection; token budget;
manifest validity.

**Findings:**
1. Contradiction: template header says "fill every section, never silently
   dropped" but §5 says "skip if the user didn't ask — never pad".
2. Privacy rules don't gate person-targeted lookups (doxxing/harassment
   context) — only "addresses the user provides".
3. `plugin.json` had not been machine-validated.
4. Prompt-injection and token-budget posture were fine on re-read
   (web content treated as data; SKILL.md 3.8 KB + on-demand references).

**Changes:**
- `report-template.md`: §5 now "include briefly by default (3–5 bullets)";
   removed the "skip" line; header contradiction resolved.
- `verification-rules.md` Privacy: added — refuse when the request is
  about a *person* rather than a property purchase (no doxxing/harassment
  lookups).
- `plugin.json`: validated with `python3 -m json.tool` (parses; required
  fields name/version/description present).
