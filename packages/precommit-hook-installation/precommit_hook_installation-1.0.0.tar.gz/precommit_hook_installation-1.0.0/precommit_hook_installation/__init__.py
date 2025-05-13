import os
from .install_hook import install_pre_commit_hook

# Automatically install the pre-commit hook when the package is imported
try:
    current_dir = os.getcwd()
    git_hooks_dir = os.path.join(current_dir, ".git", "hooks")

    if os.path.exists(git_hooks_dir):
        install_pre_commit_hook()
    else:
        print("Warning: .git/hooks directory not found. Are you in a Git repository?")
except Exception as e:
    print(f"Error during pre-commit hook installation: {e}")
