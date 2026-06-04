$repos = Get-ChildItem -Path C:/GitHub -Directory
foreach ($repo in $repos) {
    $repoPath = $repo.FullName
    if (Test-Path "$repoPath/.git") {
        Write-Host "`n[SYNC] Processing repository: $($repo.Name)" -ForegroundColor Cyan
        Set-Location $repoPath
        
        # Determine branch
        $branch = git branch --show-current
        if (-not $branch) { $branch = "main" }
        Write-Host "[SYNC] Target Branch: $branch" -ForegroundColor Gray

        # Silence advice and stage changes
        git config advice.addEmbeddedRepo false
        git add .
        
        # Check for changes to commit
        $status = git status --porcelain
        if ($status) {
            Write-Host "[SYNC] Changes detected. Committing..." -ForegroundColor Yellow
            git commit -m "Supreme Finality Sync | Global Workspace Alignment"
        } else {
            Write-Host "[SYNC] No changes to commit." -ForegroundColor Gray
        }

        # Force push for absolute alignment
        Write-Host "[SYNC] Pushing to origin/$branch..." -ForegroundColor Green
        git push origin $branch --force --verbose
    }
}
Set-Location C:/GitHub/SpartanAI_Hub_Master
Write-Host "`n[+] GLOBAL SYNC COMPLETE." -ForegroundColor Green
