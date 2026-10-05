#!/usr/bin/env python3
"""Generate an empty due-diligence report scaffold from the template.

Usage:
    python3 report_scaffold.py "123 Main St, Springfield, IL 62704" [out_dir]

Writes <slug>-due-diligence-report.md into out_dir (default: current dir)
with every template section present and TODO markers. Also writes the
optional JSON sidecar skeleton.
"""

import datetime
import json
import os
import re
import sys


def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", text)


TEMPLATE = """# Property Due-Diligence Report: {address}

- Report date: {date}
- Prepared for: home-buyer due diligence (read-only public-records research)
- Scope: US residential, v1. Not a substitute for title search, home
  inspection, or legal advice.

---

## 1. Executive Summary

<!-- 5-8 lines, findings only: property-type verdict, price vs assessment,
     red flags, count of must-verify items. -->
- TODO

---

## 2. Property Facts

| Fact | Value | Source | Confidence |
|------|-------|--------|------------|
| Property type | TODO | | |
| Year built | TODO | | |
| Living area (above grade) | TODO | | |
| Lot size | TODO | | |
| Bedrooms / bathrooms | TODO | | |
| Parking | TODO | | |
| HOA | TODO | | |
| Parcel / APN | TODO | | |
| Owner of record | TODO | | |
| Current list price (MLS#) | TODO | | |
| Price history | TODO | | |
| Assessed value (year) | TODO | | |
| Annual property tax | TODO | | |
| Tax history | TODO (table) | | |

---

## 3. Incident & Crime History

### 3a. Exact address: {address}

Queries run:
<!-- list every query, e.g. `"123 Main St" "Springfield" murder` -->

- Result: TODO (none found — or one bullet per incident with date, facts, source URL)
- Note: absence of news coverage is not proof nothing happened.

### 3b. Immediate area (≤0.5 mi)

- SpotCrime / CrimeMapping: TODO
- CrimeGrade (city/neighborhood scope only): TODO

---

## 4. Public Records

| Record | Finding | Source | Confidence |
|--------|---------|--------|------------|
| FEMA flood zone | TODO | | |
| Tax delinquency | TODO | | |
| Liens / foreclosure | TODO | | |
| Sex-offender registry (≤1 mi) | TODO | | |
| Building permits | TODO | | |

---

## 5. Neighborhood & Schools

- TODO (3-5 sourced bullets; assigned schools with district source)

---

## 6. Must-Verify Checklist (manual, before closing)

1. TODO — what to verify + exactly where/how (office, phone, URL)
2. Flood determination: FEMA Map Service Center (https://msc.fema.gov/portal/home) or insurer/title company
3. Home inspection (+ permits check with city) — especially for pre-1978 homes
4. Title search via title company (liens, easements)

---

## 7. Unverified Items

- TODO (everything not confirmed, and why)

---

## 8. Sources

1. TODO (every URL actually read, in order of first use)
"""


def main():
    if len(sys.argv) < 2:
        print("usage: report_scaffold.py \"<address>\" [out_dir]", file=sys.stderr)
        sys.exit(1)
    address = " ".join(sys.argv[1].split())
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out_dir, exist_ok=True)

    slug = slugify(address)
    date = datetime.date.today().isoformat()
    md_path = os.path.join(out_dir, f"{slug}-due-diligence-report.md")
    with open(md_path, "w") as f:
        f.write(TEMPLATE.format(address=address, date=date))

    sidecar = {
        "address": address,
        "report_date": date,
        "executive_summary": [],
        "property_facts": [],
        "incidents_exact_address": [],
        "public_records": [],
        "must_verify": [],
        "unverified": [],
    }
    json_path = os.path.join(out_dir, f"{slug}-due-diligence-report.json")
    with open(json_path, "w") as f:
        json.dump(sidecar, f, indent=2)

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
