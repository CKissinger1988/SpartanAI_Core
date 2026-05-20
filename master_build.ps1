# master_build.ps1
$ErrorActionPreference = "Stop"

$workspaceRoot = "C:\Users\ckiss\workspace\local_clone"
$backendDir = "$workspaceRoot\cloud_backend"
$isccPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" # Change if installed elsewhere

Write-Host "--- JarvisAI Backend Installer Master Build ---" -ForegroundColor Cyan

# 1. Verify Prerequisites
if (!(Test-Path $isccPath)) {
    Write-Error "Inno Setup Compiler not found at $isccPath. Please install it."
    return
}
if (!(Test-Path "$backendDir
ssm.exe")) {
    Write-Error "nssm.exe not found in $backendDir. Ensure it is placed there."
    return
}

# 2. Cleanup Old Build
if (Test-Path "$workspaceRoot\JarvisBackendInstaller.exe") {
    Remove-Item -Path "$workspaceRoot\JarvisBackendInstaller.exe" -Force
}

# 3. Compile/Build Installer
Write-Host "Running Inno Setup Compiler..." -ForegroundColor Cyan
& $isccPath "$workspaceRoot\JarvisBackend.iss"

if ($LASTEXITCODE -eq 0) {
    Write-Host "--- Build Successful: JarvisBackendInstaller.exe created ---" -ForegroundColor Green
} else {
    Write-Error "Build failed."
}
