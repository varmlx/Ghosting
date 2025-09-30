param(
  [string]$amount = '100'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

./set-env.ps1 -envname sandbox | Out-Null

$py = Join-Path $root '.venv\Scripts\python.exe'
if (!(Test-Path $py)) {
  throw 'Venv bulunamadı. Önce .venv oluşturun.'
}

# Opsiyonel: miktarı ortamdan geç
$env:AMOUNT_USDC = $amount

& $py trading_agent.py

