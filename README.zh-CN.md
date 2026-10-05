# 🏠 property-due-diligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-open_standard-blue)](https://agentskills.io)

[English](README.md) · **中文** · [Español](README.es.md) · [Français](README.fr.md)

> 通用型 AI Agent Skill，专做**美国住宅地址的买房尽职调查**。给它一个地址——它会查房产事实、该地址精确位置的事件与犯罪记录、公共记录（洪水区、欠税、留置权、建筑许可、性犯罪者登记），以及周边社区与学区——最后生成一份正式的、有来源标注的买家报告，每个关键事实都标明
> `verified`（已核实） / `third-party`（第三方） / `unverified`（未核实）。

源自一套真实跑通过的研究流程。**只核实，不瞎猜。**

---

## 🤖 适用平台

| Agent | 安装方式 |
|-------|----------|
| **Claude Code** | `/plugin marketplace add CatKingAC/property-due-diligence`，然后 `/plugin install property-due-diligence@property-due-diligence` |
| **Codex CLI** | 把 `skills/property-due-diligence/` 复制到 `~/.codex/skills/`（全局）或 `.codex/skills/`（单个项目） |
| **任何兼容 Agent Skills 的 Agent** | 把 `skills/property-due-diligence/` 指给 Agent（或跨工具的 `.agents/skills/` 规范）——需要网页搜索、页面抓取和 Python 3.8+（仅标准库） |
| **其他** | 把 `skills/property-due-diligence/SKILL.md` 的内容贴进上下文，让 Agent 照着执行 |

> `commands/` 目录（`/due-diligence`）是 Claude Code 专属的。在其他
> Agent 上用自然语言触发即可——触发语写在 skill frontmatter 的
> description 里。

---

## 🚀 用法

```text
/due-diligence 123 Main St, Springfield, IL 62704
```

或者直接用自然语言——让你的 Agent *"对 \<地址\> 做一次尽职调查"*。

你会得到：

- 📄 完整报告：`./<address-slug>-due-diligence-report.md`（可指定路径）
- 💬 聊天里 5–8 行摘要：关键发现 + 待核实事项
- 🗂️ 可选的机器可读 JSON 附件

输出长什么样，看 [`examples/sample-report.md`](examples/sample-report.md)（虚构示例）。

---

## 🔍 查什么

| # | 方面 | 数据来源 |
|---|------|----------|
| 1 | **房产事实**——类型、建造年份、面积、地块、卧卫、业主、评估价+税史、成交史、地块编号 APN | 先查县评估官（assessor），再用 2 个以上 MLS 聚合站交叉验证（Zillow、Realtor.com、Redfin、Homes.com） |
| 2 | **事件与犯罪记录**——精确地址的新闻搜索（凶杀/枪击/火灾/治安事件）、本地报纸档案、街区级犯罪地图 | 网页/新闻搜索、SpotCrime、CrimeMapping、CrimeGrade |
| 3 | **公共记录**——FEMA 洪水区、欠税、留置权/法拍、性犯罪者登记、建筑许可 | FEMA 地图服务中心、县税务官、契约登记处、NSOPW + 各州登记库、市建筑许可门户 |
| 4 | **社区与学区**——对口学校、简要的社区情况（有来源） | 学区官网、GreatSchools、NCES、人口普查 QuickFacts |

查不到就明确写"未发现"——没搜到新闻不等于证明安全，这句话会写进报告。

---

## ⚠️ 范围与限制（v1）

- **仅限美国住宅地址。**各州各县的公共记录系统不一样，skill 会按地址找到对应的县级门户。
- **只读研究。**绝不联系业主/中介/邻居，也绝不注册账号绕过付费墙。
- **不能替代**产权调查（title search）、专业验房或法律意见。报告里的"待核实清单"会告诉买家过户前要亲手确认什么。
- 有些记录藏在交互式地图或登录墙后面，Agent 不一定读得到——这些会标成明确的 `unverified`（未核实）并附上人工查询步骤，绝不靠猜。

---

## 📁 目录结构

```text
.claude-plugin/
  plugin.json            # Claude Code 插件清单
  marketplace.json       # 自托管 marketplace（本 repo 自己收录自己）
skills/property-due-diligence/
  SKILL.md               # 五步工作流（与具体 Agent 无关）
  references/
    data-sources.md      # 去哪查什么：按类别列的数据源手册
    report-template.md    # 正式报告模板（含 JSON 附件格式）
    verification-rules.md# 核实铁律：verify-don't-guess 与置信度标签
  scripts/
    normalize_address.py # 地址解析与校验（仅标准库）
    report_scaffold.py   # 报告 + JSON 骨架生成器
commands/due-diligence.md# /due-diligence 快捷命令（仅 Claude Code）
examples/sample-report.md# 虚构示例输出
REVIEW_LOG.md            # 设计、代码与核实审查历史（英文）
```

---

## 📜 许可证

MIT — 见 [LICENSE](LICENSE)。
