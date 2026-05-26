# SpartanAI Hyper-V Deployment Orchestrator (v50-SUPREME) - FIXED
# MANDATE: Automate the creation and initialization of the SpartanAI Sovereign VM.

$VMName = "JarvisAI_GodMode_Server"
$ISOPath = "C:\GitHub\JarvisAI_Server_GodMode.iso"
$VHDPath = "C:\Users\Public\Documents\Hyper-V\Virtual Hard Disks\$VMName.vhdx"
$Memory = 2GB # Reduced to 2GB to ensure resource compatibility
$SwitchName = "Default Switch"

Write-Host "[HYPER-V]: Initiating Sovereign VM Deployment..." -ForegroundColor Cyan

# 1. Cleanup existing VM if it failed to start or was partially created
if (Get-VM -Name $VMName -ErrorAction SilentlyContinue) {
    Write-Host "[HYPER-V]: Removing existing partially created VM..." -ForegroundColor Yellow
    Remove-VM -Name $VMName -Force
}

# 2. Create VM (Gen 2)
New-VM -Name $VMName -MemoryStartupBytes $Memory -Generation 2 -Path "C:\Users\Public\Documents\Hyper-V" -SwitchName $SwitchName

# 3. Create and Attach VHDX
if (-not (Test-Path $VHDPath)) {
    New-VHD -Path $VHDPath -SizeBytes 50GB -Dynamic
}
Add-VMHardDiskDrive -VMName $VMName -Path $VHDPath

# 4. Mount SpartanAI ISO
Add-VMDvdDrive -VMName $VMName -Path $ISOPath

# 5. Configure Boot Order (DVD first)
$DVD = Get-VMDvdDrive -VMName $VMName
Set-VMFirmware -VMName $VMName -FirstBootDevice $DVD -EnableSecureBoot Off

# 6. Finalize and Start
Write-Host "[HYPER-V]: Deployment Successful. Launching SpartanAI..." -ForegroundColor Green
Start-VM -Name $VMName

# 7. Open VM Console
Write-Host "[HYPER-V]: Opening Sovereign Console..." -ForegroundColor Cyan
vmconnect.exe localhost $VMName
