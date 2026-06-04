$githubRoot = "C:\GitHub"
$repos = Get-ChildItem -Path $githubRoot -Directory

foreach ($repo in $repos) {
    Write-Host "--- Cleaning Repository: $($repo.Name) ---" -ForegroundColor Cyan
    Set-Location $repo.FullName

    # 1. Git Garbage Collection
    if (Test-Path ".git") {
        Write-Host "[*] Running Git GC..."
        git gc --aggressive --prune=now
    }

    # 2. Delete known bloat directories
    $targets = @("node_modules", "venv", ".vs", "bin", "obj", "__pycache__", ".next", "dist", "build")
    foreach ($target in $targets) {
        if (Test-Path $target) {
            Write-Host "[-] Removing $target..."
            Remove-Item -Path $target -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    # 3. Specific large file cleanup (logs, temp)
    Get-ChildItem -Path . -Include "*.log", "*.tmp", "*.bak" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
}

Write-Host "--- Total Storage Optimization Complete ---" -ForegroundColor Green
