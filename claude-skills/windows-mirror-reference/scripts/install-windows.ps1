param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$InstallRoot = (Join-Path $HOME ".claude\skills"),
  [switch]$CopyInsteadOfJunction,
  [switch]$PruneUnmanaged
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$skillsRoot = Join-Path $RepoRoot "skills"
if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "Missing generated skills directory: $skillsRoot"
}

New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null
$backupRoot = Join-Path (Split-Path -Parent $InstallRoot) ("backups\claude-skills-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
$managed = @{}

foreach ($skill in Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name) {
  $managed[$skill.Name] = $true
  $target = Join-Path $InstallRoot $skill.Name
  if (Test-Path -LiteralPath $target) {
    New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
    Move-Item -LiteralPath $target -Destination (Join-Path $backupRoot $skill.Name) -Force
  }

  if ($CopyInsteadOfJunction) {
    Copy-Item -LiteralPath $skill.FullName -Destination $target -Recurse -Force
  } else {
    New-Item -ItemType Junction -Path $target -Target $skill.FullName | Out-Null
  }
  Write-Host "Installed $($skill.Name) -> $target"
}

if ($PruneUnmanaged) {
  foreach ($existing in Get-ChildItem -LiteralPath $InstallRoot -Directory -Force | Sort-Object Name) {
    if (-not $managed.ContainsKey($existing.Name)) {
      New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
      Move-Item -LiteralPath $existing.FullName -Destination (Join-Path $backupRoot $existing.Name) -Force
      Write-Host "Pruned unmanaged skill $($existing.Name)"
    }
  }
}

Write-Host "Installed $((Get-ChildItem -LiteralPath $skillsRoot -Directory).Count) Claude Code skills into $InstallRoot"
if (Test-Path -LiteralPath $backupRoot) {
  Write-Host "Backed up replaced skills under $backupRoot"
}
