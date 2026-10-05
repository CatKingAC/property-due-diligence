# 🏠 property-due-diligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-open_standard-blue)](https://agentskills.io)

[English](README.md) · [中文](README.zh-CN.md) · [Español](README.es.md) · **Français**

> Une skill universelle pour agents IA, dédiée à la **diligence
> raisonnable de l'acheteur sur une adresse résidentielle aux
> États-Unis**. Donnez-lui une adresse — elle recherchera les
> caractéristiques du bien, l'historique des incidents et de la
> criminalité à cette adresse exacte, les registres publics (zone
> inondable, arriérés d'impôts, privilèges, permis de construire,
> registre des délinquants sexuels) ainsi que le quartier et ses
> écoles — puis produira un rapport d'acheteur formel, avec sources
> citées, où chaque fait important porte l'étiquette `verified`
> (vérifié) / `third-party` (source tierce) / `unverified`
> (non vérifié).

Issue d'un véritable flux de recherche, testé en pratique. **Elle
vérifie ; elle ne devine jamais.**

---

## 🤖 Compatibilité

| Agent | Installation |
|-------|--------------|
| **Claude Code** | `/plugin marketplace add CatKingAC/property-due-diligence`, puis `/plugin install property-due-diligence@property-due-diligence` |
| **Codex CLI** | Copiez `skills/property-due-diligence/` vers `~/.codex/skills/` (tous les projets) ou `.codex/skills/` (un projet) |
| **Tout agent compatible Agent Skills** | Pointez l'agent vers `skills/property-due-diligence/` (ou la convention multi-outils `.agents/skills/`) — requiert la recherche web, la lecture de pages et Python 3.8+ (bibliothèque standard uniquement) |
| **Autre** | Collez le contenu de `skills/property-due-diligence/SKILL.md` dans le contexte et demandez à l'agent de le suivre |

> Le répertoire `commands/` (`/due-diligence`) est propre à
> Claude Code. Sur les autres agents, déclenchez la skill en langage
> naturel — les phrases de déclenchement figurent dans la description
> du frontmatter de la skill.

---

## 🚀 Utilisation

```text
/due-diligence 123 Main St, Springfield, IL 62704
```

Ou en langage naturel — demandez à votre agent de *« faire la
diligence raisonnable sur \<adresse\> »* (*« run due diligence on
\<address\> »*).

Vous obtiendrez :

- 📄 Un rapport complet dans `./<address-slug>-due-diligence-report.md` (ou le chemin de votre choix)
- 💬 Un résumé de 5 à 8 lignes dans le chat, avec les points clés et les vérifications restantes
- 🗂️ Un fichier JSON facultatif, exploitable par machine

Voir [`examples/sample-report.md`](examples/sample-report.md) pour la
forme du résultat (exemple fictif).

---

## 🔍 Ce qui est vérifié

| # | Domaine | Sources |
|---|---------|---------|
| 1 | **Caractéristiques du bien** — type, année de construction, surface, terrain, chambres/salles de bain, propriétaire, valeur cadastrale + historique fiscal, historique des ventes, parcelle/APN | D'abord l'évaluateur du comté (*assessor*), recoupé avec 2+ agrégateurs MLS (Zillow, Realtor.com, Redfin, Homes.com) |
| 2 | **Historique des incidents et de la criminalité** — recherche d'actualités à l'adresse exacte (homicide / fusillade / incendie / incident), archives du journal local, cartes de criminalité par pâté de maisons | Recherche web et d'actualités, SpotCrime, CrimeMapping, CrimeGrade |
| 3 | **Registres publics** — zone inondable FEMA, arriérés d'impôts, privilèges/saisies, registre des délinquants sexuels, permis de construire | Centre cartographique de la FEMA, percepteur du comté, bureau des hypothèques, NSOPW + registre de l'État, portail municipal des permis |
| 4 | **Quartier et écoles** — écoles de secteur, brèves notes sourcées sur le quartier | Site du district scolaire, GreatSchools, NCES, QuickFacts du recensement |

« Aucun résultat » est indiqué explicitement — l'absence de couverture
médiatique n'est jamais présentée comme une preuve de sécurité.

---

## ⚠️ Portée et limites (v1)

- **Adresses résidentielles américaines uniquement.** Les systèmes de
  registres publics varient selon l'État et le comté ; la skill trouve
  le portail du comté correspondant à chaque adresse.
- **Recherche en lecture seule.** Elle ne contacte jamais les
  propriétaires, agents ou voisins, et ne crée jamais de comptes pour
  contourner les péages.
- **Ne remplace ni** une recherche de titres (*title search*), ni une
  inspection professionnelle, ni un avis juridique. La liste de
  vérifications du rapport indique à l'acheteur ce qu'il doit confirmer
  lui-même avant la signature.
- Certains registres se cachent derrière des cartes interactives ou
  des connexions que l'agent ne peut pas toujours lire — ils deviennent
  alors des éléments `unverified` (non vérifié) explicites, avec la
  marche à suivre manuelle. Jamais de devinettes.

---

## 📁 Structure du dépôt

```text
.claude-plugin/
  plugin.json            # Manifeste du plugin Claude Code
  marketplace.json       # Marketplace auto-hébergé (ce dépôt se liste lui-même)
skills/property-due-diligence/
  SKILL.md               # Le flux en 5 étapes (indépendant de l'agent)
  references/
    data-sources.md      # Où chercher quoi, par catégorie
    report-template.md   # Modèle de rapport formel (+ JSON joint)
    verification-rules.md# Règles de vérification et étiquettes de confiance
  scripts/
    normalize_address.py # Analyse et validation d'adresse (stdlib uniquement)
    report_scaffold.py   # Générateur de squelette de rapport + JSON
commands/due-diligence.md# Commande /due-diligence (Claude Code uniquement)
examples/sample-report.md# Exemple de résultat (fictif)
REVIEW_LOG.md            # Historique des revues (en anglais)
```

---

## 📜 Licence

MIT — voir [LICENSE](LICENSE).
