param(
  [ValidateSet('sandbox','production')]
  [string]$envname = 'sandbox',
  [string]$apikey = ''
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (!(Test-Path .venv\Scripts\python.exe)) {
  Write-Host 'Venv yok. Önce: python -m venv .venv' -ForegroundColor Yellow
}

$baseUrl = if ($envname -eq 'production') { 'https://api.competitions.recall.network' } else { 'https://api.sandbox.competitions.recall.network' }

$lines = @()
if ($apikey) { $lines += "RECALL_API_KEY=$apikey" }
$lines += "RECALL_BASE_URL=$baseUrl"

Set-Content -Path .env -Value $lines -Encoding UTF8
Write-Host "Yazıldı: .env -> $envname ($baseUrl)" -ForegroundColor Green

