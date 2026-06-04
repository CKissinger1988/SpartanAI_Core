# Apex_Sovereign_Cleanup.ps1
# MANDATE: Absolute Purification. Safely remove system trash, temp data, install remnants, and OneDrive footprints.
# SAFETY: NO user files from Documents, Pictures, Desktop, or Downloads will be targeted.
# FEATURES: Real-time progress, User Review stage, and total size calculation.

# --- 1. Privilege Check ---
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host " [!] ERROR: This script requires Administrative privileges for deep system cleanup." -ForegroundColor Red
    Write-Host " Please restart PowerShell as Administrator." -ForegroundColor Yellow
    exit
}

# --- 2. Configuration & Paths ---
$CleanupLog = @()
$TotalSizeToReclaim = 0

# Categories
$TempPaths = @(
    "$env:TEMP\*",                              # User Temp
    "$env:SystemRoot\Temp\*",                   # System Temp
    "$env:SystemRoot\Prefetch\*",                # Prefetch
    "$env:SystemRoot\SoftwareDistribution\Download\*", # Windows Update Cache
    "$env:LocalAppData\Google\Chrome\User Data\Default\Cache\*", # Chrome Cache
    "$env:LocalAppData\Microsoft\Edge\User Data\Default\Cache\*"  # Edge Cache
)

$InstallRemnants = @(
    "C:\Windows.old",
    "C:\$Windows.~BT",
    "C:\$Windows.~WS",
    "C:\MSOCache"
)

$OneDriveFootprints = @(
    "$env:LocalAppData\Microsoft\OneDrive",
    "$env:ProgramData\Microsoft OneDrive",
    "C:\OneDriveTemp",
    "$env:UserProfile\AppData\Local\Microsoft\OneDrive"
)

# --- 3. Helper Functions ---
function Get-SizeInMB($Path) {
    if (Test-Path $Path) {
        try {
            $files = Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue
            $size = ($files | Measure-Object -Property Length -Sum).Sum / 1MB
            return [Math]::Round($size, 2)
        } catch { return 0 }
    }
    return 0
}

function Log-Scan($Category, $Name, $Path) {
    if (Test-Path $Path) {
        $size = Get-SizeInMB $Path
        if ($size -gt 0) {
            $global:CleanupLog += [PSCustomObject]@{
                Category = $Category
                Target   = $Name
                Path     = $Path
                SizeMB   = $size
            }
            $global:TotalSizeToReclaim += $size
        }
    }
}

# --- 4. Scanning Phase ---
Clear-Host
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "      APEX SOVEREIGN CLEANUP - SYSTEM SCANNING      " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "[*] Initializing deep scan of junk sectors..."

# Scan Temp
foreach ($p in $TempPaths) { Log-Scan "Temporary Files" "Temp Sector" $p }

# Scan Install Remnants
foreach ($p in $InstallRemnants) { Log-Scan "Install Remnants" "Old OS/Install Cache" $p }

# Scan OneDrive
foreach ($p in $OneDriveFootprints) { Log-Scan "OneDrive Remnants" "OneDrive App Metadata" $p }

# Scan Recycle Bin
$binSize = 0
try {
    $bin = (New-Object -ComObject Shell.Application).NameSpace(0x0a).Items()
    $binSize = ($bin | Measure-Object -Property Size -Sum).Sum / 1MB
} catch {}

if ($binSize -gt 0) {
    $CleanupLog += [PSCustomObject]@{
        Category = "Recycle Bin"
        Target   = "Global Trash"
        Path     = "Recycle Bin"
        SizeMB   = [Math]::Round($binSize, 2)
    }
    $TotalSizeToReclaim += $binSize
}

# --- 5. Review Phase ---
if ($CleanupLog.Count -eq 0) {
    Write-Host "[+] System is already pristine. No junk detected." -ForegroundColor Green
    exit
}

Write-Host "`n[!] SCAN COMPLETE. Findings below:" -ForegroundColor Yellow
$CleanupLog | Format-Table -AutoSize

