# grasp-env-handler

A utility for managing .env files using Google Cloud Secret Manager for Grasp teams.

## Overview

This tool helps Grasp teams securely manage their .env files by storing them in Google Cloud Secret Manager.
It uses your GitHub repository name to organize secrets logically and provides simple commands to push and pull
environment variables across your team.

## Features

- Pull .env files from Secret Manager with `grasp env pull`
- Push .env files to Secret Manager with `grasp env push`
- Support for recursive operations with the `-r` flag
- Ignore specific .env files with `.envignore`

## Installation

Install the package directly from PyPI using pip or uv:

```bash
pip install grasp-env-handler
```

```bash
uv pip install grasp-env-handler
```

### Development Installation

For development:
```bash
# Clone the repository
git clone https://github.com/username/grasp-env-handler.git
cd grasp-env-handler

# With pip
pip install -e .

# With uv
uv pip install -e .
```

## Requirements

- Python 3.8+
- Google Cloud SDK installed and configured
- Git repository connected to GitHub

## GCP Setup

Before using this tool, make sure:

1. You have the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
2. You are authenticated with GCP: `gcloud auth login`
3. You have set a default project: `gcloud config set project YOUR-PROJECT-ID`
4. The Secret Manager API is enabled in your project: `gcloud services enable secretmanager.googleapis.com`
5. You have the necessary permissions to create and access secrets

## Usage

```bash
# Pull all .env files in current directory
grasp env pull

# Pull .env files recursively from all subdirectories
grasp env pull -r

# Push all .env files in current directory
grasp env push

# Push .env files recursively from all subdirectories
grasp env push -r
```

## .envignore

Create a `.envignore` file in your repository to exclude specific .env files:

```
# Example .envignore
path/to/secret.env
*.test.env
```

See `.envignore.example` for more examples. 

## Publishing to PyPI (for maintainers)

To publish a new version of this package to PyPI:

1.  **Increment the version number** in `pyproject.toml` (e.g., from `0.1.0` to `0.1.1`).

2.  **Build the package**:
    ```bash
    uv build
    ```
    This will create distribution files (a `.tar.gz` and a `.whl`) in the `dist/` directory.

3.  **Publish to PyPI**:
    You will need an API token from PyPI. Generate one from your PyPI account settings if you don't have one.
    Then, run the following command, replacing `YOUR_PYPI_API_TOKEN` with your actual token:
    ```bash
    uv publish dist/* -t YOUR_PYPI_API_TOKEN
    ```
    Alternatively, you can set the `UV_USERNAME=__token__` and `UV_PASSWORD=YOUR_PYPI_API_TOKEN` environment variables and then run `uv publish dist/*`. 