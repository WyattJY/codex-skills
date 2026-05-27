param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string[]]$SkillName = @(),
  [decimal]$MaxBudgetUsd = 0.20,
  [int]$PerSkillTimeoutSeconds = 0
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$npmBin = Join-Path $env:APPDATA "npm"
if (Test-Path -LiteralPath $npmBin) {
  $env:Path = "$npmBin;$env:Path"
}

$skillsRoot = Join-Path $RepoRoot "skills"
if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "Missing generated skills directory: $skillsRoot"
}

$resultRoot = Join-Path $RepoRoot "test-results"
New-Item -ItemType Directory -Force -Path $resultRoot | Out-Null
$manifestRoot = Join-Path $RepoRoot "manifests"
New-Item -ItemType Directory -Force -Path $manifestRoot | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$resultFile = Join-Path $resultRoot "claude-cli-tests-$stamp.jsonl"
$runWorkspace = Join-Path ([System.IO.Path]::GetTempPath()) "claude-skill-smoke-tests-$stamp"
New-Item -ItemType Directory -Force -Path $runWorkspace | Out-Null

$skills = Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name
if ($SkillName.Count -gt 0) {
  $wanted = @{}
  foreach ($name in $SkillName) { $wanted[$name] = $true }
  $skills = $skills | Where-Object { $wanted.ContainsKey($_.Name) }
}

foreach ($skill in $skills) {
  $claude = Get-Command claude.ps1 -ErrorAction SilentlyContinue
  if ($null -eq $claude) {
    $claude = Get-Command claude -ErrorAction SilentlyContinue
  }
  if ($null -eq $claude) {
    $claude = Get-Command claude.cmd -ErrorAction Stop
  }

  $prompt = @"
/$($skill.Name)
This is a non-destructive skill smoke test in a disposable temporary workspace. Do not edit files, run shell commands, call APIs, or browse the web. If the skill needs real inputs, do not proceed with the workflow. Reply with exactly one line:
SKILL_TEST_LOADED: $($skill.Name) - <seven words or fewer describing this skill>
"@

  $started = Get-Date
  Push-Location $runWorkspace
  try {
    $output = & $claude.Source -p $prompt --max-budget-usd $MaxBudgetUsd --effort low --tools "" --permission-mode dontAsk --no-session-persistence 2>&1
  } finally {
    Pop-Location
  }
  $exitCode = $LASTEXITCODE
  $elapsedMs = [int]((Get-Date) - $started).TotalMilliseconds
  $text = ($output | Out-String).Trim()
  $licenseGate = ($exitCode -eq 0 -and $text -match "Do you accept all terms in the LICENSE\?")
  $budgetExceeded = ($text -match "Exceeded USD budget")
  $exactAck = ($exitCode -eq 0 -and $text -match "SKILL_TEST_LOADED:\s*$([regex]::Escape($skill.Name))")
  $loadedResponse = ($exitCode -eq 0 -and -not [string]::IsNullOrWhiteSpace($text))
  $ok = $exactAck -or $loadedResponse
  $status = "fail"
  if ($exactAck) {
    $status = "pass"
  } elseif ($licenseGate) {
    $status = "license_gate"
    $ok = $true
  } elseif ($loadedResponse) {
    $status = "loaded_response"
  } elseif ($budgetExceeded) {
    $status = "budget_exceeded"
  }
  $record = [ordered]@{
    skill = $skill.Name
    ok = $ok
    status = $status
    exit_code = $exitCode
    elapsed_ms = $elapsedMs
    output = $text
  }
  $json = $record | ConvertTo-Json -Compress
  Add-Content -LiteralPath $resultFile -Encoding UTF8 -Value $json
  if ($status -eq "pass") {
    Write-Host "PASS $($skill.Name)"
  } elseif ($status -eq "loaded_response") {
    Write-Host "LOADED_RESPONSE $($skill.Name)"
  } elseif ($status -eq "license_gate") {
    Write-Host "LICENSE_GATE $($skill.Name)"
  } elseif ($status -eq "budget_exceeded") {
    Write-Host "BUDGET_EXCEEDED $($skill.Name)"
  } else {
    Write-Host "FAIL $($skill.Name)"
    Write-Host $text
  }
}

$summaryRows = New-Object System.Collections.Generic.List[string]
$summaryRows.Add("skill`tstatus`tok`texit_code`telapsed_ms`toutput")
Get-Content -LiteralPath $resultFile -Encoding UTF8 | ForEach-Object {
  if ([string]::IsNullOrWhiteSpace($_)) {
    return
  }
  $record = $_ | ConvertFrom-Json
  $outputText = ([string]$record.output -replace "`t", " " -replace "`r?`n", " ")
  if ($outputText.Length -gt 120) {
    $outputText = $outputText.Substring(0, 120)
  }
  $summaryRows.Add("$($record.skill)`t$($record.status)`t$($record.ok)`t$($record.exit_code)`t$($record.elapsed_ms)`t$outputText")
}
[System.IO.File]::WriteAllLines((Join-Path $manifestRoot "claude_cli_test_summary.tsv"), $summaryRows, [System.Text.UTF8Encoding]::new($false))

Write-Host "Claude CLI test results: $resultFile"
Write-Host "Summary: $(Join-Path $manifestRoot 'claude_cli_test_summary.tsv')"
