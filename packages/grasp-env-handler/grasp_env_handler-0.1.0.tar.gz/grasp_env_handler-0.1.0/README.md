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

With pip:
```bash
pip install git+https://github.com/username/grasp-env-handler.git
```

With uv:
```bash
uv pip install git+https://github.com/username/grasp-env-handler.git
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