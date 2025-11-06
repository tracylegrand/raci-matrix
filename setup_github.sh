#!/bin/bash

# Script to set up GitHub repository for RACI Matrix Builder
# Run this after creating your GitHub repository

echo "🚀 Setting up GitHub repository for RACI Matrix Builder"
echo ""

# Check if remote is already set
if git remote -v | grep -q "origin"; then
    echo "⚠️  Remote 'origin' already exists. Removing it..."
    git remote remove origin
fi

# Prompt for GitHub username and repo name
echo "Please provide your GitHub information:"
read -p "GitHub username: " GITHUB_USERNAME
read -p "Repository name (e.g., raci-matrix): " REPO_NAME

# Set up remote
echo ""
echo "📡 Adding remote repository..."
git remote add origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

# Show remote
echo ""
echo "✅ Remote configured:"
git remote -v

echo ""
echo "📤 Ready to push! Run the following command:"
echo "   git push -u origin main"
echo ""
echo "Or if you want to push now, type 'y' and press Enter:"
read -p "Push now? (y/n): " PUSH_NOW

if [ "$PUSH_NOW" = "y" ] || [ "$PUSH_NOW" = "Y" ]; then
    echo ""
    echo "📤 Pushing to GitHub..."
    git push -u origin main
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo "🌐 Your app can now be deployed at: https://share.streamlit.io"
    else
        echo ""
        echo "❌ Push failed. Make sure:"
        echo "   1. You've created the repository on GitHub"
        echo "   2. Your GitHub credentials are configured"
        echo "   3. You have push access to the repository"
    fi
else
    echo ""
    echo "You can push later with: git push -u origin main"
fi



