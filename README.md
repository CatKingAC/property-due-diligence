# 🏠 property-due-diligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-open_standard-blue)](https://agentskills.io)

**English** · [中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md)

> A universal agent skill for **buyer due diligence on a US residential
> address**. Give it an address — it researches property facts,
> incident & crime history at the exact address, public records (flood
> zone, tax, liens, permits, sex-offender registry), and
> neighborhood/schools — then produces a formal, source-cited buyer
> report where every material fact is labeled
> `verified` / `third-party` / `unverified`.

Built from a real research workflow. **It verifies; it doesn't guess.**

---

## 🤖 Works with

| Agent | How to install |
|-------|----------------|
| **Claude Code** | `/plugin marketplace add CatKingAC/property-due-diligence`, then `/plugin install property-due-diligence@property-due-diligence` |
| **Codex CLI** | Copy `skills/property-due-diligence/` to `~/.codex/skills/` (all projects) or `.codex/skills/` (one project) |
| **Any Agent Skills-compatible agent** | Point the agent at `skills/property-due-diligence/` (or the cross-tool `.agents/skills/` convention) — needs web search, page fetch, and Python 3.8+ (stdlib only) |
| **Anything else** | Paste `skills/property-due-diligence/SKILL.md` into context and ask the agent to follow it |

> The `commands/` directory (`/due-diligence`) is Claude Code-specific.
> On other agents, trigger the skill with plain language — the trigger
> phrases are in the skill's frontmatter description.

---

## 🚀 Usage

```text
/due-diligence 123 Main St, Springfield, IL 62704
```

Or in plain language — ask your agent to *"run due diligence on
\<address\>"*.

You get:

- 📄 A full report at `./<address-slug>-due-diligence-report.md` (or a path you name)
- 💬 A 5–8 line summary in chat with key findings and must-verify items
- 🗂️ An optional machine-readable JSON sidecar

See [`examples/sample-report.md`](examples/sample-report.md) for the
(fictional) output shape.

---

## 🔍 What it checks

| # | Area | Sources |
|---|------|---------|
| 1 | **Property facts** — type, year built, sqft, lot, beds/baths, owner, assessed value + tax history, sale history, parcel/APN | County assessor first, cross-checked against 2+ MLS aggregators (Zillow, Realtor.com, Redfin, Homes.com) |
| 2 | **Incident & crime history** — exact-address news search (murder / shooting / fire / incident), local paper archives, block-level crime maps | Web/news search, SpotCrime, CrimeMapping, CrimeGrade |
| 3 | **Public records** — FEMA flood zone, tax delinquency, liens/foreclosure, sex-offender registry, building permits | FEMA Map Service Center, county tax collector, recorder of deeds, NSOPW + state registry, city permit portal |
| 4 | **Neighborhood & schools** — assigned schools, brief sourced area notes | School district site, GreatSchools, NCES, Census QuickFacts |

"None found" is stated explicitly — absence of news is never presented
as proof of safety.

---

## ⚠️ Scope and limits (v1)

- **US residential addresses only.** Public-records systems vary by
  state/county; the skill finds the right county portal per address.
- **Read-only research.** It never contacts owners/agents/neighbors and
  never creates accounts to bypass paywalls.
- **Not a substitute** for a title search, professional home inspection,
  or legal advice. The report's Must-Verify Checklist tells the buyer
  what to confirm by hand before closing.
- Some records live behind interactive maps or logins the agent can't
  always read — those become explicit `unverified` items with manual
  steps, not guesses.

---

## 📁 Repository layout

```text
.claude-plugin/
  plugin.json            # Claude Code plugin manifest
  marketplace.json       # self-hosted marketplace (this repo lists itself)
skills/property-due-diligence/
  SKILL.md               # the 5-step workflow (agent-neutral)
  references/
    data-sources.md      # where to check what, per category
    report-template.md   # formalized output template (+ JSON sidecar)
    verification-rules.md# verify-don't-guess rules, confidence labels
  scripts/
    normalize_address.py # address parsing/validation (stdlib only)
    report_scaffold.py   # report + JSON skeleton generator
commands/due-diligence.md# /due-diligence slash command (Claude Code only)
examples/sample-report.md# fictional example output
REVIEW_LOG.md            # design + code + verification review history
```

---

## 📜 License

MIT — see [LICENSE](LICENSE).
