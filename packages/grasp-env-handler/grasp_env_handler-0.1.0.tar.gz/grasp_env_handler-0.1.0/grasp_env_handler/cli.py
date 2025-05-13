"""
Command-line interface for grasp-env-handler.
"""

import typer
from rich.console import Console

from grasp_env_handler.env import pull_env_files, push_env_files, set_overrides
from grasp_env_handler.repo import check_github_repo

console = Console()

app = typer.Typer(help="Grasp utilities")
env_app = typer.Typer(
    help="Manage .env files using Google Cloud Secret Manager", no_args_is_help=True
)
app.add_typer(env_app, name="env")


@env_app.callback(invoke_without_command=True)
def env_callback(
    ctx: typer.Context,
    repo: str = typer.Option(
        None,
        "--repo",
        help="Override the GitHub repository to use (format: owner/repo)",
    ),
    subdir: str = typer.Option(
        None, "--subdir", help="Override the subdirectory path to use"
    ),
):
    """
    Manage .env files with Google Cloud Secret Manager.
    """
    set_overrides(repo=repo, subdir=subdir)
    if ctx.invoked_subcommand is not None:
        check_github_repo(override_repo=repo, override_subdir=subdir)


@env_app.command()
def pull(
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Pull .env files from all subdirectories"
    ),
):
    """
    Pull .env files from Secret Manager.
    """
    console.print(
        f"Pulling .env files {'recursively' if recursive else 'in current directory'}"
    )
    pull_env_files(recursive=recursive)
    console.print("Done! :heavy_check_mark:", style="green")


@env_app.command()
def push(
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Push .env files from all subdirectories"
    ),
):
    """
    Push .env files to Secret Manager.
    """
    console.print(
        f"Pushing .env files {'recursively' if recursive else 'in current directory'}"
    )
    push_env_files(recursive=recursive)
    console.print("Done! :heavy_check_mark:", style="green")


if __name__ == "__main__":
    app()
