# GitPush Tool - Complete Documentation

## 📦 Installation
```bash
pip install gitpush-tool
gh auth login  # Authenticate with GitHub
```

## 🚀 Core Features

### 1. New Repository Creation
```bash
# Create public repo
gitpush_tool "Initial commit" --new-repo my-project

# Create private repo
gitpush_tool "Initial commit" --new-repo private-project --private
```

### 2. Standard Git Operations
```bash
# Regular push
gitpush_tool "Fixed login bug"

# Force push
gitpush_tool "Rebased history" --force

# Push tags
gitpush_tool --tags
```

## ⚙️ Configuration

The tool automatically:
1. Creates `.gitignore` with sensible defaults
2. Sets main branch as default
3. Uses GitHub CLI for secure auth

## 🐛 Common Issues

**"Repository already exists"**
```bash
❌ Repository 'my-repo' already exists
```
Solution: Use different name or delete existing repo

**"Authentication failed"**
```bash
❌ Failed to authenticate with GitHub
```
Solution: Run `gh auth login` separately

## 📝 License
MIT Licensed - Free for personal and commercial use