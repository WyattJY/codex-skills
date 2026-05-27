param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$InstallRoot = (Join-Path $HOME ".claude\skills")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$skillsRoot = Join-Path $RepoRoot "skills"
$manifestRoot = Join-Path $RepoRoot "manifests"
if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "Missing generated skills directory: $skillsRoot"
}
New-Item -ItemType Directory -Force -Path $manifestRoot | Out-Null

$rows = New-Object System.Collections.Generic.List[object]
$managed = @{}
$failures = 0

foreach ($skill in Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name) {
  $managed[$skill.Name] = $true
  $installed = Join-Path $InstallRoot $skill.Name
  $exists = Test-Path -LiteralPath $installed
  $linkType = ""
  $target = ""
  $status = "fail"

  if ($exists) {
    $item = Get-Item -LiteralPath $installed
    $linkType = [string]$item.LinkType
    $target = ($item.Target -join "; ")
    if ($linkType -eq "Junction" -and $target -ieq $skill.FullName) {
      $status = "pass"
    }
  }

  if ($status -ne "pass") {
    $failures++
  }

  $rows.Add([pscustomobject]@{
    Skill = $skill.Name
    Status = $status
    InstalledPath = $installed
    LinkType = $linkType
    Target = $target
  })
}

foreach ($existing in Get-ChildItem -LiteralPath $InstallRoot -Directory -Force | Sort-Object Name) {
  if (-not $managed.ContainsKey($existing.Name)) {
    $item = Get-Item -LiteralPath $existing.FullName
    $rows.Add([pscustomobject]@{
      Skill = $existing.Name
      Status = "extra"
      InstalledPath = $existing.FullName
      LinkType = [string]$item.LinkType
      Target = ($item.Target -join "; ")
    })
    $failures++
  }
}

$rows | Format-Table -AutoSize
$rows | Export-Csv -LiteralPath (Join-Path $manifestRoot "storage_audit.tsv") -Delimiter "`t" -NoTypeInformation -Encoding UTF8

if ($failures -gt 0) {
  throw "$failures Claude skills are missing, extra, or not installed as H-drive junctions."
}

Write-Host "Storage audit passed: installed Claude skills exactly match generated H-drive skills."
