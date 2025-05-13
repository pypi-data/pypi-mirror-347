"""
GitHub repository detection and information.
"""

import os
import re
from pathlib import Path

import git
import typer
from rich.console import Console

console = Console()
error_console = Console(stderr=True)


def check_github_repo(override_repo: str = None, override_subdir: str = None) -> str:
    """
    Check if the current directory is within a GitHub repository.
    Returns the GitHub repository name if it is, otherwise exits.

    Args:
        override_repo: Optional GitHub repository name to override detection (format: owner/repo)
        override_subdir: Optional subdirectory path to override detection

    Returns:
        The GitHub repository name (format: owner/repo)
    """
    if override_repo:
        if "/" not in override_repo or len(override_repo.split("/")) != 2:
            error_console.print(
                "Error: Invalid repo format. Must be 'owner/repo'.", style="red"
            )
            raise typer.Exit(1)
        return override_repo

    try:
        repo = git.Repo(os.getcwd(), search_parent_directories=True)

        for remote in repo.remotes:
            if remote.name == "origin":
                url = remote.url
                github_pattern = re.compile(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$")
                match = github_pattern.search(url)

                if match:
                    repo_name = match.group(1)
                    return repo_name
                else:
                    error_console.print("Error: Not a GitHub repository.", style="red")
                    raise typer.Exit(1)

        error_console.print(
            "Error: No 'origin' remote found in the git repository.", style="red"
        )
        raise typer.Exit(1)

    except git.exc.InvalidGitRepositoryError:
        error_console.print("Error: Not in a git repository.", style="red")
        raise typer.Exit(1)
    except Exception as e:
        error_console.print(f"Error: {str(e)}", style="red")
        raise typer.Exit(1)


def get_repo_root(override_subdir: str = None) -> Path:
    """
    Get the root directory of the git repository.

    Args:
        override_subdir: Optional subdirectory path to override detection

    Returns:
        The repository root path or the specified subdirectory if override_subdir is provided
    """
    if override_subdir:
        path = Path(override_subdir)
        if not path.exists():
            error_console.print(
                f"Error: Subdirectory {override_subdir} not found.", style="red"
            )
            raise typer.Exit(1)
        return path.absolute()

    try:
        repo = git.Repo(os.getcwd(), search_parent_directories=True)
        return Path(repo.working_dir)
    except Exception:
        error_console.print("Error: Not in a git repository.", style="red")
        raise typer.Exit(1)
