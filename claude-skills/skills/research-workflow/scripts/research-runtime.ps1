Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:ResearchToolsRoot = 'H:\T7\tools'
$script:ResearchRuntimeRoot = Join-Path $script:ResearchToolsRoot 'research-workflow'
$script:ResearchPython = Join-Path $script:ResearchRuntimeRoot 'venv\Scripts\python.exe'

function Get-ResearchPandoc {
    $candidates = @(
        'H:\T7\tools\pandoc\current\pandoc.exe',
        'H:\T7\tools\pandoc\pandoc.exe'
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    $found = Get-ChildItem -Path 'H:\T7\tools\pandoc' -Filter 'pandoc.exe' -Recurse -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($found) {
        return $found.FullName
    }

    throw 'pandoc.exe was not found under H:\T7\tools\pandoc'
}

function Set-ResearchRuntimeEnvironment {
    if (-not (Test-Path $script:ResearchPython)) {
        throw "Research Python runtime not found: $script:ResearchPython"
    }

    $pandocExe = Get-ResearchPandoc
    $pandocDir = Split-Path -Parent $pandocExe
    $pandocDataDir = Join-Path $script:ResearchToolsRoot 'pandoc\data'
    $tmpDir = Join-Path $script:ResearchToolsRoot 'tmp'
    $hfHome = Join-Path $script:ResearchToolsRoot 'hf'
    $hfHub = Join-Path $hfHome 'hub'
    $torchHome = Join-Path $script:ResearchToolsRoot 'torch'
    foreach ($dir in @($pandocDataDir, $tmpDir, $hfHome, $hfHub, $torchHome)) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Force -Path $dir | Out-Null
        }
    }

    $env:RESEARCH_TOOLS_ROOT = $script:ResearchToolsRoot
    $env:RESEARCH_RUNTIME_ROOT = $script:ResearchRuntimeRoot
    $env:RESEARCH_PYTHON = $script:ResearchPython
    $env:RESEARCH_PANDOC = $pandocExe
    $env:PANDOC_EXE = $pandocExe
    $env:PANDOC_DATA_DIR = $pandocDataDir
    $env:TEMP = $tmpDir
    $env:TMP = $tmpDir
    $env:HF_HOME = $hfHome
    $env:HF_HUB_CACHE = $hfHub
    $env:HUGGINGFACE_HUB_CACHE = $hfHub
    $env:TORCH_HOME = $torchHome
    $env:HF_HUB_DISABLE_SYMLINKS = '1'
    $env:HF_HUB_DISABLE_SYMLINKS_WARNING = '1'

    if (-not (($env:PATH -split ';') -contains $pandocDir)) {
        $env:PATH = "$pandocDir;$($env:PATH)"
    }
}

Set-ResearchRuntimeEnvironment
