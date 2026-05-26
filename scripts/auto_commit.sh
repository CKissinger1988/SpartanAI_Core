#!/bin/bash
# SpartanAI Auto-Commit Monitor
# Runs every 60 minutes to capture workspace state.

while true; do
    echo "Running periodic commit..."
    git add .
    if ! git diff-index --quiet HEAD --; then
        git commit -m "chore(auto): periodic workspace synchronization"
        git push origin main
        echo "Periodic commit successful."
    else
        echo "No changes to commit."
    fi
    sleep 3600
done
