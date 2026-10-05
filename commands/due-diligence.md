---
name: "due-diligence"
description: "Run buyer due diligence on a US residential address and produce a source-cited report."
---

# /due-diligence

Run the `property_due_diligence` skill on the address given as arguments.

Usage: `/due-diligence 123 Main St, Springfield, IL 62704`

Steps:
1. Take the full argument string as the target address. If empty, ask the user for it.
2. Follow `skills/property-due-diligence/SKILL.md` exactly: normalize → property facts → incident/crime history → public records → neighborhood → report.
3. Write the report to `./<address-slug>-due-diligence-report.md` (or a path the user names) and reply with the file path plus a 5–8 line summary of key findings and must-verify items.
