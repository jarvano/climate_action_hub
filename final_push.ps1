# Climate Action Hub - Final GitHub Push Script
# This script will help you push your code to GitHub

Write-Host "🚀 Climate Action Hub - Final GitHub Push" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Add Git to PATH
$env:PATH = "$env:PATH;C:\Program Files\Git\bin"

# Check Git
$gitVersion = git --version
Write-Host "✅ Git version: $gitVersion" -ForegroundColor Green

# Get GitHub username
$gitHubUser = git config user.name
Write-Host "👤 GitHub username: $gitHubUser" -ForegroundColor Green

# Remove existing remote (if it exists)
git remote remove origin 2>$null
Write-Host "✅ Removed existing remote" -ForegroundColor Green

# Create the correct remote URL
$repoName = "climate-action-hub"
$remoteUrl = "https://github.com/$gitHubUser/$repoName.git"

Write-Host "`n🌐 Repository URL: $remoteUrl" -ForegroundColor Cyan
Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com/new" -ForegroundColor White
Write-Host "2. Create repository named: $repoName" -ForegroundColor White
Write-Host "3. Don't initialize with README (we have one)" -ForegroundColor White
Write-Host "4. Come back here and press Enter to continue..." -ForegroundColor White

Read-Host "`nPress Enter when ready to push to GitHub"

# Add the remote
git remote add origin $remoteUrl
Write-Host "✅ Remote added successfully" -ForegroundColor Green

# Push to GitHub
Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "This may take a moment due to the large data file..." -ForegroundColor Yellow

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n🎉 SUCCESS! Your Climate Action Hub is now live on GitHub!" -ForegroundColor Green
    Write-Host "Repository URL: https://github.com/$gitHubUser/$repoName" -ForegroundColor Cyan
    Write-Host "`n🌍 Share your project and make a difference!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Push failed. Common issues:" -ForegroundColor Red
    Write-Host "1. Repository doesn't exist yet" -ForegroundColor Yellow
    Write-Host "2. Authentication required" -ForegroundColor Yellow
    Write-Host "3. Network issues" -ForegroundColor Yellow
    Write-Host "`nTry running: git push -u origin main" -ForegroundColor Cyan
}

Read-Host "`nPress Enter to exit"