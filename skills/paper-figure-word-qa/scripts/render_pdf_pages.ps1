param(
  [Parameter(Mandatory = $true)]
  [string]$PdfPath,

  [Parameter(Mandatory = $true)]
  [string]$InspectDir,

  [int]$Dpi = 240,

  [int]$MinExpectedPages = 1
)

$ErrorActionPreference = "Stop"

$pdfItem = Get-Item -LiteralPath $PdfPath
New-Item -ItemType Directory -Force -Path $InspectDir | Out-Null

Get-Command pdfinfo | Out-Null
Get-Command pdftoppm | Out-Null

$info = pdfinfo $pdfItem.FullName
$pageLine = $info | Where-Object { $_ -match '^Pages:\s+(\d+)' } | Select-Object -First 1
if (-not $pageLine) {
  throw "Could not read page count from pdfinfo."
}

$pageCount = [int]([regex]::Match($pageLine, '^Pages:\s+(\d+)').Groups[1].Value)
if ($pageCount -lt $MinExpectedPages) {
  throw "PDF page count $pageCount is below expected minimum $MinExpectedPages."
}

Get-ChildItem -LiteralPath $InspectDir -Filter 'page-*.png' -ErrorAction SilentlyContinue |
  Remove-Item -Force

$prefix = Join-Path $InspectDir 'page'
pdftoppm -png -r $Dpi -- $pdfItem.FullName $prefix

$rendered = Get-ChildItem -LiteralPath $InspectDir -Filter 'page-*.png' |
  Where-Object { $_.LastWriteTime -gt $pdfItem.LastWriteTime } |
  Sort-Object Name

if ($rendered.Count -lt $pageCount) {
  throw "Rendered $($rendered.Count) PNG pages, expected $pageCount."
}

[pscustomobject]@{
  PdfPath = $pdfItem.FullName
  InspectDir = (Get-Item -LiteralPath $InspectDir).FullName
  Dpi = $Dpi
  PageCount = $pageCount
  RenderedCount = $rendered.Count
  FirstPage = $rendered[0].FullName
  LastPage = $rendered[-1].FullName
}
