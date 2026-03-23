#!/bin/bash

# AdugboInsure Website Deployment Script
# This script automates the GitHub push and Vercel deployment
# Prerequisites:
# - GitHub repository must be created at: https://github.com/koladeg/adugboinsure-website
# - You must be authenticated with both git and Vercel

set -e  # Exit on any error

PROJECT_DIR="/home/claw/.openclaw/workspace/adugboinsure"
GITHUB_REPO="https://github.com/koladeg/adugboinsure-website.git"
REPO_NAME="adugboinsure-website"

echo "🚀 AdugboInsure Deployment Script"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}→ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Step 1: Verify project directory
print_step "Checking project directory..."
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Project directory not found: $PROJECT_DIR"
    exit 1
fi
print_success "Project directory found"

# Step 2: Check git status
print_step "Verifying git repository..."
cd "$PROJECT_DIR"
if ! git status > /dev/null 2>&1; then
    print_error "Git repository not initialized"
    exit 1
fi
print_success "Git repository valid"

# Step 3: Verify remote
print_step "Setting up GitHub remote..."
git remote remove origin 2>/dev/null || true
git remote add origin "$GITHUB_REPO"
git remote -v
print_success "Remote configured"

# Step 4: Verify GitHub repo exists
print_step "Checking if GitHub repository exists..."
if ! git ls-remote --heads "$GITHUB_REPO" > /dev/null 2>&1; then
    print_error "GitHub repository not found or not accessible"
    print_info "Please create the repository at: https://github.com/new"
    print_info "Repository name: $REPO_NAME"
    exit 1
fi
print_success "GitHub repository is accessible"

# Step 5: Push to GitHub
print_step "Pushing code to GitHub..."
git push -u origin main
print_success "Code pushed to GitHub"

# Step 6: Verify push
print_step "Verifying push..."
if git ls-remote --heads origin main | grep -q "main"; then
    print_success "Code verified on GitHub"
else
    print_error "Could not verify push to GitHub"
    exit 1
fi

# Step 7: Deploy to Vercel
print_step "Preparing Vercel deployment..."
if ! command -v vercel &> /dev/null; then
    print_error "Vercel CLI not found"
    print_info "Install with: npm install -g vercel"
    exit 1
fi
print_success "Vercel CLI found"

# Step 8: Execute Vercel deployment
print_step "Deploying to Vercel (this may take a minute)..."
vercel --prod

# Step 9: Get deployment info
print_step "Retrieving deployment information..."
VERCEL_URL=$(vercel list --json 2>/dev/null | grep -o '"url":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$VERCEL_URL" ]; then
    print_info "Could not auto-retrieve Vercel URL"
    print_info "Check your Vercel dashboard: https://vercel.com/dashboard"
else
    print_success "Deployment successful!"
fi

# Final summary
echo ""
echo "=================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "=================================="
echo ""
echo "📍 Your project is now deployed:"
echo ""
echo -e "  GitHub:  ${BLUE}https://github.com/koladeg/$REPO_NAME${NC}"
echo -e "  Vercel:  ${BLUE}https://vercel.com/dashboard${NC}"
echo ""
echo "Next steps:"
echo "  1. Visit your Vercel project to view logs"
echo "  2. Enable auto-deployment in Vercel settings"
echo "  3. Add custom domain if needed"
echo "  4. Configure environment variables if needed"
echo ""
echo "Questions? Check DEPLOYMENT_INSTRUCTIONS.md"
echo ""
