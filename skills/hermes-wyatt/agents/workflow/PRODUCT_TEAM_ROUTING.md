# WyattJY Hermes Product Team Routing

This file defines the temporary subagent roster for product work. The five long-lived Hermes profiles stay small; product roles are invoked as Claude Code subagents or temporary Hermes workers when a task reaches the matching G0-G9 gate.

## Model Routing

| Work type | Provider | Model |
| --- | --- | --- |
| Architecture, product strategy, UI system design | AIHubMix | `claude-opus-4-7-think` |
| Small implementation, tests, docs, ops | AIHubMix | `deepseek-v4-pro` |
| UI draft image generation | CPA Lobewyatt | `gpt-image-2` |

## Subagent Roster

| Role | Claude Code agent file | Primary gates | Model |
| --- | --- | --- | --- |
| System architect | `/Users/jiangyu/.claude/agents/wyatt-system-architect.md` | G2, G6 | `claude-opus-4-7-think` |
| Product manager | `/Users/jiangyu/.claude/agents/wyatt-product-manager.md` | G1, G2, G8 | `claude-opus-4-7-think` |
| UI designer | `/Users/jiangyu/.claude/agents/wyatt-ui-designer.md` | G3, G4 | `claude-opus-4-7-think` |
| Frontend engineer | `/Users/jiangyu/.claude/agents/wyatt-frontend-engineer.md` | G5 | `deepseek-v4-pro` |
| Backend engineer | `/Users/jiangyu/.claude/agents/wyatt-backend-engineer.md` | G6 | `deepseek-v4-pro` |
| QA engineer | `/Users/jiangyu/.claude/agents/wyatt-qa-engineer.md` | G7, G8 | `deepseek-v4-pro` |
| Reviewer bot | `/Users/jiangyu/.claude/agents/wyatt-reviewer-bot.md` | G7, G9 | `deepseek-v4-pro` |
| DevOps release | `/Users/jiangyu/.claude/agents/wyatt-devops-release.md` | G9 | `deepseek-v4-pro` |
| Research analyst | `/Users/jiangyu/.claude/agents/wyatt-research-analyst.md` | Research routine | `deepseek-v4-pro` |
| Scholar | `/Users/jiangyu/.claude/agents/wyatt-scholar.md` | Paper deep read | `deepseek-v4-pro` |
| Memory archivist | `/Users/jiangyu/.claude/agents/wyatt-memory-archivist.md` | G0, closeout | `deepseek-v4-pro` |

## Product Flow

1. G0: `wyatt-memory-archivist` loads 0-3 relevant cases through `case-router`.
2. G1-G2: `wyatt-product-manager` and `wyatt-system-architect` write requirements, design, tasks, and test plan.
3. G3-G4: `wyatt-ui-designer` creates UI direction, image draft prompts, design tokens, and component specs.
4. G5-G6: `wyatt-frontend-engineer` and `wyatt-backend-engineer` implement approved slices.
5. G7: `wyatt-qa-engineer` and `wyatt-reviewer-bot` independently verify behavior, tests, and risk.
6. G8: `wyatt-product-manager` maps feedback to the exact gate that needs revision.
7. G9: `wyatt-devops-release` packages, documents, and verifies release or local launch.
8. Closeout: `wyatt-memory-archivist` archives final prompt, turning points, bugs, and reusable cases.

## Hard Rules

- Do not persist every subagent as a long-lived Hermes profile; these are task roles.
- Architecture/design work uses `claude-opus-4-7-think`; routine implementation uses `deepseek-v4-pro`.
- UI image drafts call `gpt-image-2` through the configured image provider.
- No agent writes secrets, Weixin tokens, `.env` contents, cookies, session files, or raw company data into memory or reports.
