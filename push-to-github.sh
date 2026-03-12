#!/bin/bash
# GenX FX - Push to GitHub
# Run this in the Replit Shell: bash push-to-github.sh

REPO="https://$GITHUB_TOKEN@github.com/nuna69v-cell/A6..9V-GenX_FX.main.git"

echo "=== GenX FX GitHub Push ==="
echo "Target: github.com/nuna69v-cell/A6..9V-GenX_FX.main"

# Remove stale lock if present
[ -f .git/index.lock ] && rm -f .git/index.lock && echo "Cleared git lock"

# Configure git identity
git config user.email "lengkundee01@gmail.com"
git config user.name "GenX FX Trading System"

# Set remote (remove old if exists)
git remote remove github 2>/dev/null || true
git remote add github "$REPO"

# Stage all changes
git add -A

# Commit
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "GenX FX Dashboard update - $TIMESTAMP" || echo "Nothing new to commit"

# Push
echo "Pushing to GitHub..."
git push github HEAD:main --force
echo "Done! View at: https://github.com/nuna69v-cell/A6..9V-GenX_FX.main"
