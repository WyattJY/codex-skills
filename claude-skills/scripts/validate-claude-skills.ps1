param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$skillsRoot = Join-Path $RepoRoot "skills"
$manifestRoot = Join-Path $RepoRoot "manifests"
New-Item -ItemType Directory -Force -Path $manifestRoot | Out-Null

if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "Missing skills directory: $skillsRoot"
}

$rows = New-Object System.Collections.Generic.List[string]
$rows.Add("skill`tstatus`twarnings")
$bad = 0

foreach ($dir in Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name) {
  $warnings = New-Object System.Collections.Generic.List[string]
  $skillFile = Join-Path $dir.FullName "SKILL.md"
  if (-not (Test-Path -LiteralPath $skillFile)) {
    $rows.Add("$($dir.Name)`tfail`tmissing SKILL.md")
    $bad++
    continue
  }

  $raw = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8
  if ($raw -notmatch "(?s)\A---\r?\n(?<fm>.*?)\r?\n---\r?\n(?<body>.*)\z") {
    $rows.Add("$($dir.Name)`tfail`tmissing YAML frontmatter")
    $bad++
    continue
  }
  $fm = $Matches.fm
  if ($fm -notmatch "(?m)^name:\s*$([regex]::Escape($dir.Name))\s*$") {
    $warnings.Add("name does not match directory")
  }
  if ($fm -notmatch "(?m)^description:\s*.+") {
    $warnings.Add("missing description")
  }
  $lineCount = (Get-Content -LiteralPath $skillFile -Encoding UTF8 | Measure-Object -Line).Lines
  if ($lineCount -gt 500) {
    $warnings.Add("SKILL.md has $lineCount lines; consider moving detail to references")
  }

  $unsafe = Get-ChildItem -LiteralPath $dir.FullName -File -Recurse -Force |
    Where-Object { $_.Name -ieq ".env" -or $_.Name -match "(?i)(cookie|session|credential|token|secret|password)" }
  if ($unsafe) {
    $warnings.Add("possible unsafe files: " + (($unsafe | Select-Object -First 5 -ExpandProperty Name) -join ","))
  }

  $status = "pass"
  $warningText = ($warnings -join "; ")
  if ([string]::IsNullOrWhiteSpace($warningText)) {
    $warningText = "none"
  }
  $rows.Add("$($dir.Name)`t$status`t$warningText")
}

[System.IO.File]::WriteAllLines((Join-Path $manifestRoot "validation.tsv"), $rows, [System.Text.UTF8Encoding]::new($false))

if ($bad -gt 0) {
  throw "$bad skills failed validation"
}

Write-Host "Validation passed for $((Get-ChildItem -LiteralPath $skillsRoot -Directory).Count) skills."
Write-Host "Report: $(Join-Path $manifestRoot 'validation.tsv')"
