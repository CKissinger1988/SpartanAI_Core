# SpartanAI Boot Sequence
# Automatically launches the creator dashboard and updater service.

$SpartanPath = "C:\Users\ckiss\SpartanAI"
$Launcher = "run_app.py"

# Start SpartanAI in background
Start-Process python -ArgumentList "$SpartanPath\$Launcher" -WindowStyle Hidden

# Trigger updater
Invoke-Expression "C:\Users\ckiss
ebrand.ps1"
