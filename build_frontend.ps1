# build_frontend.ps1 - Automated JarvisAI Windows Frontend Compiler
$ErrorActionPreference = "Stop"

$workspaceRoot = Get-Location
$projectDir = "$workspaceRoot\local_frontend\JarvisClient"

Write-Host "--- JarvisAI Windows Frontend Build ---" -ForegroundColor Cyan

# 1. Verification
if (!(Test-Path $projectDir)) {
    Write-Error "Project directory not found: $projectDir"
    return
}

# 2. Compilation
cd $projectDir
Write-Host "Restoring dependencies and compiling..." -ForegroundColor Yellow
dotnet publish -c Release -r win-x64 --self-contained

if ($LASTEXITCODE -eq 0) {
    Write-Host "--- Build Successful: Frontend EXE created ---" -ForegroundColor Green
    Write-Host "Output: $projectDir\bin\Release\net9.0\win-x64\publish\" -ForegroundColor Yellow
} else {
    Write-Error "Frontend build failed."
}
