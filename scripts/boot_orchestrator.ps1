# SentinelAI Boot Sequence
# Automatically launches the creator dashboard and updater service.

$SentinelPath = "C:\Users\ckiss\SentinelAI"
$Launcher = "run_app.py"

# Start SentinelAI in background
Start-Process python -ArgumentList "$SentinelPath\$Launcher" -WindowStyle Hidden

# Trigger updater
Invoke-Expression "C:\Users\ckiss
ebrand.ps1"
