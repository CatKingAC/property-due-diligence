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

---

# Code review — scripts (rounds 6–10)

Deep review of `scripts/normalize_address.py` and
`scripts/report_scaffold.py`, conducted 2026-10-05 after the design rounds.
Each round lists genuine findings and the changes made. Test battery results
are recorded under Round 10.

## Round 6 — Correctness & edge cases
**Findings:**
1. `", ".join(parts[:-2])` on input with a doubled comma
   (`"123 Main St,, Springfield, IL 62704"`) leaked a stray `", "` into
   the canonical street.
2. US territories with US ZIP codes (PR, GU, VI, AS, MP) were rejected —
   wrongly, since they are US addresses.
3. `report_scaffold.py` used `TEMPLATE.format(...)`: any address containing
   `{`/`}` (e.g. `"123 {Main} St"`) crashed the script with KeyError.
4. `report_scaffold.py` accepted an empty address and wrote
   `-due-diligence-report.md`.
5. `report_scaffold.py` silently overwrote an existing report — a filled-in
   report is easy to destroy by accident.
6. Tail-parse error message (`could not parse state + ZIP from ...`) gave
   no hint of the expected format.

**Changes:**
- `normalize_address.py`: drop empty comma segments before splitting;
  added PR/GU/VI/AS/MP to the state set; tail error now shows the expected
  `'<ST> <ZIP>'` format.
- `report_scaffold.py`: template rendering switched to explicit
  `.replace("{address}", …).replace("{date}", …)`; empty address is a hard
  error; overwrite now requires `--force` (refuses otherwise with the file
  list); added `--slug` override so the agent can pin the report path to
  the slug from `normalize_address.py`; added `encoding="utf-8"` on all
  file writes.
- Scaffold template synced with `report-template.md`: added Zoning/land-use
  and Listing-agent rows (§2) and the listing-legitimacy checklist item
  (§6), which the design review added to the template but the scaffold
  was missing.

## Round 7 — Security
**Findings:**
1. Regex DoS audit: all patterns are simple (no nested quantifiers, no
   backtracking traps) — clean by inspection.
2. `out_dir` path traversal: considered and deliberately NOT hard-blocked.
   Threat-model reasoning: `out_dir` is chosen by the invoking agent, which
   already has arbitrary file-write through its own tools — the script adds
   no new capability, so a block would be theater with a usability cost.
   The attacker-influenced value is the *address*, and its path use (the
   slug) is already restricted to `[a-z0-9-]`.
3. Control/bidi-override characters (U+202E et al.) in a pasted address
   could corrupt report headings and terminal display.

**Changes:**
- `normalize_address.py`: strip Cc/Cf/format characters
  (`\x00-\x1f`, `\x7f-\u009f`, U+200E/200F, U+202A-202E, U+2066-2069)
  from the raw input before parsing.
- No `out_dir` block added (documented reasoning above instead).

