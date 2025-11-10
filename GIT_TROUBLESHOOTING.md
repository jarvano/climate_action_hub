# 🚨 Git Installation Troubleshooting Guide

## Current Issue: Git Not Found

Git is not recognized in your system PATH. Here's how to fix this:

## 🔧 Step 1: Verify Git Installation

### **Check if Git is installed:**
1. Press `Windows + R`, type `appwiz.cpl` and press Enter
2. Look for "Git" in the list of installed programs
3. If NOT found: Download and install Git from https://git-scm.com/download/win
4. If FOUND: Proceed to Step 2 to fix PATH

## 🔧 Step 2: Fix System PATH

### **Option A: Add Git to PATH manually**
1. Find your Git installation folder (usually `C:\Program Files\Git\bin`)
2. Press `Windows + S`, search for "Environment Variables"
3. Click "Edit the system environment variables"
4. Click "Environment Variables"
5. Under "System variables", find and select "Path", click "Edit"
6. Click "New" and add: `C:\Program Files\Git\bin`
7. Click "New" again and add: `C:\Program Files\Git\cmd`
8. Click "OK" on all windows
9. **Restart your terminal/computer**

### **Option B: Reinstall Git with PATH setup**
1. Download Git installer: https://git-scm.com/download/win
2. Run the installer
3. **Important**: On the "Adjusting your PATH environment" screen, select:
   - ✅ "Git from the command line and also from 3rd-party software"
4. Complete installation
5. **Restart your terminal**

## 🔧 Step 3: Verify Git Works

After restart, test in a NEW terminal:
```bash
git --version
```

Should output something like: `git version 2.40.0`

## 🚀 Alternative: Use GitHub Desktop

If command-line Git continues to be problematic:

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Use the GUI to create and manage your repository
4. Or use GitHub Desktop to handle authentication, then use command line

## 📝 Manual Git Commands (Once Working)

Once Git is working, here are the exact commands to push your project:

```bash
# Navigate to your project directory
cd c:\Users\OKURO_67\Documents\trae_projects\climate_action

# Initialize git repository
git init

# Configure your identity (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files (respects .gitignore)
git add .

# Create initial commit
git commit -m "🚀 Initial commit: Climate Action Hub with CO2 emissions dashboard

Features:
- Interactive CO2 emissions dashboard with real data
- Responsive design for mobile, tablet, and desktop
- Data visualization with Chart.js
- Python backend with built-in HTTP server
- Real data processing from OWID CO2 dataset
- Forecasting capabilities (2025-2030)
- Modern UI/UX with glassmorphism design"

# Create GitHub repository first at https://github.com/new
# Then add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/climate-action-hub.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🎯 Verification Steps

After each step, verify:
1. **Git installation**: `git --version`
2. **PATH fix**: `where git` (should show path)
3. **Configuration**: `git config --list`
4. **Repository status**: `git status`

## 🆘 Still Having Issues?

### **Try Git Bash:**
1. Search for "Git Bash" in Start Menu
2. Open Git Bash terminal
3. Navigate to your project: `cd /c/Users/OKURO_67/Documents/trae_projects/climate_action`
4. Run the git commands there

### **Check Windows Version:**
- Some older Windows versions need different Git installers
- Try both 64-bit and 32-bit versions from git-scm.com

### **Alternative Solutions:**
- Use Windows Subsystem for Linux (WSL)
- Use Git through Python's `gitpython` library
- Upload files manually through GitHub web interface (last resort)

## 📞 Need Help?

Once Git is working, continue with the GitHub push process. The project files are ready and waiting!