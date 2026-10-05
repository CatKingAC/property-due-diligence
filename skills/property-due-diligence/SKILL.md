---
name: "property_due_diligence"
description: "Buyer due diligence on a US residential address. Use when the user asks to research a property before buying, check whether an address is a single-family home, look up a house's history, or check an address for crimes, floods, or other red flags. Trigger on: 'due diligence on <address>', 'look into this house', 'research this property', 'is this address safe', 'check out this listing'. Produces a formal, source-cited buyer report with every fact labeled verified / third-party / unverified."
---

# Property Due Diligence

## Purpose
Produce a formal, source-cited buyer due-diligence report for one US residential address: property facts, incident/crime history at the exact address, public records (flood, tax, liens, permits, sex-offender registry), and neighborhood/schools. Every material fact carries a confidence label; inference is never presented as fact.

## Workflow
Scripts referenced below live in this skill's `scripts/` directory —
resolve them relative to this SKILL.md's location.

0. **Normalize and confirm.** Run `scripts/normalize_address.py "<address>"`. US addresses only (v1) — refuse non-US addresses plainly. If the address is ambiguous (missing ZIP, multiple matches), stop and ask the user which property they mean. Never research the wrong house.
1. **Property facts.** County assessor first (official source — see `references/data-sources.md` §1), then cross-check with 2+ MLS aggregators (Zillow, Realtor.com, Redfin, Homes.com). Record: property type, zoning/land-use, year built, sqft, lot size, beds/baths, owner of record, assessed value + tax history, sale/price history, parcel/APN, listing agent/brokerage. **Existence gate:** if neither the assessor nor any aggregator returns this parcel, STOP and tell the user the address doesn't resolve — never research a neighboring address as a proxy.
2. **Incident & crime history.** Exact-address news search (`"<street>, <city>"` + murder/shooting/fire/crime/incident), local newspaper archive, then SpotCrime/CrimeMapping for the block. Write "none found" explicitly when empty — absence of news is not proof of safety; say so.
3. **Public records.** FEMA flood zone (msc.fema.gov), county tax collector (delinquency), recorder of deeds (liens), NSOPW + state sex-offender registry, city permit portal. Anything behind a login or an interactive map you cannot read goes in as `unverified` with the exact manual step for the buyer.
4. **Neighborhood & schools.** Listing description, school district site / GreatSchools / NCES, Census QuickFacts. Keep brief; this section supports the purchase decision, it is not a relocation guide.
5. **Report.** Scaffold with `scripts/report_scaffold.py`, fill every section per `references/report-template.md`, apply `references/verification-rules.md` to every fact. Deliver: the report file path + a 5–8 line chat summary of key findings and the must-verify items needing the buyer's manual action.

## Output Contract
- One Markdown report at the user-chosen path (default `./<address-slug>-due-diligence-report.md`), following `references/report-template.md` exactly — all eight sections present, even if a section says "none found" or "unverified".
- Chat summary: 5–8 lines, key findings only, plus must-verify checklist items that need the buyer's manual action. Never paste the whole report into chat.

## Operating Rules
1. US residential addresses only (v1). Say no to anything else.
2. Verify, don't guess: no material fact without a source you actually read — see `references/verification-rules.md`.
3. Label every material fact `verified` / `third-party` / `unverified`. Never present inference as fact.
4. Read-only research: never contact owners, agents, or neighbors; never create accounts to bypass paywalls or registration walls.
5. Conflicting sources: report both, mark the fact `unverified`, and put the manual resolution step in Must-Verify Checklist.
6. One failed fetch proves nothing — record the attempt and move on.
7. Never reuse a real address from prior work in examples, tests, or docs. Examples are fictional and labeled as such.
