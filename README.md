# property-due-diligence

A Claude Code plugin for **buyer due diligence on a US residential address**.
Give it an address; it researches property facts, incident/crime history at
the exact address, public records (flood zone, tax, liens, permits,
sex-offender registry), and neighborhood/schools — then produces a formal,
source-cited buyer report where every material fact is labeled
`verified` / `third-party` / `unverified`.

Built from a real research workflow. It verifies; it doesn't guess.

## Install

```bash
# add this repo as a marketplace, then install the plugin
/plugin marketplace add github.com/CatKingAC/property-due-diligence
/plugin install property-due-diligence@https://github.com/CatKingAC/property-due-diligence
```

## Usage

```text
/due-diligence 123 Main St, Springfield, IL 62704
```

Or invoke the skill directly: ask Claude Code to "run due diligence on
<address>". The report is written to
`./<address-slug>-due-diligence-report.md` (or a path you name), and you get
a 5–8 line summary in chat. See `examples/sample-report.md` for the
(fictional) output shape.

## What it checks

1. **Property facts** — county assessor first, cross-checked against 2+
   MLS aggregators (Zillow, Realtor.com, Redfin, Homes.com): type, year
   built, sqft, lot, beds/baths, owner, assessed value + tax history, sale
   history, parcel/APN.
2. **Incident & crime history** — exact-address news search
   (murder/shooting/fire/incident), local paper archives, SpotCrime /
   CrimeMapping for the block. "None found" is stated explicitly; absence
   of news is never presented as proof of safety.
3. **Public records** — FEMA flood zone, county tax delinquency, recorder
   of deeds (liens), NSOPW + state sex-offender registry, city permit
   portal. Anything behind a login or unreadable interactive map is marked
   `unverified` with the exact manual step for the buyer.
4. **Neighborhood & schools** — assigned schools, brief sourced area notes.

## Scope and limits (v1)

- **US residential addresses only.** Public-records systems vary by
  state/county; the skill finds the right county portal per address.
- Read-only research. It never contacts owners/agents/neighbors and never
  creates accounts to bypass paywalls.
- **Not a substitute** for a title search, professional home inspection,
  or legal advice. The report's Must-Verify Checklist tells the buyer what
  to confirm by hand before closing.
- Some records (deeds, permits, registries) live behind interactive maps
  or logins the agent can't always read — those become explicit
  `unverified` items with manual steps, not guesses.

## Repo layout

```text
.claude-plugin/plugin.json
skills/property-due-diligence/
  SKILL.md                  # the 5-step workflow
  references/
    data-sources.md         # where to check what, per category
    report-template.md      # formalized output template (+ JSON sidecar)
    verification-rules.md   # verify-don't-guess rules, confidence labels
  scripts/
    normalize_address.py    # address parsing/validation (stdlib only)
    report_scaffold.py      # report + JSON skeleton generator
commands/due-diligence.md   # /due-diligence slash command
examples/sample-report.md   # fictional example output
REVIEW_LOG.md               # design review history (5 rounds)
```

## License

MIT — see [LICENSE](LICENSE).
