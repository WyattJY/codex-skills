# CLAUDE.md

Runtime skill mirror for Claude Code. This repo is not the source of truth; the three source roots are.

## Source Roots

Priority order:

1. `H:\T7\codex_skills\skills` - active Wyatt skills (`h-t7-active`)
2. `C:\Users\18357\.codex\skills` - local Codex personal skills (`personal-codex`)
3. `C:\Users\18357\.agents\skills` - shared agent skills, including Lark (`agents`)

Duplicate names keep the first source. See `manifests/skipped_sources.tsv`.

## Key Commands

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-claude-skills.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\install-windows.ps1 -PruneUnmanaged
powershell -ExecutionPolicy Bypass -File .\scripts\validate-claude-skills.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\review-claude-skills.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\audit-storage.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\test-with-claude.ps1
```

## Storage Model

- `skills/` in this repo contains the H-drive Claude Code-ready mirror.
- `C:\Users\18357\.claude\skills\` contains junctions pointing to this repo.
- Edit source roots or rebuild this repo; do not edit the junction targets through `~/.claude\skills`.

## Safety

- Never commit API keys, cookies, `.env`, credentials, or session files.
- The build and review scripts exclude common credential file patterns, but manual review is still required before publishing.
- Keep `unique user-managed Codex skills == generated Claude skills == installed Claude skills`.
