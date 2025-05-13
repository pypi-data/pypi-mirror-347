"""
Environment file operations and Secret Manager integration.
"""

import fnmatch
import os
from pathlib import Path

import typer
from google.cloud import secretmanager
from rich.console import Console

from grasp_env_handler.repo import check_github_repo, get_repo_root

console = Console()
error_console = Console(stderr=True)

_override_repo = None
_override_subdir = None


def set_overrides(repo: str = None, subdir: str = None) -> None:
    """Set global override values for repo and subdir."""
    global _override_repo, _override_subdir
    _override_repo = repo
    _override_subdir = subdir


def get_client() -> secretmanager.SecretManagerServiceClient:
    """Get a Secret Manager client."""
    try:
        return secretmanager.SecretManagerServiceClient()
    except Exception as e:
        error_console.print(
            f"Error connecting to Secret Manager: {str(e)}", style="red"
        )
        raise typer.Exit(1)


def get_project_id() -> str:
    """Get the default GCP project ID."""
    try:
        from google.auth import default

        _, project_id = default()

        if not project_id:
            error_console.print(
                "Error: No default GCP project found. Please run 'gcloud config set project <PROJECT_ID>'",
                style="red",
            )
            raise typer.Exit(1)

        return project_id
    except Exception as e:
        error_console.print(f"Error getting default GCP project: {str(e)}", style="red")
        raise typer.Exit(1)


def read_envignore() -> list[str]:
    """Read the .envignore file if it exists."""
    repo_root = get_repo_root(_override_subdir)
    envignore_path = repo_root / ".envignore"

    if not envignore_path.exists():
        return []

    with open(envignore_path, "r") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def should_ignore(file_path: Path, ignore_patterns: list[str]) -> bool:
    """Check if a file should be ignored based on .envignore patterns."""
    if not ignore_patterns:
        return False

    repo_root = get_repo_root(_override_subdir)
    relative_path = str(file_path.relative_to(repo_root))

    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True

    return False


def find_env_files(recursive: bool = False) -> list[Path]:
    """Find all .env files in the current directory (and subdirectories if recursive)."""
    current_dir = Path(os.getcwd())
    if _override_subdir:
        current_dir = Path(_override_subdir)
    ignore_patterns = read_envignore()

    env_files = []

    if recursive:
        for root, dirs, files in os.walk(current_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith(".env") and not file.endswith(".example"):
                    file_path = Path(root) / file
                    if not should_ignore(file_path, ignore_patterns):
                        env_files.append(file_path)
    else:
        for file in os.listdir(current_dir):
            if file.startswith(".env") and not file.endswith(".example"):
                file_path = current_dir / file
                if not should_ignore(file_path, ignore_patterns):
                    env_files.append(file_path)

    return env_files


def get_secret_id(env_file: Path) -> str:
    """Generate a secret ID for an .env file based on its path in the repo."""
    repo_name_str = check_github_repo(_override_repo, _override_subdir)
    repo_name = repo_name_str.replace("/", "__").replace(".", "--")

    repo_root = get_repo_root(_override_subdir)
    relative_path_str = str(env_file.relative_to(repo_root))
    path_part_for_secret = relative_path_str.replace("/", "__").replace(".", "--")

    secret_id_candidate = f"{repo_name}__{path_part_for_secret}"

    secret_id = "".join(
        c if c.isalnum() or c in "-_" else "-" for c in secret_id_candidate
    )

    return secret_id


def pull_env_files(recursive: bool = False) -> None:
    """Pull .env files from Secret Manager."""
    client = get_client()
    project_id = get_project_id()
    repo_root = get_repo_root(_override_subdir)

    env_files = []

    if not _override_repo:
        env_files = find_env_files(recursive)

    try:
        parent = f"projects/{project_id}"
        repo_name_str = check_github_repo(_override_repo, _override_subdir)
        repo_name_for_check = repo_name_str.replace("/", "__").replace(".", "--")

        found_secrets = False

        for secret in client.list_secrets(request={"parent": parent}):
            secret_id_from_gcp = secret.name.split("/")[-1]

            separator = "__"
            if secret_id_from_gcp.startswith(f"{repo_name_for_check}{separator}"):
                found_secrets = True
                path_part_from_secret = secret_id_from_gcp[
                    len(repo_name_for_check) + len(separator) :
                ]

                original_path_str = path_part_from_secret.replace("__", "/").replace(
                    "--", "."
                )
                file_path = repo_root / original_path_str

                filename = file_path.name
                if not filename.startswith(".env") and "." not in filename:
                    file_path = Path(f"{file_path}/.env")

                if should_ignore(file_path, read_envignore()):
                    continue

                should_add_file = False
                if recursive:
                    should_add_file = True
                else:
                    cwd = Path(os.getcwd())
                    if file_path.parent == cwd:
                        should_add_file = True

                if should_add_file and file_path not in env_files:
                    env_files.append(file_path)

        if _override_repo and not found_secrets:
            console.print(
                f"⚠️ No secrets found for repository: {_override_repo}", style="yellow"
            )

    except Exception as e:
        error_console.print(f"Error listing secrets: {str(e)}", style="red")

    if not env_files:
        console.print("No .env files found to pull.")
        return

    for env_file in env_files:
        try:
            secret_id = get_secret_id(env_file)
            secret_path = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

            try:
                response = client.access_secret_version(request={"name": secret_path})
                content = response.payload.data.decode("UTF-8")

                env_file.parent.mkdir(parents=True, exist_ok=True)

                with open(env_file, "w") as f:
                    f.write(content)

                console.print(f"✅ Pulled {env_file}")

            except Exception as e:
                if "NOT_FOUND" in str(e):
                    console.print(f"⚠️  Secret not found for {env_file}", style="yellow")
                else:
                    error_console.print(
                        f"❌ Error pulling {env_file}: {str(e)}", style="red"
                    )

        except Exception as e:
            error_console.print(
                f"❌ Error processing {env_file}: {str(e)}", style="red"
            )


def push_env_files(recursive: bool = False) -> None:
    """Push .env files to Secret Manager."""
    client = get_client()
    project_id = get_project_id()

    env_files = find_env_files(recursive)

    if not env_files:
        if _override_repo:
            console.print(
                f"⚠️ No local .env files found to push for repository: {_override_repo}",
                style="yellow",
            )
        else:
            console.print("No .env files found to push.")
        return

    for env_file in env_files:
        try:
            with open(env_file, "r") as f:
                content = f.read()

            secret_id = get_secret_id(env_file)

            parent = f"projects/{project_id}"
            secret_path = f"{parent}/secrets/{secret_id}"

            try:
                client.get_secret(request={"name": secret_path})
            except Exception:
                client.create_secret(
                    request={
                        "parent": parent,
                        "secret_id": secret_id,
                        "secret": {"replication": {"automatic": {}}},
                    }
                )

            response = client.add_secret_version(
                request={
                    "parent": secret_path,
                    "payload": {"data": content.encode()},
                }
            )

            repo_name = check_github_repo(_override_repo, _override_subdir)
            console.print(f"✅ Pushed {env_file} to {secret_id}")

        except Exception as e:
            error_console.print(f"❌ Error pushing {env_file}: {str(e)}", style="red")
