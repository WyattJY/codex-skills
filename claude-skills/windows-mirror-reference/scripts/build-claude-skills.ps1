param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$ActiveSkillRoot = "H:\T7\codex_skills\skills",
  [string]$PersonalCodexSkillRoot = "C:\Users\18357\.codex\skills",
  [string]$AgentsSkillRoot = "C:\Users\18357\.agents\skills"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-FullPath([string]$Path) {
  if (Test-Path -LiteralPath $Path) {
    return (Resolve-Path -LiteralPath $Path).Path
  }
  return [System.IO.Path]::GetFullPath($Path)
}

function Assert-UnderRoot([string]$Path, [string]$Root) {
  $fullPath = Resolve-FullPath $Path
  $fullRoot = (Resolve-FullPath $Root).TrimEnd('\')
  if (-not $fullPath.StartsWith($fullRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to operate outside repository root: $fullPath"
  }
}

function Convert-ToClaudeText([string]$Text) {
  $out = $Text
  $out = $out -creplace "Codex", "Claude Code"
  $out = $out -replace "normal Claude Code browsing", "available Claude Code web/search tools"
  $out = $out -replace "Use this as the Claude Code entry skill", "Use this as the Claude Code entry skill"
  $out = $out -replace '\$research-workflow', "/research-workflow"
  $out = $out -replace '\$research-analysis-subagent', "/research-analysis-subagent"
  $out = $out -replace "CODEX_WYATT_RESEARCH_ROOT", "CLAUDE_WYATT_RESEARCH_ROOT or CODEX_WYATT_RESEARCH_ROOT"
  $out = $out -replace "CODEX_WYATT_MEMORY_HOME", "CLAUDE_WYATT_MEMORY_HOME or CODEX_WYATT_MEMORY_HOME"
  $out = $out -replace "CODEX_UI_IMAGE_API_KEY", "CLAUDE_UI_IMAGE_API_KEY or CODEX_UI_IMAGE_API_KEY"
  $out = $out -replace "CODEX_UI_IMAGE_BASE_URL", "CLAUDE_UI_IMAGE_BASE_URL or CODEX_UI_IMAGE_BASE_URL"
  $out = $out -replace "CODEX_UI_IMAGE_MODEL", "CLAUDE_UI_IMAGE_MODEL or CODEX_UI_IMAGE_MODEL"
  $out = $out -replace "CODEX_UI_IMAGE_ENV", "CLAUDE_UI_IMAGE_ENV or CODEX_UI_IMAGE_ENV"
  $out = $out -replace "documents:documents", "Claude Code document/DOCX tooling or a locally installed documents skill"
  return $out
}

function Convert-SkillPaths([string]$Text, [string]$SkillName) {
  $out = $Text
  $out = $out.Replace("H:\T7\codex_skills\skills\$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("H:/T7/codex_skills/skills/$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("C:\Users\18357\.codex\skills\$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("C:/Users/18357/.codex/skills/$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("C:\Users\18357\.agents\skills\$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("C:/Users/18357/.agents/skills/$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("~/.codex/skills/$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("~/.agents/skills/$SkillName", '${CLAUDE_SKILL_DIR}')
  $out = $out.Replace("C:\Users\18357\.codex\skills", "C:\Users\18357\.claude\skills")
  $out = $out.Replace("C:/Users/18357/.codex/skills", "C:/Users/18357/.claude/skills")
  $out = $out.Replace("C:\Users\18357\.agents\skills", "C:\Users\18357\.claude\skills")
  $out = $out.Replace("C:/Users/18357/.agents/skills", "C:/Users/18357/.claude/skills")
  return $out
}

function Update-MarkdownForClaude([string]$SkillDir, [string]$SkillName) {
  Get-ChildItem -LiteralPath $SkillDir -Recurse -File -Force |
    Where-Object { $_.Extension -ieq ".md" -and $_.Name -ne "SKILL.md" } |
    ForEach-Object {
      $raw = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
      $updated = Convert-ToClaudeText $raw
      $updated = Convert-SkillPaths $updated $SkillName
      [System.IO.File]::WriteAllText($_.FullName, $updated, [System.Text.UTF8Encoding]::new($false))
    }
}

function Update-CodeEnvFallbacks([string]$SkillDir) {
  Get-ChildItem -LiteralPath $SkillDir -Recurse -File -Force |
    Where-Object { $_.Extension -in @(".py", ".ps1") } |
    ForEach-Object {
      $raw = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
      $raw = $raw -replace 'os\.environ\.get\("CODEX_WYATT_MEMORY_HOME",\s*"([^"]+)"\)', 'os.environ.get("CLAUDE_WYATT_MEMORY_HOME") or os.environ.get("CODEX_WYATT_MEMORY_HOME", "$1")'
      $raw = $raw -replace "os\.environ\.get\('CODEX_WYATT_MEMORY_HOME',\s*'([^']+)'\)", 'os.environ.get("CLAUDE_WYATT_MEMORY_HOME") or os.environ.get("CODEX_WYATT_MEMORY_HOME", "$1")'
      $raw = $raw -replace 'os\.environ\.get\("CODEX_WYATT_RESEARCH_ROOT",\s*"([^"]+)"\)', 'os.environ.get("CLAUDE_WYATT_RESEARCH_ROOT") or os.environ.get("CODEX_WYATT_RESEARCH_ROOT", "$1")'
      $raw = $raw -replace "os\.environ\.get\('CODEX_WYATT_RESEARCH_ROOT',\s*'([^']+)'\)", 'os.environ.get("CLAUDE_WYATT_RESEARCH_ROOT") or os.environ.get("CODEX_WYATT_RESEARCH_ROOT", "$1")'
      $raw = $raw -creplace "Codex", "Claude Code"
      $raw = $raw -replace "\.codex-review", ".claude-review"
      [System.IO.File]::WriteAllText($_.FullName, $raw, [System.Text.UTF8Encoding]::new($false))
    }
}

function Add-ClaudeAdaptationSection([string]$Body) {
  if ($Body -match "## Claude Code Adaptation") {
    return $Body
  }
  $section = @"

## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to `${CLAUDE_SKILL_DIR}` when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.
"@

  $lines = $Body -split "`r?`n"
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^#\s+") {
      $before = $lines[0..$i] -join "`n"
      $after = ""
      if ($i + 1 -lt $lines.Count) {
        $after = ($lines[($i + 1)..($lines.Count - 1)] -join "`n")
      }
      return ($before + $section + "`n" + $after).TrimEnd() + "`n"
    }
  }
  return ($section.TrimStart() + "`n`n" + $Body).TrimEnd() + "`n"
}

function Update-SkillMarkdown([string]$SkillFile, [string]$SkillName) {
  $raw = Get-Content -LiteralPath $SkillFile -Raw -Encoding UTF8
  if ($raw -notmatch "(?s)\A---\r?\n(?<fm>.*?)\r?\n---\r?\n(?<body>.*)\z") {
    throw "Missing YAML frontmatter: $SkillFile"
  }
  $fm = $Matches.fm
  $body = $Matches.body

  $fm = Convert-ToClaudeText $fm
  $body = Convert-ToClaudeText $body
  $body = Convert-SkillPaths $body $SkillName
  $body = Add-ClaudeAdaptationSection $body
  $fm = $fm -replace "(?m)^version:\s*.*\r?\n?", ""

  if ($fm -match "(?m)^name:\s*.*$") {
    $fm = $fm -replace "(?m)^name:\s*.*$", "name: $SkillName"
  } else {
    $fm = "name: $SkillName`n$fm"
  }

  if ($fm -notmatch "(?m)^description:\s*.+") {
    $fm = $fm.TrimEnd() + "`ndescription: Use this Claude Code skill for $SkillName tasks."
  }

  $updated = "---`n$($fm.TrimEnd())`n---`n`n$body"
  [System.IO.File]::WriteAllText($SkillFile, $updated, [System.Text.UTF8Encoding]::new($false))
}

function Update-AihubmixScript([string]$SkillDir) {
  $path = Join-Path $SkillDir "scripts\generate-ui-draft.py"
  if (-not (Test-Path -LiteralPath $path)) {
    return
  }
  $raw = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  $raw = $raw -replace 'configured_env = os\.environ\.get\("CODEX_UI_IMAGE_ENV", ""\)', 'configured_env = os.environ.get("CLAUDE_UI_IMAGE_ENV") or os.environ.get("CODEX_UI_IMAGE_ENV", "")'
  $raw = $raw -replace 'os\.environ\.get\("CODEX_UI_IMAGE_ENV"\)', 'os.environ.get("CLAUDE_UI_IMAGE_ENV") or os.environ.get("CODEX_UI_IMAGE_ENV")'
  $raw = $raw -replace 'os\.environ\.get\("CODEX_UI_IMAGE_BASE_URL"\)', 'os.environ.get("CLAUDE_UI_IMAGE_BASE_URL") or os.environ.get("CODEX_UI_IMAGE_BASE_URL")'
  $raw = $raw -replace 'os\.environ\.get\("CODEX_UI_IMAGE_MODEL"\)', 'os.environ.get("CLAUDE_UI_IMAGE_MODEL") or os.environ.get("CODEX_UI_IMAGE_MODEL")'
  $raw = $raw -replace 'os\.environ\.get\("CODEX_UI_IMAGE_API_KEY"\)', 'os.environ.get("CLAUDE_UI_IMAGE_API_KEY") or os.environ.get("CODEX_UI_IMAGE_API_KEY")'
  [System.IO.File]::WriteAllText($path, $raw, [System.Text.UTF8Encoding]::new($false))
}

function Copy-DirectoryIfPresent([string]$Source, [string]$Destination) {
  if (-not (Test-Path -LiteralPath $Source)) {
    return
  }
  if (Test-Path -LiteralPath $Destination) {
    Remove-Item -LiteralPath $Destination -Recurse -Force
  }
  Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
}

function Write-ResearchWorkflowSkill([string]$SkillDir) {
  $content = @'
---
name: research-workflow
description: Use when the user asks to generate a research report from paper links, batch-download papers, convert PDFs to Markdown, or export a research report to Word
---

# Research Workflow

## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to `${CLAUDE_SKILL_DIR}` when Claude Code exposes it; otherwise use this skill directory.
- The bundled scripts and assets are the source of truth for Claude Code usage.

Use this workflow for a paper-to-report pipeline.

## Runtime

1. Verify the H-drive runtime:
   `powershell -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}\scripts\verify-research-runtime.ps1"`
2. The helper sets `HF_HOME`, `HUGGINGFACE_HUB_CACHE`, `TEMP`, and `TMP` under `H:\T7\tools`.
3. Prefer the bundled scripts under `${CLAUDE_SKILL_DIR}\scripts`.

## Workflow

1. Batch download papers:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" download_arxiv_papers.py --input "${paper_list_file}" --outdir "${topic_outdir}" --delay 0.5`
2. Convert PDFs to Markdown:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" pdf_to_markdown.py --root "${pdf_root}"`
3. Use enhanced extraction for scanned PDFs or table-heavy layouts:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" pdf_to_markdown.py --root "${pdf_root}" --mode enhanced`
4. Analyze one paper at a time with the paired `/research-analysis-subagent` skill.
5. Preflight one paper before analysis:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" preflight.py --paper-dir "${paper_dir}"`
6. Merge the report:
   `python "${CLAUDE_SKILL_DIR}\scripts\run.py" merge_moe_report.py --base-dir "${topic_outdir}" --outline "${outline_md}" --output "${merged_report_md}"`
7. Export to Word with the bundled reference doc and Lua filter:
   `pandoc "${merged_report_md}" -o "${merged_report_docx}" --reference-doc="${CLAUDE_SKILL_DIR}\assets\reference.docx" --lua-filter="${CLAUDE_SKILL_DIR}\assets\figure_caption.lua" -f markdown-yaml_metadata_block`

## Utility

Relativize image paths only when sharing the Markdown file itself:

`python "${CLAUDE_SKILL_DIR}\scripts\run.py" convert_paths_to_relative.py --file "${merged_report_md}" --base-dir "<downloads root>"`
'@
  [System.IO.File]::WriteAllText((Join-Path $SkillDir "SKILL.md"), $content + "`n", [System.Text.UTF8Encoding]::new($false))
}

function Write-ResearchAnalysisSkill([string]$SkillDir) {
  $content = @'
---
name: research-analysis-subagent
description: Use when processing one paper directory for the research workflow and writing Analysis_Detail.md from paper.md plus paper_artifacts
---

# Research Analysis Subagent

## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to `${CLAUDE_SKILL_DIR}` when Claude Code exposes it; otherwise use this skill directory.

Use this skill only for a single paper directory at a time.

Required steps:

1. Read `assets/analysis_prompt.md` in full from this skill directory.
2. Read `${paper_dir}\paper.md`.
3. Read all images under `${paper_dir}\paper_artifacts`.
4. Write `${paper_dir}\Analysis_Detail.md` following the prompt specification exactly.
5. Remind the user to verify formula and image rendering.

Do not batch multiple papers in one invocation.
'@
  [System.IO.File]::WriteAllText((Join-Path $SkillDir "SKILL.md"), $content + "`n", [System.Text.UTF8Encoding]::new($false))
}

function Bundle-ResearchResources([string]$SkillDir, [string]$SkillName) {
  $hkAgentRoot = "H:\T7\Wyatt\HK_intership\.agent"
  if ($SkillName -eq "research-workflow") {
    $sourceSkill = Join-Path $hkAgentRoot "skills\research-workflow"
    Copy-DirectoryIfPresent (Join-Path $sourceSkill "assets") (Join-Path $SkillDir "assets")
    Copy-DirectoryIfPresent (Join-Path $sourceSkill "scripts") (Join-Path $SkillDir "scripts")
    $requirements = Join-Path $sourceSkill "requirements-lock.txt"
    if (Test-Path -LiteralPath $requirements) {
      Copy-Item -LiteralPath $requirements -Destination (Join-Path $SkillDir "requirements-lock.txt") -Force
    }
    $tools = Join-Path $hkAgentRoot "tools"
    foreach ($tool in @("research-runtime.ps1", "verify-research-runtime.ps1")) {
      $sourceTool = Join-Path $tools $tool
      if (Test-Path -LiteralPath $sourceTool) {
        Copy-Item -LiteralPath $sourceTool -Destination (Join-Path $SkillDir "scripts\$tool") -Force
      }
    }
    $runtime = Join-Path $SkillDir "scripts\research-runtime.ps1"
    if (Test-Path -LiteralPath $runtime) {
      $raw = Get-Content -LiteralPath $runtime -Raw -Encoding UTF8
      $raw = $raw.Replace("G:\tools", "H:\T7\tools")
      [System.IO.File]::WriteAllText($runtime, $raw, [System.Text.UTF8Encoding]::new($false))
    }
    Write-ResearchWorkflowSkill $SkillDir
  } elseif ($SkillName -eq "research-analysis-subagent") {
    $sourceSkill = Join-Path $hkAgentRoot "skills\research-analysis-subagent"
    Copy-DirectoryIfPresent (Join-Path $sourceSkill "assets") (Join-Path $SkillDir "assets")
    Copy-DirectoryIfPresent (Join-Path $sourceSkill "scripts") (Join-Path $SkillDir "scripts")
    Write-ResearchAnalysisSkill $SkillDir
  }
}

function Repair-KnownReferenceLinks([string]$SkillDir, [string]$SkillName) {
  if ($SkillName -eq "lark-event") {
    $path = Join-Path $SkillDir "references\lark-event-im.md"
    if (Test-Path -LiteralPath $path) {
      $raw = Get-Content -LiteralPath $path -Raw -Encoding UTF8
      $raw = $raw.Replace('[`events/im/message_receive.go`](../../../events/im/message_receive.go)', '`events/im/message_receive.go`')
      [System.IO.File]::WriteAllText($path, $raw, [System.Text.UTF8Encoding]::new($false))
    }
  }

  if ($SkillName -eq "lark-mail") {
    $path = Join-Path $SkillDir "references\lark-mail-watch.md"
    if (Test-Path -LiteralPath $path) {
      $raw = Get-Content -LiteralPath $path -Raw -Encoding UTF8
      $raw = $raw.Replace("[lark-event-subscribe](../../lark-event/references/lark-event-subscribe.md)", "[lark-event](../../lark-event/SKILL.md)")
      [System.IO.File]::WriteAllText($path, $raw, [System.Text.UTF8Encoding]::new($false))
    }
  }
}

function Test-UnsafeFileName([System.IO.FileInfo]$File) {
  $name = $File.Name.ToLowerInvariant()
  $ext = $File.Extension.ToLowerInvariant()
  if ($name -eq ".env" -or $name.StartsWith(".env.")) { return $true }
  if ($name -in @("auth.json", "credentials.json", "cookies.txt", "session.json", "sessions.json", "token.txt", "tokens.txt", "secret.txt", "secrets.txt", "password.txt", "passwords.txt", ".netrc")) { return $true }
  if ($name -match "^(id_rsa|id_dsa|id_ecdsa|id_ed25519)$") { return $true }
  if ($name -match "(?i)(credential|secret|password|session|token|private[-_]?key|api[-_]?key).*\.(json|ya?ml|toml|ini|cfg|conf|txt|pem|key)$") { return $true }
  if ($ext -in @(".pem", ".key", ".p12", ".pfx", ".kdbx", ".sqlite", ".sqlite3", ".db")) { return $true }
  if ($name -match "(?i)\.(db|sqlite|sqlite3)-(wal|journal|shm)$") { return $true }
  return $false
}

function Remove-GeneratedUnsafeFiles([string]$SkillDir) {
  $excludedDirs = @(".git", "node_modules", "__pycache__", ".venv", "venv", ".mypy_cache", ".pytest_cache")
  Get-ChildItem -LiteralPath $SkillDir -Directory -Recurse -Force |
    Where-Object { $excludedDirs -contains $_.Name } |
    Sort-Object FullName -Descending |
    ForEach-Object {
      Assert-UnderRoot $_.FullName $SkillDir
      Remove-Item -LiteralPath $_.FullName -Recurse -Force
    }

  $topLevelAgents = Join-Path $SkillDir "agents"
  if (Test-Path -LiteralPath $topLevelAgents) {
    Assert-UnderRoot $topLevelAgents $SkillDir
    Remove-Item -LiteralPath $topLevelAgents -Recurse -Force
  }

  Get-ChildItem -LiteralPath $SkillDir -File -Recurse -Force |
    Where-Object {
      $_.Name -in @(".DS_Store") -or
      $_.Name -like "._*" -or
      $_.Name -like "*.pyc" -or
      $_.Name -like "*.pyo" -or
      (Test-UnsafeFileName $_)
    } |
    ForEach-Object {
      Assert-UnderRoot $_.FullName $SkillDir
      Remove-Item -LiteralPath $_.FullName -Force
    }
}

function Test-GeneratedTextFile([System.IO.FileInfo]$File) {
  $ext = $File.Extension.ToLowerInvariant()
  if ($ext -in @(".md", ".txt", ".tsv", ".csv", ".json", ".jsonl", ".xml", ".xsd", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".py", ".ps1", ".sh", ".js", ".ts", ".css", ".html", ".lua", ".gitignore")) {
    return $true
  }
  if ($File.Name -in @(".gitignore", "LICENSE", "README", "SECURITY")) {
    return $true
  }
  return $false
}

function Normalize-GeneratedTextFile([string]$Path) {
  $raw = [System.IO.File]::ReadAllText($Path, [System.Text.UTF8Encoding]::new($false))
  $raw = $raw.Replace("`r`n", "`n").Replace("`r", "`n")
  $parts = $raw -split "`n", -1
  $lines = New-Object System.Collections.Generic.List[string]
  foreach ($part in $parts) {
    $lines.Add($part.TrimEnd("`t", " "))
  }
  while ($lines.Count -gt 0 -and $lines[$lines.Count - 1] -eq "") {
    $lines.RemoveAt($lines.Count - 1)
  }
  $updated = ""
  if ($lines.Count -gt 0) {
    $updated = ([string[]]$lines -join "`n") + "`n"
  }
  if ($updated -ne $raw) {
    [System.IO.File]::WriteAllText($Path, $updated, [System.Text.UTF8Encoding]::new($false))
  }
}

function Normalize-GeneratedTextTree([string]$Root) {
  Get-ChildItem -LiteralPath $Root -Recurse -File -Force |
    Where-Object { Test-GeneratedTextFile $_ } |
    ForEach-Object { Normalize-GeneratedTextFile $_.FullName }
}

function Get-Description([string]$SkillFile) {
  $raw = Get-Content -LiteralPath $SkillFile -Raw -Encoding UTF8
  if ($raw -match "(?m)^description:\s*(.+)$") {
    return $Matches[1].Trim().Trim('"').Trim("'")
  }
  return ""
}

$repo = Resolve-FullPath $RepoRoot
$skillsOut = Join-Path $repo "skills"
$manifestsOut = Join-Path $repo "manifests"

Assert-UnderRoot $skillsOut $repo
Assert-UnderRoot $manifestsOut $repo

if (Test-Path -LiteralPath $skillsOut) {
  Remove-Item -LiteralPath $skillsOut -Recurse -Force
}
if (Test-Path -LiteralPath $manifestsOut) {
  Remove-Item -LiteralPath $manifestsOut -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $skillsOut | Out-Null
New-Item -ItemType Directory -Force -Path $manifestsOut | Out-Null

$sources = @(
  @{ Label = "h-t7-active"; Root = $ActiveSkillRoot },
  @{ Label = "personal-codex"; Root = $PersonalCodexSkillRoot },
  @{ Label = "agents"; Root = $AgentsSkillRoot }
)

$sourceRows = New-Object System.Collections.Generic.List[string]
$skippedRows = New-Object System.Collections.Generic.List[string]
$inventoryRows = New-Object System.Collections.Generic.List[string]
$sourceRows.Add("skill`tsource_label`tsource_path`ttarget_path")
$skippedRows.Add("skill`tsource_label`tsource_path`treason")
$inventoryRows.Add("skill`tfiles`tsize_bytes`tskill_md_lines`tdescription")

$seen = @{}

foreach ($source in $sources) {
  if (-not (Test-Path -LiteralPath $source.Root)) {
    Write-Warning "Source root missing: $($source.Root)"
    continue
  }

  foreach ($skill in Get-ChildItem -LiteralPath $source.Root -Directory | Sort-Object Name) {
    $skillFile = Join-Path $skill.FullName "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile)) {
      continue
    }

    $name = $skill.Name
    if ($seen.ContainsKey($name)) {
      Write-Warning "Skipping duplicate skill '$name' from $($source.Label); already came from $($seen[$name])"
      $skippedRows.Add("$name`t$($source.Label)`t$($skill.FullName)`tduplicate of $($seen[$name])")
      continue
    }
    $seen[$name] = $source.Label

    $targetSkill = Join-Path $skillsOut $name
    Copy-Item -LiteralPath $skill.FullName -Destination $targetSkill -Recurse -Force
    Remove-GeneratedUnsafeFiles $targetSkill
    Update-SkillMarkdown (Join-Path $targetSkill "SKILL.md") $name
    Update-MarkdownForClaude $targetSkill $name
    Update-CodeEnvFallbacks $targetSkill
    Update-AihubmixScript $targetSkill
    Bundle-ResearchResources $targetSkill $name
    Repair-KnownReferenceLinks $targetSkill $name
    Remove-GeneratedUnsafeFiles $targetSkill
    Normalize-GeneratedTextTree $targetSkill

    $files = @(Get-ChildItem -LiteralPath $targetSkill -Recurse -File -Force)
    $size = ($files | Measure-Object Length -Sum).Sum
    if ($null -eq $size) {
      $size = 0
    }
    $lines = (Get-Content -LiteralPath (Join-Path $targetSkill "SKILL.md") -Encoding UTF8 | Measure-Object -Line).Lines
    $desc = Get-Description (Join-Path $targetSkill "SKILL.md")
    $sourceRows.Add("$name`t$($source.Label)`t$($skill.FullName)`t$targetSkill")
    $inventoryRows.Add("$name`t$(@($files).Count)`t$size`t$lines`t$desc")
  }
}

[System.IO.File]::WriteAllLines((Join-Path $manifestsOut "source_map.tsv"), $sourceRows, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllLines((Join-Path $manifestsOut "skipped_sources.tsv"), $skippedRows, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllLines((Join-Path $manifestsOut "skill_inventory.tsv"), $inventoryRows, [System.Text.UTF8Encoding]::new($false))

$fileRows = Get-ChildItem -LiteralPath $skillsOut -Recurse -File -Force |
  Sort-Object FullName |
  ForEach-Object { $_.FullName.Substring($repo.Length + 1) }
[System.IO.File]::WriteAllLines((Join-Path $manifestsOut "all_files.txt"), $fileRows, [System.Text.UTF8Encoding]::new($false))

Write-Host "Generated $($seen.Count) Claude Code skills under $skillsOut"
