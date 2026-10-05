# Report Template

Fill **every** section. A section with nothing to report still appears, with
"none found" or "unverified" stated explicitly — never silently dropped.
Report language follows the user's request (default: match the user's
language). Confidence labels: `verified` / `third-party` / `unverified`
(see `verification-rules.md`).

```markdown
# Property Due-Diligence Report: <full address>

- Report date: <YYYY-MM-DD>
- Prepared for: home-buyer due diligence (read-only public-records research)
- Scope: US residential, v1. Not a substitute for title search, home
  inspection, or legal advice.

---

## 1. Executive Summary

5–8 lines, findings only. Lead with: property type verdict, price vs
assessment, any red flags found, and the count of must-verify items.
Example shape (do not copy wording):
- Single-family residence, built <year>, <beds>bd/<baths>ba, <sqft> sqft.
- Listed at $<price> (<date>); last sold $<price> (<date>).
- No crimes/fires reported at this exact address in public sources searched.
- Flags: <e.g. third-party flood-zone flag, unverified> / none.
- <N> items need manual verification before closing (see §6).

---

## 2. Property Facts

| Fact | Value | Source | Confidence |
|------|-------|--------|------------|
| Property type | | | |
| Zoning / land use | | | |
| Year built | | | |
| Living area (above grade) | | | |
| Lot size | | | |
| Bedrooms / bathrooms | | | |
| Parking | | | |
| HOA | | | |
| Parcel / APN | | | |
| Owner of record | | | |
| Current list price (MLS#, as of <date>) | | | |
| Listing agent / brokerage | | | |
| Price history | | | |
| Assessed value (<year>) | | | |
| Annual property tax | | | |
| Tax history (table) | | | |

- Source column: short name + full URL on first use.
- Cross-check rule: assessor or 2+ aggregators agreeing → `verified`;
  single aggregator → `third-party`. (For MLS-sourced facts, aggregator
  agreement counts as one source — see `verification-rules.md`.)
- Note methodology differences explicitly (e.g. living-area figures that
  include/exclude basement).
- Optional: valuation sanity check (inference, not fact) — e.g. assessed
  value ÷ state assessment ratio vs. list price. Show the arithmetic or
  omit it.

---

## 3. Incident & Crime History

### 3a. Exact address: <full address>
- Queries run (list them all, e.g. `"123 Main St" "Springfield" murder`,
  news vertical, local paper archive):
- Result: **none found** / or one bullet per incident with date, what
  happened, and source URL.
- State plainly: absence of news coverage is not proof nothing happened.

### 3b. Immediate area (≤0.5 mi)
- SpotCrime / CrimeMapping: what the map showed (counts by category if
  readable), or `unverified` + manual steps.
- CrimeGrade: label the geographic scope actually shown (city /
  neighborhood / ZIP, or block-level for address searches). Never present
  a city grade as a block-level fact.

---

## 4. Public Records

| Record | Finding | Source | Confidence |
|--------|---------|--------|------------|
| FEMA flood zone | Zone <X/AE/…> (panel <n>, dated <d>) — or flag + unverified | | |
| Tax delinquency | | | |
| Liens / foreclosure | | | |
| Sex-offender registry (≤1 mi) | <n> registrants at listed distances — or unverified + steps | | |
| Building permits | | | |

- Conflicting sources: show both rows, mark `unverified`, move resolution
  to §6 with the exact office/phone/URL.

---

## 5. Neighborhood & Schools

Include briefly by default (3–5 sourced bullets): area character,
assigned schools (district source: elementary / middle / high). This
section supports the purchase decision; it is not a relocation guide —
never pad.

---

## 6. Must-Verify Checklist (manual, before closing)

Numbered items the buyer (or their agent/title company/inspector) must
confirm by hand. Each item: what to verify + exactly where/how
(office name, phone, or URL). Typical items: flood determination, tax
status, deed/seller entity, sex-offender map, home inspection + permits,
title search, spot-check crime maps, and: confirm the listing itself is
legitimate — contact the listing brokerage directly; beware
rental/owner-impersonation scams.

---

## 7. Unverified Items

Everything the research could not confirm and why (login wall,
interactive map unreadable, no public record found). One line each.
This section is mandatory — an empty "all verified" claim is not allowed
unless every material fact is truly `verified`.

---

## 8. Sources

Numbered list of every URL actually read, in order of first use.
```

## JSON sidecar (optional)

When the caller wants machine-readable output, also write
`<slug>-due-diligence-report.json` next to the Markdown report:

```json
{
  "address": "<full address>",
  "report_date": "<YYYY-MM-DD>",
  "executive_summary": ["<line>", "…"],
  "property_facts": [{"fact": "…", "value": "…", "source": "<url>", "confidence": "verified|third-party|unverified"}],
  "incidents_exact_address": [{"date": "…", "description": "…", "source": "<url>"}],
  "public_records": [{"record": "…", "finding": "…", "source": "<url>", "confidence": "…"}],
  "must_verify": [{"item": "…", "how": "…"}],
  "unverified": ["…"]
}
```
