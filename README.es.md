# 🏠 property-due-diligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-open_standard-blue)](https://agentskills.io)

[English](README.md) · [中文](README.zh-CN.md) · **Español** · [Français](README.fr.md)

> Una skill universal para agentes de IA dedicada a la **diligencia
> debida del comprador sobre una dirección residencial en EE. UU.**
> Dale una dirección — investigará los datos de la propiedad, el
> historial de incidentes y delitos en esa dirección exacta, los
> registros públicos (zona de inundación, impuestos atrasados,
> gravámenes, permisos de construcción, registro de delincuentes
> sexuales) y el vecindario con sus escuelas — y producirá un informe
> formal para el comprador, con fuentes citadas, donde cada dato
> relevante lleva la etiqueta `verified` (verificado) /
> `third-party` (de terceros) / `unverified` (no verificado).

Nace de un flujo de investigación real, probado en la práctica.
**Verifica; no adivina.**

---

## 🤖 Compatibilidad

| Agente | Instalación |
|--------|-------------|
| **Claude Code** | `/plugin marketplace add CatKingAC/property-due-diligence` y luego `/plugin install property-due-diligence@property-due-diligence` |
| **Codex CLI** | Copia `skills/property-due-diligence/` a `~/.codex/skills/` (todos los proyectos) o a `.codex/skills/` (un proyecto) |
| **Cualquier agente compatible con Agent Skills** | Apunta al agente a `skills/property-due-diligence/` (o la convención multi-herramienta `.agents/skills/`) — necesita búsqueda web, lectura de páginas y Python 3.8+ (solo biblioteca estándar) |
| **Cualquier otro** | Pega el contenido de `skills/property-due-diligence/SKILL.md` en el contexto y pide al agente que lo siga |

> El directorio `commands/` (`/due-diligence`) es exclusivo de
> Claude Code. En otros agentes, activa la skill con lenguaje natural —
> las frases de activación están en la descripción del frontmatter de
> la skill.

---

## 🚀 Uso

```text
/due-diligence 123 Main St, Springfield, IL 62704
```

O en lenguaje natural — pídele a tu agente que *"investigue esta
dirección"* (*"run due diligence on \<address\>"*).

Obtendrás:

- 📄 Un informe completo en `./<address-slug>-due-diligence-report.md` (o la ruta que elijas)
- 💬 Un resumen de 5–8 líneas en el chat, con los hallazgos clave y los puntos por verificar
- 🗂️ Un archivo JSON opcional, legible por máquinas

Mira [`examples/sample-report.md`](examples/sample-report.md) para ver
la forma del resultado (ejemplo ficticio).

---

## 🔍 Qué verifica

| # | Área | Fuentes |
|---|------|---------|
| 1 | **Datos de la propiedad** — tipo, año de construcción, superficie, lote, habitaciones/baños, propietario, valor catastral + historial fiscal, historial de ventas, parcela/APN | Primero el tasador del condado (*assessor*), contrastado con 2+ agregadores MLS (Zillow, Realtor.com, Redfin, Homes.com) |
| 2 | **Historial de incidentes y delitos** — búsqueda de noticias en la dirección exacta (homicidio / tiroteo / incendio / incidente), archivo del periódico local, mapas de delitos por manzana | Búsqueda web y de noticias, SpotCrime, CrimeMapping, CrimeGrade |
| 3 | **Registros públicos** — zona de inundación FEMA, impuestos atrasados, gravámenes/ejecuciones hipotecarias, registro de delincuentes sexuales, permisos de construcción | Centro de Mapas de FEMA, recaudador de impuestos del condado, registro de escrituras, NSOPW + registro estatal, portal municipal de permisos |
| 4 | **Vecindario y escuelas** — escuelas asignadas, notas breves del área con fuentes | Sitio del distrito escolar, GreatSchools, NCES, QuickFacts del Censo |

Si no se encuentra nada, se dice explícitamente — la ausencia de
noticias nunca se presenta como prueba de seguridad.

---

## ⚠️ Alcance y límites (v1)

- **Solo direcciones residenciales en EE. UU.** Los sistemas de
  registros públicos varían por estado y condado; la skill localiza el
  portal del condado correspondiente a cada dirección.
- **Investigación de solo lectura.** Nunca contacta a propietarios,
  agentes ni vecinos, y nunca crea cuentas para saltar muros de pago.
- **No sustituye** una búsqueda de títulos (*title search*), una
  inspección profesional de la vivienda ni el asesoramiento legal. La
  lista de verificación del informe indica al comprador qué debe
  confirmar en persona antes del cierre.
- Algunos registros están tras mapas interactivos o inicios de sesión
  que el agente no siempre puede leer — esos se marcan como
  `unverified` (no verificado) con los pasos manuales, nunca se
  adivinan.

---

## 📁 Estructura del repositorio

```text
.claude-plugin/
  plugin.json            # Manifiesto del plugin de Claude Code
  marketplace.json       # Marketplace autoalojado (este repo se lista a sí mismo)
skills/property-due-diligence/
  SKILL.md               # El flujo de 5 pasos (independiente del agente)
  references/
    data-sources.md      # Dónde consultar qué, por categoría
    report-template.md   # Plantilla formal del informe (+ JSON adjunto)
    verification-rules.md# Reglas de verificación y etiquetas de confianza
  scripts/
    normalize_address.py # Análisis y validación de direcciones (solo stdlib)
    report_scaffold.py   # Generador del esqueleto del informe + JSON
commands/due-diligence.md# Comando /due-diligence (solo Claude Code)
examples/sample-report.md# Ejemplo de resultado (ficticio)
REVIEW_LOG.md            # Historial de revisiones (en inglés)
```

---

## 📜 Licencia

MIT — ver [LICENSE](LICENSE).
