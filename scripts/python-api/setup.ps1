Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$apiPath = Join-Path $repoRoot "backend\python-api"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv is required but was not found in PATH. Install uv first: https://docs.astral.sh/uv/getting-started/installation/"
}

Push-Location $apiPath
try {
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating virtual environment in backend/python-api/.venv"
        uv venv .venv
    }

    Write-Host "Syncing Python dependencies"
    uv sync --all-groups

    Write-Host "Environment ready."
    Write-Host "Run API:  make py-backend-run"
    Write-Host "Run tests: make py-backend-test"
}
finally {
    Pop-Location
}
