cd /d D:\SpartanAI_Core
git pull origin main
if (-not (Test-Path SpartanAI_Hub_Master)) {
    git clone https://github.com/CKissinger1988/SpartanAI_Hub_Master.git SpartanAI_Hub_Master
} else {
    Push-Location SpartanAI_Hub_Master
    git pull origin main
    Pop-Location
}
