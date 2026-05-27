Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\research-runtime.ps1"

$pythonOutput = & $env:RESEARCH_PYTHON -c "import docling, docling_core, torch; print('ok')"
if ($pythonOutput.Trim() -ne 'ok') {
    throw "Unexpected Python verification output: $pythonOutput"
}

$pandocOutput = & $env:RESEARCH_PANDOC --version
$pandocFirstLine = ($pandocOutput | Select-Object -First 1)
if (-not $pandocFirstLine) {
    throw 'pandoc verification returned no output'
}

Write-Host "python-ok: $env:RESEARCH_PYTHON"
Write-Host "pandoc-ok: $pandocFirstLine"
