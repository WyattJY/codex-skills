param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [int]$MaxSkillMdLines = 500
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$skillsRoot = Join-Path $RepoRoot "skills"
$manifestRoot = Join-Path $RepoRoot "manifests"
$sourceMap = Join-Path $manifestRoot "source_map.tsv"
New-Item -ItemType Directory -Force -Path $manifestRoot | Out-Null

if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "Missing skills directory: $skillsRoot"
}
if (-not (Test-Path -LiteralPath $sourceMap)) {
  throw "Missing source map: $sourceMap"
}

function Add-Issue(
  [System.Collections.Generic.List[string]]$Rows,
  [string]$Skill,
  [string]$Severity,
  [string]$Check,
  [string]$Detail
) {
  $safeDetail = ($Detail -replace "`t", " " -replace "`r?`n", " ")
  $Rows.Add("$Skill`t$Severity`t$Check`t$safeDetail")
}

function Test-RelativeMarkdownLinks(
  [string]$SkillName,
  [string]$SkillDir,
  [string]$MarkdownFile,
  [System.Collections.Generic.List[string]]$Rows
) {
  $raw = Get-Content -LiteralPath $MarkdownFile -Raw -Encoding UTF8
  $raw = [regex]::Replace($raw, '(?s)```.*?```', '')
  $raw = [regex]::Replace($raw, '`[^`]*`', '')
  $matches = [regex]::Matches($raw, '\[[^\]]+\]\((?<target>[^)]+)\)')
  foreach ($match in $matches) {
    $target = $match.Groups["target"].Value.Trim()
    if ($target -match '^(https?:|mailto:|#)' -or $target.StartsWith('$')) {
      continue
    }
    $target = ($target -split '\s+"')[0]
    $target = ($target -split "\s+'")[0]
    $target = $target.Split('#')[0]
    if ([string]::IsNullOrWhiteSpace($target)) {
      continue
    }
    if ([System.IO.Path]::IsPathRooted($target)) {
      continue
    }
    $candidate = Join-Path (Split-Path -Parent $MarkdownFile) $target
    if (-not (Test-Path -LiteralPath $candidate)) {
      Add-Issue $Rows $SkillName "fail" "relative-link" "$MarkdownFile references missing $target"
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

$rows = New-Object System.Collections.Generic.List[string]
$rows.Add("skill`tseverity`tcheck`tdetail")

$sourceNames = @(Import-Csv -LiteralPath $sourceMap -Delimiter "`t" | Select-Object -ExpandProperty skill)
$sourceUnique = @($sourceNames | Sort-Object -Unique)
$skillDirs = @(Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name)
$skillNames = @($skillDirs | Select-Object -ExpandProperty Name)

if ($sourceUnique.Count -ne $skillDirs.Count) {
  Add-Issue $rows "_summary" "fail" "count" "source_map unique=$($sourceUnique.Count), generated=$($skillDirs.Count)"
}

$missingGenerated = @($sourceUnique | Where-Object { $skillNames -notcontains $_ })
foreach ($name in $missingGenerated) {
  Add-Issue $rows $name "fail" "missing-generated" "source skill was not generated"
}

$extraGenerated = @($skillNames | Where-Object { $sourceUnique -notcontains $_ })
foreach ($name in $extraGenerated) {
  Add-Issue $rows $name "fail" "extra-generated" "generated skill is not in source_map"
}

foreach ($dir in $skillDirs) {
  $skillFile = Join-Path $dir.FullName "SKILL.md"
  if (-not (Test-Path -LiteralPath $skillFile)) {
    Add-Issue $rows $dir.Name "fail" "entrypoint" "missing SKILL.md"
    continue
  }

  $raw = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8
  if ($raw -notmatch "(?s)\A---\r?\n(?<fm>.*?)\r?\n---\r?\n(?<body>.*)\z") {
    Add-Issue $rows $dir.Name "fail" "frontmatter" "missing YAML frontmatter"
    continue
  }

  $fm = $Matches.fm
  $body = $Matches.body
  if ($fm -notmatch "(?m)^name:\s*$([regex]::Escape($dir.Name))\s*$") {
    Add-Issue $rows $dir.Name "fail" "frontmatter-name" "name field must match directory and slash command"
  }
  if ($fm -match "(?m)^version:\s*") {
    Add-Issue $rows $dir.Name "fail" "frontmatter-version" "top-level version is not part of the Claude Code skill metadata contract"
  }
  if ($fm -notmatch "(?m)^description:\s*(?<description>.+)$") {
    Add-Issue $rows $dir.Name "fail" "frontmatter-description" "missing description"
  } else {
    $description = $Matches.description.Trim().Trim('"').Trim("'")
    if ($description.Length -gt 1536) {
      Add-Issue $rows $dir.Name "fail" "frontmatter-description" "description exceeds Claude Code listing cap"
    }
  }
  if ($fm -match "(?m)^\t") {
    Add-Issue $rows $dir.Name "fail" "frontmatter-yaml" "frontmatter contains tab indentation"
  }

  $lineCount = (Get-Content -LiteralPath $skillFile -Encoding UTF8 | Measure-Object -Line).Lines
  if ($lineCount -gt $MaxSkillMdLines) {
    Add-Issue $rows $dir.Name "fail" "skill-md-size" "SKILL.md has $lineCount lines; Claude docs recommend under $MaxSkillMdLines"
  }

  if ($body -match "C:\\Users\\18357\\\.codex\\skills|C:/Users/18357/\.codex/skills|C:\\Users\\18357\\\.agents\\skills|C:/Users/18357/\.agents/skills") {
    Add-Issue $rows $dir.Name "fail" "old-loader-path" "body still references old local skill loader path"
  }
  if ($body -match "G:\\Wyatt\\HK_intership") {
    Add-Issue $rows $dir.Name "fail" "old-workspace-path" "body still references the old G-drive HK workspace path instead of bundled resources"
  }
  if ($dir.Name -eq "research-workflow") {
    foreach ($required in @("scripts\run.py", "scripts\pdf_to_markdown.py", "scripts\merge_moe_report.py", "scripts\verify-research-runtime.ps1", "scripts\research-runtime.ps1", "assets\reference.docx", "assets\figure_caption.lua")) {
      if (-not (Test-Path -LiteralPath (Join-Path $dir.FullName $required))) {
        Add-Issue $rows $dir.Name "fail" "bundled-resource" "missing $required"
      }
    }
  }
  if ($dir.Name -eq "research-analysis-subagent") {
    foreach ($required in @("assets\analysis_prompt.md")) {
      if (-not (Test-Path -LiteralPath (Join-Path $dir.FullName $required))) {
        Add-Issue $rows $dir.Name "fail" "bundled-resource" "missing $required"
      }
    }
  }

  $topLevelAgents = Join-Path $dir.FullName "agents"
  if (Test-Path -LiteralPath $topLevelAgents) {
    Add-Issue $rows $dir.Name "fail" "codex-ui-metadata" "top-level agents directory should not be published as Claude skill content"
  }

  $unsafeFiles = @(Get-ChildItem -LiteralPath $dir.FullName -File -Recurse -Force |
    Where-Object { Test-UnsafeFileName $_ })
  if ($unsafeFiles.Count -gt 0) {
    Add-Issue $rows $dir.Name "fail" "unsafe-files" (($unsafeFiles | Select-Object -First 5 -ExpandProperty FullName) -join "; ")
  }

  foreach ($md in Get-ChildItem -LiteralPath $dir.FullName -File -Recurse -Filter "*.md" -Force) {
    Test-RelativeMarkdownLinks $dir.Name $dir.FullName $md.FullName $rows
  }
}

if ($rows.Count -eq 1) {
  $rows.Add("_summary`tpass`tall`tcodex source skills and Claude generated skills are aligned")
}

$reviewPath = Join-Path $manifestRoot "review.tsv"
[System.IO.File]::WriteAllLines($reviewPath, $rows, [System.Text.UTF8Encoding]::new($false))

$failures = @($rows | Select-Object -Skip 1 | Where-Object { $_ -match "^[^`t]+`tfail`t" })
if ($failures.Count -gt 0) {
  throw "$($failures.Count) review checks failed. See $reviewPath"
}

Write-Host "Review passed for $($skillDirs.Count) Claude Code skills."
Write-Host "Report: $reviewPath"