## Round 8 — Portability
**Findings:**
1. `open()` without `encoding=` uses the locale default — on Windows
   (cp1252) this corrupts non-ASCII content (e.g. "Señora St", the
   template's em-dashes).
2. No documented minimum Python version.

**Changes:**
- All file writes now use `encoding="utf-8"`.
- Both scripts document "Requires Python 3.8+" (only 3.6+ features used;
  3.8 is the support floor). No POSIX-only calls; stdlib only (verified:
  imports are json/re/sys/datetime/os).

## Round 9 — API / UX design
**Findings:**
1. Slug inconsistency: `normalize_address.py` derives the slug from
   street+city+state (no ZIP), while `report_scaffold.py` slugified the
   full address string (with ZIP) — the agent could not predict the report
   path from the normalize output.
2. `report_scaffold.py` had no usage error for unknown flags.

**Changes:**
- Added `--slug` (round 6) and documented the wiring in SKILL.md's
  workflow: pass the slug from step 0 into the scaffold call.
- Tiny arg parser rejects unknown `--` flags with a clear error.

## Round 10 — Adversarial test battery (all green)
normalize_address.py:
- `"123 Main St, Springfield, IL 62704"` → canonical + slug OK
- `"123 Main St, Apt 4B, ..."` → unit preserved in street
- `"1600 Pennsylvania Avenue NW, Washington, DC 20500"` → DC accepted
- `"Calle Luna 123, San Juan, PR 00901"` → PR accepted (round 6 fix)
- `"123 Main St,, Springfield, IL 62704"` → no stray comma (round 6 fix)
- lowercase + ZIP+4 → normalized to `IL 62704`
- `"PO Box 123, ..."` → warning, not failure
- RTL-override char in input → stripped (round 7 fix)
- non-US (`UK`) / missing commas → clean JSON errors, exit 1

report_scaffold.py:
- braces in address → no crash, heading intact (round 6 fix)
- empty address → usage error, exit 1
- existing report without `--force` → refused with file list
- `--force` → overwrites; `--slug` → deterministic path; unknown flag → error

---

# Verification rounds (rounds 11–15) — search-grounded, no guessing

Rule for these rounds: every factual claim about platforms, formats, and
sources was verified by web search against official docs or the spec
before changing anything. Sources are cited inline.

## Round 11 — Agent Skills spec compliance
**Sources:** agentskills.io specification (via justinhubbard37/agentskills-docs,
serisium/doltrooms, immutex/mcode mirrors of the spec).

**Findings:**
1. **Spec violation:** frontmatter `name` was `property_due_diligence` but
   the directory is `property-due-diligence`. The spec requires the name to
   match the directory name (lowercase, digits, hyphens; ≤64 chars).
2. SKILL.md body is 39 lines — well under the 500-line / 5000-token limit.
3. `references/` is one level deep, no nested chains — compliant.
4. Description is 494 chars (limit 1024), states what + when to use — compliant.
5. The spec provides native `license` and `compatibility` (≤500 chars)
   frontmatter fields for exactly what the "Required capabilities" body
   section was saying — frontmatter is the right place (progressive
   disclosure: capabilities visible at catalog tier).

**Changes:**
- Frontmatter: `name: "property-due-diligence"` (matches directory);
  added `license: "MIT"`; added `compatibility` with the environment
  requirements; removed the duplicated body section.

## Round 12 — Claude Code plugin manifest + marketplace
**Sources:** official docs code.claude.com/docs/en/plugins-reference and
code.claude.com/docs/en/plugin-marketplaces (read in full).

**Findings:**
1. **README was wrong twice:** `/plugin marketplace add` takes
   `<owner>/<repo>` (or repo URL) — not a bare `github.com/...` path —
   and `/plugin install` takes `<plugin>@<marketplace-name>` — not a URL.
2. **Missing file:** a repo with only `plugin.json` cannot be added as a
   marketplace — the marketplace command registers repos that contain
   `.claude-plugin/marketplace.json`. The documented self-hosting pattern
   is the repo listing itself with `"source": "./"`.
3. `plugin.json` checked field-by-field against the official Fields table:
   all keys (`name`, `description`, `version`, `author.name`, `repository`,
   `license: MIT` SPDX, `keywords`) are recognized — no strip-warnings
   expected; `name` is kebab-case with no Anthropic-name collision.
4. Default component discovery covers our layout (`skills/` and
   `commands/` at plugin root) — no manifest path declarations needed.
5. Marketplace entry `name` must equal manifest `name` — both are
   `property-due-diligence`.

**Changes:**
- Added `.claude-plugin/marketplace.json` (repo as its own marketplace:
  `owner: CatKingAC`, one plugin entry, `source: "./"`).
- README install commands corrected to the documented forms.
- Limitation noted: `claude plugin validate` could not be run here (no
  Claude Code CLI in this environment) — the user should run
  `claude plugin validate .` once in Claude Code to confirm.

## Round 13 — Codex install path
**Sources:** OpenAI Codex docs via nirelbaz/promptpit knowledge base;
mrkhachaturov/agent-harness-docs; nacha192/codex-claude-code-team.

**Findings:**
1. `~/.codex/skills/<name>/SKILL.md` (user scope) confirmed — the README
   claim was correct.
2. Additionally verified: `.codex/skills/` (project scope) and the
   cross-tool `.agents/skills/` convention, which compliant clients scan
   alongside native directories.
3. `agents/openai.yaml` is optional UI/invocation metadata — not required;
   the skill works without it.
4. Skill-directory-name == frontmatter-name (fixed in round 11) is what
   Codex uses for discovery — the fix mattered here too.

**Changes:**
- README Codex row extended with the project-scope path and the
  `.agents/skills/` alternative. No skill changes needed.

## Round 14 — Data-source URL re-verification
**Sources:** msc.fema.gov FAQ pages; DOJ SMART Office / nsopw.gov "About NSOPW".

**Findings:**
1. FEMA Flood Map Service Center confirmed at msc.fema.gov with an
   Address Search feature (`/portal/search`) — matches data-sources.md.
   The doc's fallback note (site is slow/bot-sensitive; record the
   attempt, go manual) stays accurate.
2. NSOPW confirmed at www.nsopw.gov (DOJ SMART Office): free, supports a
   geographic-radius search around an address via the "Geographical
   Search" tab — matches data-sources.md §6.

**Changes:** none needed — both entries verified accurate as written.

## Round 15 — Repo hygiene / secret scan
**Findings:**
1. Grep for `api_key|secret|token|password|bearer` across md/py/json:
   clean (only prose mentions of "token budget").
2. Grep for email addresses: none in the repo.
3. LICENSE: MIT, `Copyright (c) 2026 CatKingAC` — correct.
4. Re-ran the real-address leak grep (`hixson|1905|37405`): no hits.

**Changes:** none — repo is clean.
