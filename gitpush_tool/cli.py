
import os
import argparse
import sys
import subprocess
from datetime import datetime
import os
import subprocess
import platform
import urllib.request
import tempfile
import shutil

def check_gh_installed():
    if shutil.which("gh"):
        return True

    print("📦 GitHub CLI not found. Attempting installation...")

    system = platform.system()
    try:
        if system == "Windows":
            return install_gh_cli_windows()
        elif system == "Darwin":
            subprocess.run(["brew", "install", "gh"], check=True)
            return shutil.which("gh") is not None
        elif system == "Linux":
            subprocess.run(["sudo", "apt", "install", "-y", "gh"], check=True)
            return shutil.which("gh") is not None
        else:
            print("❌ Unsupported OS.")
            return False
    except Exception as e:
        print(f"❌ Failed to install GitHub CLI: {e}")
        return False



def gh_authenticated():
    """Check if user is authenticated with GitHub CLI"""
    try:
        result = subprocess.run(["gh", "auth", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except:
        return False

def authenticate_with_gh():
    """Authenticate user with GitHub CLI"""
    print("\n🔑 GitHub authentication required")
    print("We'll use the GitHub CLI (gh) for authentication")
    print("This will open your browser for secure login")
    
    try:
        subprocess.run(["gh", "auth", "login", "--web", "-h", "github.com"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Authentication failed")
        return False
    except FileNotFoundError:
        print("❌ GitHub CLI not found")
        return False

def initialize_git_repository():
    """Initialize git repository if not already initialized"""
    if not os.path.exists(".git"):
        print("🛠 Initializing git repository")
        try:
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            
            # Create basic .gitignore if doesn't exist
            if not os.path.exists(".gitignore"):
                with open(".gitignore", "w") as f:
                    f.write("""# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# System
.DS_Store
Thumbs.db

# Project specific
*.log
*.tmp
*.bak
""")
                print("📁 Created .gitignore file")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize Git repository: {e}")
            return False
    return False

def create_initial_commit(commit_message="Initial commit"):
    """Create initial commit if no commits exist"""
    try:
        # Check if there are any commits
        result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        commit_count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
        
        if commit_count == 0:
            print("📦 Creating initial commit")
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create initial commit: {e}")
        return False

def create_with_gh_cli(repo_name, private=False, description="", commit_message="Initial commit"):
    """Create and push to new repository using GitHub CLI"""
    try:
        # First ensure we have a Git repository
        if not os.path.exists(".git"):
            if not initialize_git_repository():
                return False
        
        # Create initial commit if needed
        if not create_initial_commit(commit_message):
            print("ℹ️ Using existing commits")

        private_flag = "--private" if private else "--public"
        cmd = [
            "gh", "repo", "create", repo_name,
            private_flag,
            "--source=.",
            "--remote=origin",
            "--push"
        ]
        
        if description:
            cmd.extend(["--description", description])
        
        print("🚀 Creating repository and pushing code...")
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            # Get the repo URL
            url_result = subprocess.run(
                ["gh", "repo", "view", "--json", "url", "--jq", ".url"],
                stdout=subprocess.PIPE,
                text=True,
                check=True
            )
            repo_url = url_result.stdout.strip()
            print(f"✅ Successfully created repository: {repo_url}")
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create repository: {e.stderr if e.stderr else 'Unknown error'}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def standard_git_push(commit_message, branch, remote, force=False, tags=False):
    """Handle standard git push operations"""
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit if message provided
        if commit_message:
            print(f"📦 Committing: '{commit_message}'")
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
        else:
            print("ℹ️ No commit message provided - skipping commit")
        
        # Build push command
        push_cmd = ["git", "push"]
        if force:
            push_cmd.append("--force-with-lease")
        if tags:
            push_cmd.append("--tags")
        if remote and branch:
            push_cmd.extend([remote, branch])
        
        print(f"🚀 Executing: {' '.join(push_cmd)}")
        subprocess.run(push_cmd, check=True)
        print("✅ Successfully pushed changes")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Push failed: {e}")
        return False


import subprocess
import shutil
import os
import sys
import platform
import tempfile
import urllib.request

def is_gh_installed():
    return shutil.which("gh") is not None

def install_gh_windows():
    print("📦 GitHub CLI not found. Attempting installation on Windows...")
    
    # Try winget first
    if shutil.which("winget"):
        print("👉 Installing via winget...")
        try:
            subprocess.run(["winget", "install", "--id", "GitHub.cli", "--silent", "--accept-package-agreements", "--accept-source-agreements"], check=True)
            return shutil.which("gh") is not None
        except subprocess.CalledProcessError:
            print("⚠️ winget installation failed.")
    
    # Fallback to direct MSI download
    print("⚠️ winget not available or failed. Trying direct download...")
    gh_url = "https://github.com/cli/cli/releases/latest/download/gh_2.76.0_windows_amd64.msi"
    installer_path = os.path.join(tempfile.gettempdir(), "gh_installer.msi")
    try:
        print("⬇️ Downloading GitHub CLI installer...")
        urllib.request.urlretrieve(gh_url, installer_path)
        print("📥 Running installer...")
        subprocess.run(["msiexec", "/i", installer_path, "/quiet", "/qn", "/norestart"], check=True)
        return shutil.which("gh") is not None
    except Exception as e:
        print(f"❌ Direct installation failed: {e}")
        return False

def ensure_gh():
    if is_gh_installed():
        print("✅ GitHub CLI is already installed.")
        return True

    if platform.system() == "Windows":
        success = install_gh_windows()
    else:
        print("❌ Automatic installation not supported on this OS. Please install manually.")
        success = False

    if not success:
        print("❌ GitHub CLI (gh) is not installed")
        print("Please install it manually:")
        print("  Mac: brew install gh")
        print("  Windows: winget install --id GitHub.cli")
        print("  Linux: https://github.com/cli/cli#installation")
        return False

    return True

# ✅ Call this before using gh in your code
if ensure_gh():
    # You can proceed to use `gh`, like:
    subprocess.run(["gh", "auth", "login"])


def install_gh_cli_windows():
    """Install GitHub CLI on Windows using winget or direct download"""
    print("📦 GitHub CLI not found. Attempting installation on Windows...")

    # First, try using winget
    try:
        subprocess.run(["winget", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("👉 Installing via winget...")
        subprocess.run(["winget", "install", "--id", "GitHub.cli", "-e", "--silent"], check=True)
        print("✅ GitHub CLI installed successfully via winget.")
        return True
    except Exception as e:
        print("⚠️ winget not available or failed. Trying direct download...")

    # Fallback: Direct download from GitHub
    try:
        print("⬇️ Downloading GitHub CLI installer...")
        url = "https://github.com/cli/cli/releases/latest/download/gh_2.46.0_windows_amd64.msi"
        temp_dir = tempfile.mkdtemp()
        msi_path = os.path.join(temp_dir, "gh.msi")
        urllib.request.urlretrieve(url, msi_path)

        print("🛠 Installing GitHub CLI...")
        subprocess.run(["msiexec", "/i", msi_path, "/quiet", "/norestart"], check=True)

        shutil.rmtree(temp_dir)  # clean up
        print("✅ GitHub CLI installed successfully via MSI.")
        return True
    except Exception as e:
        print(f"❌ Direct installation failed: {e}")
        return False


def run():
    parser = argparse.ArgumentParser(
        description="🚀 Supercharged Git push tool with GitHub repo creation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  Standard push:         gitpush_tool "Commit message"
  Create new repo:       gitpush_tool "Initial commit" --new-repo project-name
  Private repository:    gitpush_tool --new-repo private-project --private
  Force push:            gitpush_tool "Fix critical bug" --force
"""
    )
    parser.add_argument("commit", nargs="?", help="Commit message")
    parser.add_argument("branch", nargs="?", default="main", help="Branch name (default: main)")
    parser.add_argument("remote", nargs="?", default="origin", help="Remote name (default: origin)")
    parser.add_argument("--force", action="store_true", help="Force push with --force-with-lease")
    parser.add_argument("--tags", action="store_true", help="Push tags")
    parser.add_argument("--init", action="store_true", help="Initialize git repo")
    parser.add_argument("--new-repo", metavar="NAME", help="Create new GitHub repository")
    parser.add_argument("--private", action="store_true", help="Make repository private")
    parser.add_argument("--description", help="Repository description")

    args = parser.parse_args()

    if args.new_repo:
        print(f"🆕 Creating repository: {args.new_repo}")
        
        if not check_gh_installed():
            print("❌ GitHub CLI (gh) is not installed")
            print("Please install it first:")
            print("  Mac (Homebrew): brew install gh")
            print("  Windows (Winget): winget install --id GitHub.cli")
            print("  Linux: See https://github.com/cli/cli#installation")
            sys.exit(1)
        
        if not gh_authenticated():
            if not authenticate_with_gh():
                sys.exit(1)
        
        commit_msg = args.commit if args.commit else "Initial commit"
        if not create_with_gh_cli(
            args.new_repo,
            private=args.private,
            description=args.description or "",
            commit_message=commit_msg
        ):
            sys.exit(1)
    elif args.init:
        if initialize_git_repository():
            create_initial_commit(args.commit or "Initial commit")
    else:
        # Standard git push operation
        if not standard_git_push(
            args.commit,
            args.branch,
            args.remote,
            args.force,
            args.tags
        ):
            sys.exit(1)
            
            
            


if __name__ == "__main__":
    run()