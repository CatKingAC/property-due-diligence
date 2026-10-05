#!/usr/bin/env python3
"""Generate an empty due-diligence report scaffold from the template.

Usage:
    python3 report_scaffold.py "<address>" [out_dir] [--slug SLUG] [--force]

Writes <slug>-due-diligence-report.md into out_dir (default: current dir)
with every template section present and TODO markers. Also writes the
optional JSON sidecar skeleton.

--slug overrides the auto-derived slug. Pass the slug from
normalize_address.py so the report path is predictable.
--force allows overwriting existing report files; without it the script
refuses to clobber an existing report (a filled-in report is easy to
destroy by accident).

Requires Python 3.8+.
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
| Zoning / land use | TODO | | |
| Year built | TODO | | |
| Living area (above grade) | TODO | | |
| Lot size | TODO | | |
| Bedrooms / bathrooms | TODO | | |
| Parking | TODO | | |
| HOA | TODO | | |
| Parcel / APN | TODO | | |
| Owner of record | TODO | | |
| Listing agent / brokerage | TODO | | |
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

### 3b. Immediate area (<=0.5 mi)

- SpotCrime / CrimeMapping: TODO
- CrimeGrade (city/neighborhood scope only): TODO

---

## 4. Public Records

| Record | Finding | Source | Confidence |
|--------|---------|--------|------------|
| FEMA flood zone | TODO | | |
| Tax delinquency | TODO | | |
| Liens / foreclosure | TODO | | |
| Sex-offender registry (<=1 mi) | TODO | | |
| Building permits | TODO | | |

---

## 5. Neighborhood & Schools

- TODO (3-5 sourced bullets; assigned schools with district source)

---

## 6. Must-Verify Checklist (manual, before closing)

1. TODO — what to verify + exactly where/how (office, phone, URL)
2. Confirm the listing is legitimate — contact the listing brokerage directly; beware rental/owner-impersonation scams
3. Flood determination: FEMA Map Service Center (https://msc.fema.gov/portal/home) or insurer/title company
4. Home inspection (+ permits check with city) — especially for pre-1978 homes
5. Title search via title company (liens, easements)

---

## 7. Unverified Items

- TODO (everything not confirmed, and why)

---

## 8. Sources

1. TODO (every URL actually read, in order of first use)
"""


def parse_args(argv):
    """Tiny arg parser: report_scaffold.py "<address>" [out_dir] [--slug S] [--force]."""
    address = None
    out_dir = "."
    slug = None
    force = False
    positional = []
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--force":
            force = True
        elif a == "--slug":
            i += 1
            if i >= len(argv) or not argv[i].strip():
                return None, "--slug needs a value"
            slug = slugify(argv[i])
            if not slug:
                return None, "--slug produced an empty slug"
        elif a.startswith("--"):
            return None, f"unknown option {a}"
        else:
            positional.append(a)
        i += 1
    if positional:
        address = " ".join(positional[0].split())
    if len(positional) > 1:
        out_dir = positional[1]
    if not address:
        return None, 'usage: report_scaffold.py "<address>" [out_dir] [--slug SLUG] [--force]'
    return {"address": address, "out_dir": out_dir, "slug": slug, "force": force}, None


def main():
    opts, err = parse_args(sys.argv)
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    address = opts["address"]
    out_dir = opts["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    slug = opts["slug"] or slugify(address)
    if not slug:
        print("error: address produced an empty slug", file=sys.stderr)
        sys.exit(1)

    date = datetime.date.today().isoformat()
    # NOTE: plain .replace(), not str.format() — an address containing
    # braces (e.g. "123 {Main} St") must not crash the script.
    body = TEMPLATE.replace("{address}", address).replace("{date}", date)

    md_path = os.path.join(out_dir, f"{slug}-due-diligence-report.md")
    json_path = os.path.join(out_dir, f"{slug}-due-diligence-report.json")
    if not opts["force"]:
        existing = [p for p in (md_path, json_path) if os.path.exists(p)]
        if existing:
            print("error: refusing to overwrite existing report file(s):", file=sys.stderr)
            for p in existing:
                print(f"  {p}", file=sys.stderr)
            print("re-run with --force to overwrite.", file=sys.stderr)
            sys.exit(1)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(body)

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
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sidecar, f, indent=2)

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
