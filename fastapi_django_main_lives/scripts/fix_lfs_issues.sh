#!/bin/bash

# Fix LFS issues by properly migrating files to LFS
set -e

echo "🔧 Fixing LFS issues..."

# Create a backup of current state
git stash push -m "Backup before LFS fix"

# Remove all files from git index (but keep in working directory)
git rm -r --cached .

# Re-add files, this time respecting .gitattributes LFS rules
git add .

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "🔧 Fix LFS issues: properly migrate files to LFS"
    echo "✅ LFS issues fixed and committed"
else
    echo "ℹ️ No changes detected after LFS migration"
fi

# Verify LFS status
echo "📊 Current LFS status:"
git lfs status

echo "🎉 LFS fix complete!"
