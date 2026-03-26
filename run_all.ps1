
# 1️ Wait for Oracle XE listener to be ready
$oracleReady = $false
while (-not $oracleReady) {
    try {
        tnsping XE | Out-Null
        $oracleReady = $true
    } catch {
        Write-Host "Oracle not ready yet. Waiting 10 seconds..."
        Start-Sleep -Seconds 10
    }
}

Write-Host " Oracle is ready!"

# 2️ Run all batch files in order
$batFiles = @(
    ".\INSTALL_ORACLE_DATABASE.bat",
    ".\INSTALL_ORACLE_PACKAGE.bat",
    ".\QUICK_INSTALL.bat",
    ".\RUN_PROJECT.bat"
)

foreach ($bat in $batFiles) {
    if (Test-Path $bat) {
        Write-Host "Running $bat..."
        Start-Process cmd.exe -ArgumentList "/c `"$bat`"" -Wait
    } else {
        Write-Host " File not found: $bat"
    }
}

Write-Host " All batch files executed successfully!"