@echo off
echo 🚀 Climate Action Hub - GitHub Push Script
echo ========================================
echo.

REM Check if Git is available
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not found in PATH!
    echo Please install Git or add it to your PATH
    echo See GIT_TROUBLESHOOTING.md for help
    pause
    exit /b 1
)

echo ✅ Git found!
git --version
echo.

REM Navigate to project directory
cd /d "%~dp0"
echo 📁 Working directory: %cd%
echo.

REM Initialize Git repository
echo 🔧 Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize Git repository
    pause
    exit /b 1
)

REM Configure Git (user will be prompted)
echo.
echo 👤 Git Configuration Setup
echo Please enter your GitHub username (e.g., "John Doe"):
set /p git_name=
git config user.name "%git_name%"

echo Please enter your GitHub email:
set /p git_email=
git config user.email "%git_email%"

REM Add all files
echo.
echo 📦 Adding project files...
git add .
if %errorlevel% neq 0 (
    echo ❌ Failed to add files
    pause
    exit /b 1
)

REM Create initial commit
echo.
echo 💾 Creating initial commit...
git commit -m "🚀 Initial commit: Climate Action Hub with CO2 emissions dashboard

Features:
- Interactive CO2 emissions dashboard with real data
- Responsive design for mobile, tablet, and desktop
- Data visualization with Chart.js
- Python backend with built-in HTTP server
- Real data processing from OWID CO2 dataset
- Forecasting capabilities (2025-2030)
- Modern UI/UX with glassmorphism design"

if %errorlevel% neq 0 (
    echo ❌ Failed to create commit
    pause
    exit /b 1
)

echo.
echo ✅ Repository initialized and committed successfully!
echo.
echo 🌐 Next steps:
echo 1. Create a repository at https://github.com/new
echo 2. Name it: climate-action-hub
echo 3. Copy the repository URL (e.g., https://github.com/YOUR_USERNAME/climate-action-hub.git)
echo 4. Run: git remote add origin YOUR_REPOSITORY_URL
echo 5. Run: git branch -M main
echo 6. Run: git push -u origin main
echo.
echo See GITHUB_SETUP.md for detailed instructions!
echo.
pause