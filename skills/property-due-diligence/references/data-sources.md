# Data Sources: Where to Check What

US-only (v1). Public-records systems vary by **state and county** — when a
county-specific portal is needed, find it via the NETR Online directory
(§1) or a targeted search; never invent a county URL.

Some sites rate-limit or block automated fetching (you may see 403s or
timeouts on census.gov, crimegrade.org, or msc.fema.gov). That does not
make the source invalid — record the failed attempt, and fall back to the
manual steps given in each section.

Legend for each source: **O** = official/primary, **T** = third-party
aggregator · **$** free / paid / freemium · login needed? · text-readable
vs interactive (with fallback when interactive).

## 1. Property facts, assessed value, tax history

- **County Assessor / Property Appraiser / Tax Assessor** — **O** · $ free ·
  usually no login · usually text-readable.
  How to find: https://publicrecords.netronline.com/ → state → county →
  "Assessor". Or search `"[county] [state] property assessor parcel search"`.
  Many counties run on qpublic.net subdomains. Record: property type,
  zoning/land-use, year built, living area, lot size, parcel/APN, owner of
  record, assessed value, appraisal history.
- **County GIS / parcel viewer** — **O** · $ free · interactive map.
  Usually linked from the assessor site; use it to visually confirm lot
  boundaries and neighboring land use. If unreadable, skip — the
  assessor's lot dimensions are the record of reference.
- **Zillow** (https://www.zillow.com) — **T** · $ free · no login ·
  text-readable. Search the full address; use "Price history" and "Tax
  history" sections. Cross-check, don't trust alone.
- **Realtor.com** (https://www.realtor.com) — **T** · same as Zillow.
- **Redfin** (https://www.redfin.com) — **T** · same as Zillow.
- **Homes.com** (https://www.homes.com) — **T** · same as Zillow; often has
  the most complete MLS remarks and tax-history tables.
- Rule: property type, price history, and tax history must be confirmed by
  the assessor **or** 2+ aggregators agreeing. One aggregator alone =
  `third-party`.

## 2. Ownership history, liens, deeds

- **County Register of Deeds / Recorder** — **O** · $ free–small fee ·
  often requires a free account · sometimes interactive only.
  Name varies by state: Register of Deeds (TN), County Recorder (CA),
  Clerk of Court (FL), Registry of Deeds (MA). Find via NETR (§1). Record grantor/grantee, sale dates, prices, lien
  filings. If registration-walled: mark `unverified`, give the buyer the
  exact lookup steps.
- Aggregator "ownership history" sections — **T** · treat as leads, not facts.

## 3. Incident & crime history at the exact address

- **Web/news search** — **O/T mix** · $ free.
  Queries (run all, with the street address in quotes):
  - `"<number> <street>" "<city>"` + `murder`
  - `"<number> <street>" "<city>"` + `shooting`
  - `"<number> <street>" "<city>"` + `fire`
  - `"<number> <street>" "<city>"` + `crime OR incident OR arrest`
  - Same set on the **news** vertical.
  - Local paper: search `"[city] newspaper"` archive for the address string.
  List every query you ran in the report (so "none found" is auditable).
- **SpotCrime** (https://spotcrime.com) — **T** · $ free · interactive map.
  Enter the address, set radius ≤ 0.5 mi, read the incident list. If the map
  is unreadable: `unverified` + manual steps for the buyer.
- **CrimeMapping** (https://www.crimemapping.com) — **T** · same handling
  as SpotCrime.
- **CrimeGrade** (https://crimegrade.org) — **T** · city/neighborhood grades
  ONLY. Never present as block-level fact; label the geographic scope.

## 4. Flood zone

- **FEMA Map Service Center** (https://msc.fema.gov/portal/home) — **O** ·
  $ free · interactive map. Search the address → open the FIRM panel →
  record the zone (e.g. X, AE, VE) and panel number/date. If unreadable:
  `unverified` + tell the buyer to request a flood determination from
  their insurer/title company (lenders require flood insurance in
  high-risk zones).

## 5. Property tax delinquency

- **County Trustee / Tax Collector** — **O** · $ free · usually
  text-readable. Search `"[county] [state] property tax search"`; look up
  by parcel/address; record paid/delinquent status per year.
- If an aggregator flags delinquency but the collector shows paid (or vice
  versa): report **both**, mark `unverified`, put the trustee's phone
  number (listed on the collector site) in Must-Verify Checklist.

## 6. Sex-offender registry (vicinity)

- **NSOPW national search** (https://www.nsopw.gov/) — **O** · $ free.
- **State registry** — **O** · $ free · often interactive. Search
  `"[state] sex offender registry address search"`. Record registrants
  within ~1 mi with distances as shown; if the tool is unreadable, give
  the buyer the exact URL + steps instead of guessing.

## 7. Building permits & code violations

- **City permit portal / code enforcement** — **O** · $ free · varies.
  Search `"[city] building permit search"`. Record major permits
  (additions, roof, electrical) with dates. If the portal needs
  interaction you can't complete: `unverified` + manual steps. Always
  recommend a professional home inspection for pre-1978 homes regardless.

## 8. Schools & neighborhood

- **School district site** (search `"[city] school district school finder"`)
  — **O** · assigned schools by address.
- **GreatSchools.org** — **T** · ratings/reviews; label as third-party.
- **NCES school search** (https://nces.ed.gov/ccd/schoolsearch/) — **O** ·
  enrollment/demographics.
- **Census QuickFacts** (https://www.census.gov/quickfacts/) — **O** ·
  city/county demographics. Brief only.

## Deliberately out of scope for v1 (with reasons)

- **Title search / title insurance** — requires a licensed title company;
  the skill lists it in Must-Verify Checklist instead.
- **Insurance claims history (CLUE report)** — only the current owner can
  pull it; listed in Must-Verify Checklist.
- **HOA docs / CC&Rs** — obtainable only via seller or HOA; listed in
  Must-Verify Checklist.
- **Environmental (EPA Superfund, underground tanks)** — public via
  https://www.epa.gov/superfund/search-superfund-sites-where-you-live but
  address-level interpretation needs expertise; noted as optional, not in
  the default template.
