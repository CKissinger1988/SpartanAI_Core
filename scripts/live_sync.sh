#!/bin/bash
cd ~/SpartanAI_Core
git pull origin main
if [ ! -d "SpartanAI_Hub_Master" ]; then
    git clone https://github.com/CKissinger1988/SpartanAI_Hub_Master.git SpartanAI_Hub_Master
else
    cd SpartanAI_Hub_Master
    git pull origin main
    cd ..
fi
