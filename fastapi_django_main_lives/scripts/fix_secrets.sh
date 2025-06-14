#!/bin/bash

# Script to securely regenerate .env file after secret exposure
# This script helps you safely create a new .env file with fresh secrets

echo "🚨 SECURITY: Regenerating .env file with new secrets"
echo "========================================================="

# Backup the current .env (without secrets)
if [ -f .env ]; then
    echo "📄 Backing up current .env to .env.backup"
    cp .env .env.backup
fi

# Copy template
echo "📋 Creating new .env from template"
cp .env.example .env

echo ""
echo "🔧 REQUIRED ACTIONS:"
echo "==================="
echo ""
echo "1. 🔑 Generate new GitHub Personal Access Token:"
echo "   → Go to: https://github.com/settings/tokens"
echo "   → Generate new token (classic)"
echo "   → Select required scopes: repo, workflow, admin:org"
echo "   → Replace 'ghp_your_github_personal_access_token' in .env"
echo ""
echo "2. 🔑 Generate new Google Cloud Service Account:"
echo "   → Go to: https://console.cloud.google.com/iam-admin/serviceaccounts"
echo "   → Create new service account"
echo "   → Download JSON key file"
echo "   → Store as 'service-account-key.json' (NOT in git)"
echo "   → Update GOOGLE_APPLICATION_CREDENTIALS path in .env"
echo ""
echo "3. 🔄 Update other API keys if compromised:"
echo "   → Groq API key"
echo "   → HuggingFace token"
echo "   → Any other sensitive tokens"
echo ""
echo "4. 📝 Edit .env file with your actual values"
echo ""
echo "5. ✅ Verify .env is in .gitignore (already done)"
echo ""
echo "⚠️  NEVER commit the .env file to version control!"
echo "⚠️  The exposed tokens have been invalidated and must be regenerated!"

echo ""
echo "🔧 Next steps after updating .env:"
echo "================================="
echo "1. Remove .env from git history: git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all"
echo "2. Force push (DANGEROUS): git push origin --force --all"
echo "3. Test application: python app.py"
echo ""
echo "📧 Contact your team to update any shared secrets!"
