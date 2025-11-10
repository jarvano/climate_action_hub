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
    Read-Host "Press Enter to exit"
    exit 1
}

# Get user information
Write-Host "`n👤 Git Configuration Setup" -ForegroundColor Yellow
Write-Host "==========================" -ForegroundColor Yellow

$gitName = Read-Host "Enter your GitHub username (or full name)"
$gitEmail = Read-Host "Enter your GitHub email address"

# Configure Git
git config --global user.name "$gitName"
git config --global user.email "$gitEmail"

Write-Host "✅ Git configured for $gitName <$gitEmail>" -ForegroundColor Green

# Initialize Git repository
Write-Host "`n📁 Initializing Git Repository" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "⚠️  Git repository already exists" -ForegroundColor Yellow
} else {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Add all files
Write-Host "`n📋 Adding Files to Git" -ForegroundColor Yellow
Write-Host "======================" -ForegroundColor Yellow

# Add all files except those in .gitignore
git add .

# Check if there are files to commit
$status = git status --porcelain
if ([string]::IsNullOrEmpty($status)) {
    Write-Host "⚠️  No files to commit (repository may already be set up)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Files staged for commit:" -ForegroundColor Green
    git status --short
}

# Create initial commit
Write-Host "`n💾 Creating Initial Commit" -ForegroundColor Yellow
Write-Host "==========================" -ForegroundColor Yellow

$commitMessage = "🚀 Initial commit: Climate Action Hub with CO2 emissions dashboard"
git commit -m "$commitMessage"

Write-Host "✅ Initial commit created successfully!" -ForegroundColor Green
Write-Host "`n🎉 Git repository setup complete!" -ForegroundColor Green

# GitHub repository creation instructions
Write-Host "`n🌐 Next Steps - GitHub Repository" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "1. Go to https://github.com/new" -ForegroundColor White
Write-Host "2. Create a new repository named 'climate-action-hub'" -ForegroundColor White
Write-Host "3. DON'T initialize with README (we already have one)" -ForegroundColor White
Write-Host "4. After creating, run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/$gitName/climate-action-hub.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "5. 🌍 Your Climate Action Hub will be live on GitHub!" -ForegroundColor Green

Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "- ✅ Git configured" -ForegroundColor Green
Write-Host "- ✅ Repository initialized" -ForegroundColor Green
Write-Host "- ✅ Files committed" -ForegroundColor Green
Write-Host "- 🔄 Ready to push to GitHub" -ForegroundColor Yellow

Read-Host "`nPress Enter to exit the setup script"