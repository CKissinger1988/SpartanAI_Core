<#
    .SYNOPSIS
        SpartanAI Terminal - Kali Linux WSL Installer
        MANDATE: Automated Provisioning & Native Integration
    
    .DESCRIPTION
        1. Enables WSL and VM Platform features.
        2. Installs Kali Linux (Distro: kali-linux).
        3. Configures the Linux environment using scripts/kali_bootstrap.sh.
#>

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "      SPARTANAI TERMINAL - KALI WSL INSTALLER      " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Check/Enable WSL Features
Write-Host "[*] Validating Windows Subsystem for Linux state..." -ForegroundColor Yellow
$wslStatus = wsl --status 2>$null
if ($null -eq $wslStatus) {
    Write-Host "[!] WSL is not enabled. Enabling mandatory features..." -ForegroundColor Red
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart | Out-Null
    Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart | Out-Null
    Write-Host "[!] Mandatory features enabled. A SYSTEM REBOOT IS REQUIRED." -ForegroundColor Yellow
    Write-Host "[!] Please reboot and run this script again." -ForegroundColor Yellow
    exit
}

# 2. Install Kali Linux
Write-Host "[*] Checking for existing Kali Linux installation..." -ForegroundColor Yellow
$distros = wsl --list --quiet
if ($distros -match "kali-linux") {
    Write-Host "[+] Kali Linux already detected. Proceeding to bootstrap..." -ForegroundColor Green
} else {
    Write-Host "[*] Downloading and installing Kali Linux..." -ForegroundColor Yellow
    wsl --install -d kali-linux --no-launch
    Write-Host "[+] Kali Linux installation initiated. Please complete the user setup in the new window." -ForegroundColor Green
    Write-Host "[*] Waiting for user to complete Linux setup (Press Enter once finished)..." -ForegroundColor Cyan
    Read-Host
}

# 3. Bootstrapping
Write-Host "[*] Commencing Kali Bootstrap Phase..." -ForegroundColor Yellow

$hostScriptPath = Join-Path $PSScriptRoot "kali_bootstrap.sh"
$linuxScriptPath = "/tmp/kali_bootstrap.sh"

# Copy bootstrap script to Kali
Write-Host "[-] Uploading bootstrap engine to Kali Enclave..." -ForegroundColor Yellow
wsl -d kali-linux -u root -- bash -c "cat > $linuxScriptPath" < $hostScriptPath

# Execute bootstrap script
Write-Host "[-] Executing bootstrap engine (requires root escalation)..." -ForegroundColor Yellow
wsl -d kali-linux -u root -- bash $linuxScriptPath

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "      KALI WSL INSTALLATION & PROVISIONING COMPLETE      " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "[*] You can now access your hardened environment by running: wsl -d kali-linux" -ForegroundColor Cyan
