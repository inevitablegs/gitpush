# GitPush Tool 🚀

[![PyPI version](https://img.shields.io/pypi/v/gitpush-tool.svg)](https://pypi.org/project/gitpush-tool/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/inevitablegs/gitpush/blob/main/LICENSE)

A supercharged Git CLI tool that simplifies repository creation and pushing with intelligent defaults. It's designed to automate the tedious parts of starting a new project and streamline your daily Git workflow.

---

## ✨ Features

- **One-Command Setup:** Create a new GitHub repository and push your project in a single command.
- **Automatic Git Initialization:** No need to run `git init` or `git add` separately for new projects.
- **Safe Force Pushing:** Uses `--force-with-lease` by default to prevent accidentally overwriting collaborators' work.
- **Seamless GitHub CLI Integration:** Leverages `gh` for secure, persistent authentication.
- **Smart Defaults:** Automatically creates a `.gitignore`, adds a remote, and sets up your main branch.
- **Comprehensive Error Handling:** Provides clear, actionable feedback for common issues.

---

## 📦 Installation

This tool requires the official **GitHub CLI (`gh`)** to be installed and authenticated.

```bash
# 1. Install the tool
pip install gitpush-tool

# 2. Authenticate with GitHub (if you haven't already)
gh auth login
```

---

## 🛠️ Usage

### **Basic Commands**

| Command | Description |
|---------|-------------|
| `gitpush "Commit message"` | Adds all changes, commits, and pushes to the current branch. |
| `gitpush` | Pushes already staged/committed changes (no new commit is made). |
| `gitpush --force` | Performs a safe force push (`--force-with-lease`). |
| `gitpush --tags` | Pushes all your local tags to the remote. |

---

### **New Repository Workflow**

From an uninitialized directory, create a new GitHub repository and push your code in **one step**.

```bash
# Create a new public repository
gitpush "Initial commit" --new-repo my-awesome-project

# Create a private repository with a description
gitpush "Initial commit" --new-repo my-secret-project --private --description "A project for my eyes only."
```

---

### **Branch Management**

```bash
# Push "New feature" commit to a branch named 'feature-x'
gitpush "New feature" feature-x

# Push to a specific remote ('upstream') and branch ('main')
gitpush "Sync with upstream" main upstream
```

---

## 🔥 Workflow Examples

**Scenario 1: Starting a Brand-New Project**
```bash
# Create and enter your new project directory
mkdir my-new-app
cd my-new-app

# Create some initial files
echo "# My New App" > README.md
touch app.py

# Initialize, commit, create GitHub repo, and push all at once!
gitpush "Initial commit" --new-repo my-new-app
```

**Scenario 2: Daily Updates on an Existing Project**
```bash
# Make your code changes...
# git add . (optional, gitpush adds all untracked files)

# Commit and push in one go
gitpush "Refactored user authentication logic"

# After rebasing, safely force push your changes
gitpush "Rebased onto main" --force
```

---

## 🧠 Advanced Options

| Option | Description |
|--------|-------------|
| `--new-repo NAME` | The name for the new GitHub repository. |
| `--private` | Creates a private repository. Public is the default. |
| `--description "TEXT"` | Sets the repository description on GitHub. |
| `--force` | Force pushes using `--force-with-lease` for safety. |
| `--tags` | Pushes all local tags along with your commits. |
| `--init` | Initializes a Git repository and creates a `.gitignore` but does not push. |

---

## 🛑 Troubleshooting

**Error:** GitHub CLI (gh) is not installed  
```
❌ GitHub CLI (gh) is not installed or not in your PATH.
➡️ Please install it from https://cli.github.com/
```

**Error:** Authentication failed  
```
❌ Authentication failed. Unable to connect to GitHub.
➡️ Run `gh auth login` and follow the prompts to re-authenticate.
```

**Error:** Repository already exists on GitHub  
```
❌ Repository 'user/my-repo' already exists.
➡️ Choose a different name for your new repository or delete the existing one on GitHub.
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/inevitablegs/gitpush/blob/main/LICENSE) file for details.

For more details, issues, or contributions, visit the **[GitHub Repository](https://github.com/inevitablegs/gitpush)**.

---

<div align="center">✨ <strong>Happy Coding!</strong> ✨</div>
