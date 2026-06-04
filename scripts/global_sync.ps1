$repos = Get-ChildItem -Path C:/GitHub -Directory
foreach ($repo in $repos) {
    $repoPath = $repo.FullName
    if (Test-Path "$repoPath/.git") {
        Write-Host "Processing $repoPath..." -ForegroundColor Cyan
        Set-Location $repoPath
        
        # Check current branch
        $branch = git branch --show-current
        if (-not $branch) { $branch = "main" }
        
        # Add and commit with auto-ignore for submodules that cause issues
        git config set advice.addEmbeddedRepo false
        git add .
        git commit -m "Supreme Finality Sync"
        
        Write-Host "Pushing to origin/$branch..." -ForegroundColor Green
        git push origin $branch --force
    }
}
Set-Location C:/GitHub/SpartanAI_Hub_Master
