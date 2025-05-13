import os

PRE_COMMIT_HOOK = """#!/bin/sh
# Run Snyk test on all project files
echo "Running Snyk vulnerability scan..."
snyk test --all-project --fail-on=all
# Check if Snyk test was successful (exit code 0) or failed (exit code 1)
if [ $? -ne 0 ]; then
  echo "Snyk found vulnerabilities in your project. Commit aborted."
  exit 1
fi
# Run Talisman secret scan to detect any sensitive data
echo "Running Talisman secret scan..."
talisman --githook pre-commit
# Check if Talisman found any secrets (exit code 1 means secrets found)
if [ $? -ne 0 ]; then
  echo "Talisman found secrets in your code. Commit aborted."
  exit 1
fi
# If no vulnerabilities or secrets are found, allow the commit to proceed
exit 0
"""

def install_pre_commit_hook():
    # Locate the .git/hooks directory in the target repository
    current_dir = os.getcwd()
    git_hooks_dir = os.path.join(current_dir, ".git", "hooks")
    pre_commit_path = os.path.join(git_hooks_dir, "pre-commit")

    if not os.path.exists(git_hooks_dir):
        print("Error: .git/hooks directory not found. Are you in a Git repository?")
        return

    # Write the pre-commit hook script
    with open(pre_commit_path, "w") as hook_file:
        hook_file.write(PRE_COMMIT_HOOK)

    # Make the pre-commit hook executable
    os.chmod(pre_commit_path, 0o755)
    print("Pre-commit hook installed successfully in the target repository.")

# Automatically install the pre-commit hook when the package is imported
if __name__ == "__main__":
    install_pre_commit_hook()
