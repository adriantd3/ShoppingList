param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("setup", "run", "test", "lint", "typecheck", "check", "migrate-up", "migrate-revision", "seed-dummy-user")]
    [string]$Action
    ,
    [string]$Message = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$apiPath = Join-Path $repoRoot "backend\python-api"

function Import-EnvFileIfPresent {
    param(
        [Parameter(Mandatory = $true)]
        [string]$EnvFilePath
    )

    if (-not (Test-Path $EnvFilePath)) {
        return
    }

    $lines = Get-Content $EnvFilePath
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith("#")) {
            continue
        }

        $parts = $trimmed.Split("=", 2)
        if ($parts.Count -ne 2) {
            continue
        }

        $key = $parts[0].Trim()
        $value = $parts[1].Trim()

        # Import a safe allowlist of runtime keys used by FastAPI settings.
        $allowedKeys = @(
            "APP_ENV",
            "APP_DEBUG",
            "APP_HOST",
            "APP_PORT",
            "API_V1_PREFIX",
            "DATABASE_URL",
            "JWT_SECRET_KEY",
            "JWT_ALGORITHM",
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "CORS_ALLOW_ORIGINS",
            "TRUSTED_HOSTS",
            "ENABLE_DOCS",
            "LOG_LEVEL"
        )
        if ($allowedKeys -notcontains $key) {
            continue
        }
        if ([string]::IsNullOrWhiteSpace($key)) {
            continue
        }

        [Environment]::SetEnvironmentVariable($key, $value, "Process")
    }
}

function Normalize-ListEnvironmentVariable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $currentValue = [Environment]::GetEnvironmentVariable($Name, "Process")
    if ([string]::IsNullOrWhiteSpace($currentValue)) {
        return
    }

    $trimmed = $currentValue.Trim()
    if ($trimmed.StartsWith("[") -and $trimmed.EndsWith("]")) {
        return
    }

    $items = @()
    foreach ($item in $trimmed.Split(",")) {
        $entry = $item.Trim()
        if (-not [string]::IsNullOrWhiteSpace($entry)) {
            $items += $entry
        }
    }

    [Environment]::SetEnvironmentVariable($Name, ($items | ConvertTo-Json -Compress), "Process")
}

Push-Location $apiPath
try {
    function Initialize-RuntimeEnvironment {
        Import-EnvFileIfPresent -EnvFilePath (Join-Path $repoRoot ".env")
        Normalize-ListEnvironmentVariable -Name "CORS_ALLOW_ORIGINS"
        Normalize-ListEnvironmentVariable -Name "TRUSTED_HOSTS"
    }

    switch ($Action) {
        "setup" {
            & (Join-Path $PSScriptRoot "setup.ps1")
        }
        "run" {
            Initialize-RuntimeEnvironment
            uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
        }
        "test" {
            uv run pytest -q
        }
        "lint" {
            uv run ruff check .
        }
        "typecheck" {
            uv run mypy app tests
        }
        "check" {
            uv run ruff check .
            uv run mypy app tests
            uv run pytest -q
        }
        "migrate-up" {
            Initialize-RuntimeEnvironment
            uv run alembic upgrade head
        }
        "migrate-revision" {
            if ([string]::IsNullOrWhiteSpace($Message)) {
                throw "Message is required for migrate-revision"
            }
            Initialize-RuntimeEnvironment
            uv run alembic revision -m $Message
        }
        "seed-dummy-user" {
            Initialize-RuntimeEnvironment
            uv run alembic upgrade head
            uv run python scripts/seed_dummy_user.py
        }
        default {
            throw "Unsupported action: $Action"
        }
    }
}
finally {
    Pop-Location
}
