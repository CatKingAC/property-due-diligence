#!/usr/bin/env python3
"""Normalize a US street address for due-diligence research.

Usage:
    python3 normalize_address.py "123 Main St, Springfield, IL 62704"

Output (JSON):
    {
      "canonical": "123 Main St, Springfield, IL 62704",
      "street": "123 Main St",
      "city": "Springfield",
      "state": "IL",
      "zip": "62704",
      "slug": "123-main-st-springfield-il",
      "search_variants": ["\"123 Main St\" \"Springfield\"", ...],
      "warnings": [...]
    }

Exits non-zero with an error JSON when the address is not a plausible
US address (bad state code, bad ZIP, missing street number).
"""

import json
import re
import sys

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI",
    "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN",
    "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
    "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
    "WV", "WI", "WY",
    # US territories (have US ZIP codes; assessor coverage varies)
    "PR", "GU", "VI", "AS", "MP",
}

# Common street suffix abbreviations -> expansion (for search variants only)
SUFFIX_EXPAND = {
    "St": "Street", "Ave": "Avenue", "Blvd": "Boulevard", "Dr": "Drive",
    "Rd": "Road", "Ln": "Lane", "Ct": "Court", "Pl": "Place", "Pkwy": "Parkway",
    "Ter": "Terrace", "Way": "Way", "Cir": "Circle",
}


def fail(msg):
    print(json.dumps({"error": msg}, indent=2))
    sys.exit(1)


def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", text)


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        fail("usage: normalize_address.py \"<street>, <city>, <ST> <zip>\"")
    raw = " ".join(sys.argv[1].split())
    # Strip control / bidi-override characters: they can corrupt report
    # headings and terminal output if they ride in on a pasted address.
    raw = re.sub(r"[\x00-\x1f\x7f-\u009f\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", raw)
    raw = " ".join(raw.split())
    if not raw:
        fail("empty address")

    # Split into comma-separated parts; last part holds state + zip.
    # Empty segments (e.g. "St,, Springfield") are dropped so they don't
    # leak stray commas into the canonical form.
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if len(parts) < 3:
        fail("address must look like: <street>, <city>, <ST> <zip>")

    street = ", ".join(parts[:-2])
    city = parts[-2]
    tail = parts[-1]

    m = re.fullmatch(r"([A-Za-z]{2})\s+(\d{5})(?:-\d{4})?", tail)
    if not m:
        fail(f"could not parse state + ZIP from {tail!r} (expected '<ST> <ZIP>', e.g. 'IL 62704)")
    state, zip_code = m.group(1).upper(), m.group(2)
    if state not in US_STATES:
        fail(f"{state!r} is not a US state code")

    warnings = []
    if not re.match(r"^\d+[A-Za-z]?\s+\S", street):
        warnings.append("street does not start with a house number; results may be unreliable")
    if not city:
        warnings.append("city is empty")

    canonical = f"{street}, {city}, {state} {zip_code}"
    quoted = f'"{street}" "{city}"'
    variants = [quoted]
    # Add a variant with expanded street suffix (catches listings that spell it out)
    tokens = street.split()
    if tokens and tokens[-1].rstrip(".") in SUFFIX_EXPAND:
        expanded = " ".join(tokens[:-1] + [SUFFIX_EXPAND[tokens[-1].rstrip(".")]])
        variants.append(f'"{expanded}" "{city}"')

    print(json.dumps({
        "canonical": canonical,
        "street": street,
        "city": city,
        "state": state,
        "zip": zip_code,
        "slug": slugify(f"{street} {city} {state}"),
        "search_variants": variants,
        "warnings": warnings,
    }, indent=2))


if __name__ == "__main__":
    main()
