#!/bin/bash
# Clean and push Planetary repo

# Make sure we're in repo root
cd "$(dirname "$0")" || exit

# Remove logs from git
git rm -r --cached artifacts/storage/outputs/logs/ 2>/dev/null

# Update .gitignore to ignore logs
echo "artifacts/storage/outputs/logs/" >> .gitignore

# Add everything else
git add .

# Commit cleanly
git commit -m "Clean commit: remove logs, update .gitignore"

# Ensure main branch
git branch -M main

# Set remote
git remote set-url origin https://github.com/cygel-co/FacePrintPay.git

# Push to GitHub
git push -u origin main
