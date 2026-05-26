# SentinelAI Hyper-V Diagnostic Script
# MANDATE: Identify why the sovereign VM deployment is failing.

Write-Host "--- SENTINELAI HYPER-V DIAGNOSTICS ---" -ForegroundColor Cyan

# 1. Check Administrative Privileges
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[ERROR]: This script MUST be run as ADMINISTRATOR." -ForegroundColor Red
    return
}

# 2. Check Hyper-V Feature State
Write-Host "[1/4] Checking Hyper-V Windows Feature..." -ForegroundColor White
$feature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -ErrorAction SilentlyContinue
if ($feature.State -ne "Enabled") {
    Write-Host "[FAIL]: Hyper-V feature is NOT enabled. Run: Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All" -ForegroundColor Red
} else {
    Write-Host "[PASS]: Hyper-V feature is enabled." -ForegroundColor Green
}

# 3. Check Virtualization Support (BIOS/UEFI)
Write-Host "[2/4] Checking Hardware Virtualization..." -ForegroundColor White
$cpu = Get-WmiObject Win32_Processor
if ($cpu.VirtualizationFirmwareEnabled -eq $false) {
    Write-Host "[FAIL]: Virtualization is disabled in BIOS/UEFI. Please enable Intel VT-x or AMD-V." -ForegroundColor Red
} else {
    Write-Host "[PASS]: Hardware virtualization is enabled." -ForegroundColor Green
}

# 4. Check Disk Space and Paths
Write-Host "[3/4] Checking Paths and Resources..." -ForegroundColor White
$isoPath = "C:\GitHub\SentinelAI_Server.iso"
if (Test-Path $isoPath) {
    Write-Host "[PASS]: ISO found at $isoPath" -ForegroundColor Green
} else {
    Write-Host "[FAIL]: ISO NOT found at $isoPath. Run 'prepare iso' first." -ForegroundColor Red
}

# 5. Check System Memory
$os = Get-WmiObject Win32_OperatingSystem
$freeMem = [math]::round($os.FreePhysicalMemory / 1024, 0)
Write-Host "[4/4] Available System Memory: $freeMem MB" -ForegroundColor White
if ($freeMem -lt 2048) {
    Write-Host "[WARN]: Low memory. This may prevent the VM from starting." -ForegroundColor Yellow
}

Write-Host "`nDiagnostics Complete. If everything is PASS, run the deploy_hyperv.ps1 script as Administrator." -ForegroundColor Cyan
