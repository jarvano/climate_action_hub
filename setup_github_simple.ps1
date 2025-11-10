# Climate Action Hub - GitHub Setup Script
# This script handles Git initialization and GitHub setup

Write-Host "🚀 Climate Action Hub - GitHub Setup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Add Git to PATH for this session
$env:PATH = "$env:PATH;C:\Program Files\Git\bin"

# Check if Git is available
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found. Please install Git from https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# Initialize Git repository
Write-Host "`n📁 Initializing Git Repository" -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "⚠️  Git repository already exists" -ForegroundColor Yellow
} else {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Add all files
Write-Host "`n📋 Adding Files to Git" -ForegroundColor Yellow
git add .

# Create initial commit
Write-Host "`n💾 Creating Initial Commit" -ForegroundColor Yellow
git commit -m "🚀 Initial commit: Climate Action Hub with CO2 emissions dashboard"

Write-Host "✅ Initial commit created successfully!" -ForegroundColor Green

# Get current directory name for GitHub repo suggestion
$repoName = Split-Path -Leaf (Get-Location)

Write-Host "`n🌐 Next Steps - Create GitHub Repository:" -ForegroundColor Cyan
Write-Host "1. Go to https://github.com/new" -ForegroundColor White
Write-Host "2. Create repository named: $repoName" -ForegroundColor White
Write-Host "3. Don't initialize with README" -ForegroundColor White
Write-Host "4. After creating, run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/$repoName.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 Your Climate Action Hub will be live on GitHub!" -ForegroundColor Green