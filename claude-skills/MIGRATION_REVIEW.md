# Claude Skills Migration Review

Generated: 2026-05-27T20:21:28

## Counts

- Codex skill source `SKILL.md` files: **69**
- Claude Code target skills generated under `claude-skills/skills`: **84**
- Codex-to-Claude migrated skill parity: **69/69**
- Hermes-local-to-Claude skill parity: **14/14**
- Claude-native Hermes product-team entrypoint: **1**
- Claude-native / Hermes role agent markdown files copied under `claude-skills/agents`: **13**

This makes the migrated Codex-to-Claude skill count equal for the current local source set while also installing the local Hermes skill layer needed by Wyatt's product-team workflow. Existing Claude marketplace/plugin skills under `~/.claude/plugins/...` are not counted in this parity number because they are upstream plugin assets, not Jiangyu's migrated Codex skill set.

## Claude Code Format Rules Applied

- Each skill is a directory under `claude-skills/skills/<kebab-case-name>/SKILL.md`.
- Each `SKILL.md` starts at byte 1 with YAML frontmatter.
- Frontmatter has normalized `name` and single-line `description`.
- Descriptions are capped below 1024 characters and angle brackets are removed from generated frontmatter.
- Codex `agents/openai.yaml`, `.env`, `settings.json*`, AppleDouble sidecars, bytecode, and caches are excluded; false-positive token examples were reviewed and retained.
- Support files such as `scripts/`, `references/`, `templates/`, `examples/`, and `assets/` are copied when safe.

## Runtime Review

Some skills are format-compatible but still depend on local runtime tools or Claude-side equivalents:

- Claude Code model route: local Claude Code and all Wyatt/Hermes Claude agents are configured for CPA-backed Xiaomi MiMo, model `mimo-v2.5-pro`.
- Hermes product manager / product team: supported via migrated `hermes-wyatt-workflow`, installed `$wyatt-product-team`, `claude-skills/agents/wyatt-product-manager.md`, `PRODUCT_TEAM_ROUTING.md`, and local `/Users/jiangyu/.hermes-wyatt` wrappers.
- Note generation: `audio-screenshot-course-notes` is migrated and depends on local media assets, ASR tooling, image access, and Markdown asset validation.
- Word/DOCX writing: `jiangyu-word-report-style` is migrated and preserves the style contract; render verification needs a Claude-side Word/LibreOffice/Pandoc path rather than Codex Documents runtime.
- Daily summaries: `lark-workflow-standup-report` is migrated and requires `lark-cli` plus Feishu calendar/task auth.
- Meeting summaries: `lark-workflow-meeting-summary` is migrated and requires `lark-cli` plus vc/minutes/drive/docs scopes as needed.

## Files

- `manifests/summary.json` machine-readable count summary.
- `manifests/source_skills.tsv` one row per migrated source skill.
- `manifests/format_review.tsv` per-skill format/runtime review.
- `manifests/agents.tsv` copied Claude/Hermes role agents.
- `manifests/runtime_verification.tsv` command evidence for the current local verification pass.
- `manifests/secret_scan_exclusions.json` records secret-like exclusions; currently empty after manual false-positive review.

## Verification Status

- Installed into `~/.claude/skills`: **84** skill directories and **84** `SKILL.md` files.
- Local frontmatter validator: **0** issues for both `claude-skills/skills` and `~/.claude/skills`.
- Claude Code plugin validation: `claude-real plugins validate claude-skills` passes.
- Claude Code route smoke test: local settings and agents point to CPA-backed Xiaomi MiMo `mimo-v2.5-pro`, but the live CPA call currently returns `auth_unavailable` for that model on the CPA server.
- Hermes/Wyatt workflow validation: `validate_wyatt_workflow.py` passes with `PYTHONPYCACHEPREFIX=/private/tmp/hermes_pycache`; `test_wyatt_workflow.py -v` passes 5 tests.
- GitHub publish uses the `codex/claude-skills-migration` branch and is reconciled against `origin/main` before merge.
- Lark and Word render flows remain dependency-gated in the current shell: `lark-cli`, `pandoc`, and `soffice/libreoffice` are not on `PATH`.

## Dependency Bootstrap

- Lark daily summary and meeting summary flows need `lark-cli` plus user auth for calendar/task and vc/drive/docs scopes before live Feishu calls can be verified.
- Word report generation can use the migrated `jiangyu-word-report-style` script and `python-docx`; visual/render verification needs `pandoc` and LibreOffice or a compatible `soffice` command.
- Audio/screenshot note generation should use a T7-hosted ASR virtual environment and install the media/image packages required by `audio-screenshot-course-notes`.