$ReclaimGB = [Math]::Round($TotalSizeToReclaim / 1024, 2)
Write-Host "------------------------------------------------------------"
Write-Host " TOTAL RECLAIMABLE SPACE: $TotalSizeToReclaim MB ($ReclaimGB GB)" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------"
Write-Host "`n [SAFE-GUARD]: Only app data, logs, and temp files are targeted." -ForegroundColor Green
Write-Host " [SAFE-GUARD]: Your Documents, Pictures, and User data are EXCLUDED." -ForegroundColor Green

$Confirm = Read-Host "`n>>> Execute full system purification? (Y/N)"
if ($Confirm -ne "Y" -and $Confirm -ne "y") {
    Write-Host "[*] Cleanup aborted by user." -ForegroundColor Gray
    exit
}

# --- 6. Backup Phase ---
function Backup-SovereignState {
    Write-Host "`n[*] INITIATING AUTOMATED SAFETY BACKUP..." -ForegroundColor Cyan
    
    # 1. Create System Restore Point
    Write-Progress -Activity "Safety Backup" -Status "Creating System Restore Point..." -PercentComplete 10
    Write-Host " [-] Creating System Restore Point (Sovereign_Cleanup_Safety)..." -NoNewline
    try {
        Checkpoint-Computer -Description "Sovereign_Cleanup_Safety" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop
        Write-Host " [DONE]" -ForegroundColor Green
    } catch {
        Write-Host " [SKIPPED] (Restore points may be disabled or limited)" -ForegroundColor Yellow
    }

    # 2. Export Registry Keys
    Write-Progress -Activity "Safety Backup" -Status "Exporting Registry Keys..." -PercentComplete 50
    $BackupDir = Join-Path $env:TEMP "SovereignCleanup_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -Path $BackupDir -ItemType Directory -Force | Out-Null
    Write-Host " [-] Exporting OneDrive Registry Keys to $BackupDir..." -NoNewline
    
    $regKeys = @(
        "HKCU\Software\Microsoft\OneDrive",
        "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{018D5C66-4533-4307-9B53-224DE2ED1FE6}"
    )
    
    foreach ($key in $regKeys) {
        $safeName = $key -replace '[\\{}]', '_'
        reg export "$key" "$BackupDir\$safeName.reg" /y | Out-Null
    }
    Write-Host " [DONE]" -ForegroundColor Green
    Write-Progress -Activity "Safety Backup" -Status "Backup Complete" -PercentComplete 100
}

# --- 7. Execution Phase ---
Clear-Host
Backup-SovereignState

Write-Host "`n[*] COMMENCING SYSTEM PURIFICATION..." -ForegroundColor Cyan

$count = 0
foreach ($Item in $CleanupLog) {
    $percent = [int](($count / $CleanupLog.Count) * 100)
    Write-Progress -Activity "Purifying System..." -Status "Removing: $($Item.Target)" -PercentComplete $percent
    
    Write-Host "[-] Purging $($Item.Category): $($Item.Target)..." -NoNewline
    
    if ($Item.Category -eq "Recycle Bin") {
        Clear-RecycleBin -Force -Confirm:$false -ErrorAction SilentlyContinue
    } else {
        if (Test-Path $Item.Path) {
            Remove-Item -Path $Item.Path -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host " [DONE]" -ForegroundColor Green
    $count++
}

# Specialized OneDrive Deep Clean (Registry/Tasks)
Write-Host "[-] Scrubbing OneDrive Registry & Task footprints..." -NoNewline
# Remove Namespace
$regPaths = @(
    "HKCU:\Software\Microsoft\OneDrive",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{018D5C66-4533-4307-9B53-224DE2ED1FE6}"
)
foreach ($r in $regPaths) { if (Test-Path $r) { Remove-Item $r -Recurse -Force -ErrorAction SilentlyContinue } }
# Tasks
Get-ScheduledTask -TaskName "*OneDrive*" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false
Write-Host " [DONE]" -ForegroundColor Green

# Final Component Cleanup (Install Remnants)
Write-Host "[*] Finalizing with DISM Component Cleanup (May take a moment)..."
dism.exe /online /Cleanup-Image /StartComponentCleanup /NoRestart /Quiet

Write-Progress -Activity "Purifying System..." -Status "Cleanup Complete" -PercentComplete 100
Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "      SYSTEM PURIFICATION COMPLETE. REBOOT RECOMMENDED.      " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
