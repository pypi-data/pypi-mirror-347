from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class CustomInstallCommand(install):
    """Custom install command to run post-install logic."""
    def run(self):
        # Run the standard install process
        install.run(self)
        
        # Run the pre-commit hook installation logic
        try:
            # Check if the current directory is a Git repository
            if os.path.exists(".git/hooks"):
                # Run the install-precommit-hook script
                subprocess.check_call(["install-precommit-hook"])
                print("Pre-commit hook installed successfully.")
            else:
                print("Warning: .git/hooks directory not found. Are you in a Git repository?")
        except Exception as e:
            print(f"Error during post-install script execution: {e}")

setup(
    name="precommit_hook_installation",
    version="1.0.0",
    packages=find_packages(include=["sitecustomize"]),
    install_requires=[
        # No snyk or talisman dependencies
    ],
    cmdclass={
        "install": CustomInstallCommand,
    },
    entry_points={
        "console_scripts": [
            "install-precommit-hook=precommit_hook_installation.install_hook:install_pre_commit_hook"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
