# WyattJY Skills

This repository is a T7 Shield export of Codex, Hermes, Claude, and project
skills collected from this machine, the migrated Windows Codex home, and a
broader T7 Shield skill scan.

The export preserves source snapshots instead of deduplicating them. Duplicate
skills across roots are expected because they show which environment each copy
came from.

## Contents

- `skills/hermes-home/` - from `/Volumes/T7 Shield/hermes/home/skills`
- `skills/mac-codex/` - from `/Users/jiangyu/.codex/skills`
- `skills/windows-codex-home/` - from `/Volumes/T7 Shield/codex_session_migration_20260515/windows_codex_home/skills`
- `skills/wyatt-agents/` - from `/Volumes/T7 Shield/Wyatt/.agents/skills`
- `skills/wyatt-claude/` - from `/Volumes/T7 Shield/Wyatt/.claude/skills`
- `skills/codex-downloads/` - from `/Volumes/T7 Shield/codex_downloads/skills`
- `skills/t7-shield-full/` - path-preserving export of the T7 scan recorded in `manifests/t7_candidate_skill_files_outside_export.txt`
- `claude-skills/` - Claude Code-ready mirror generated from the current Windows user-managed Codex skill roots

Current export summary:

- `927` `SKILL.md` files
- `526` unique skill directory names
- `7229` tracked candidate files before Git filtering
- about `1.2G` on the T7 Shield volume

High-signal recovered paths include:

- `skills/t7-shield-full/hermes/codex_agent_skills/sources/superpowers_skills/using-superpowers/`
- `skills/t7-shield-full/hermes/home/skills/using-superpowers/`
- `skills/t7-shield-full/Wyatt/HK_intership/.agent/skills/research-workflow/`
- `skills/t7-shield-full/Wyatt/HK_intership/.agent/skills/research-analysis-subagent/`
- `skills/t7-shield-full/hermes/hermes-agent/skills/`
- `skills/t7-shield-full/hermes/hermes-agent/optional-skills/`

## Manifests

- `manifests/source_roots.tsv` records the source path for each exported root.
- `manifests/skill_files.txt` lists every exported `SKILL.md`.
- `manifests/unique_skill_names.txt` lists unique skill directory names.
- `manifests/all_files.txt` lists exported files.
- `manifests/directories.txt` lists exported directories.
- `manifests/removed_sensitive_candidates.txt` lists excluded credential/config candidates.
- `manifests/secret_scan_strict.txt` records the strict post-cleanup scan output.
- `manifests/t7_candidate_skill_files_outside_export.txt` lists T7 skill files found outside this export repository.
- `manifests/t7_full_export_map.tsv` maps each T7 source skill directory to its exported target directory.

## Exclusions

The export excludes generated or risky files:

- `.git/`
- `.DS_Store`
- Apple resource fork files (`._*`)
- `node_modules/`
- `__pycache__/`
- `*.pyc`
- `.env`
- `settings.json*`

Do not commit API keys, session files, cookies, machine credentials, or local
settings into this repository.

## Restore Notes

To make a machine use one of these skill sets, copy the desired skill
directories into that machine's Codex skills root, usually:

```bash
~/.codex/skills
```

Keep this repository as the canonical backup on GitHub, and keep local runtime
or dependency installs on the T7 Shield unless explicitly changed later.
