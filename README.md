# Git and uv quick start

This repository is a practical introduction to Git and [uv](https://docs.astral.sh/uv/): Git tracks our code, while uv creates a fast, reproducible Python workflow.

## Why uv?

Python projects traditionally combine several tools: `venv` for isolation, `pip` for installation, and another tool for dependency locking or Python versions. uv brings the common workflow together in one fast command-line tool.

It manages virtual environments, dependencies, lockfiles, Python versions, and project commands. `pyproject.toml` declares what the project needs and `uv.lock` records exact versions. Commit both so teammates and CI can recreate the same environment.

## Short workflow

### 1. Install and verify uv

Follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/), then run:

```bash
uv --version
```

On Ubuntu/WSL, the standalone installer is:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal or run `source ~/.bashrc` if your shell cannot find `uv`.

### 2. Create or clone a project

`uv init` creates the project structure and writes the project metadata to `pyproject.toml`. It does not install dependencies or create the virtual environment yet:

```bash
uv init my-project
cd my-project
```

Now create the virtual environment and install the project with:

```bash
uv sync
```

`uv sync` creates the local `.venv` directory and the `uv.lock` lockfile. The `.venv` directory is for your machine and should not be committed; `uv.lock` records exact versions and should be committed.

For an existing project:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 3. Add and change dependencies

Add the packages the application needs:

```bash
uv add requests
```

Add tools used only while developing or testing:

```bash
uv add --dev pytest ruff
```

Remove a package when it is no longer needed:

```bash
uv remove requests
```

These commands update `pyproject.toml`, update `uv.lock`, and synchronise `.venv`. In other words, use `uv add` and `uv remove` to change the project; use `uv sync` to make a local environment match the project files.

### 4. Run commands

Use `uv run` to execute a command inside the project’s virtual environment. You do not need to activate `.venv` manually:

```bash
uv run python main.py
uv run pytest
uv run ruff check .
```

### 5. Recreate an environment after cloning

When another developer clones the repository, `pyproject.toml` describes the project and `uv.lock` describes the exact versions to install. They can reproduce the environment with:

```bash
git clone <repository-url>
cd <repository-directory>
uv sync
uv run pytest
```

Here `uv sync` creates `.venv` if necessary and installs the locked dependencies. `uv run pytest` then runs the tests in that environment. Do not edit `uv.lock` manually.

## Useful commands

| Goal | Command |
| --- | --- |
| Inspect dependencies | `uv tree` |
| Update the lockfile | `uv lock --upgrade` |
| Run a one-off tool | `uvx TOOL` |
| Show help | `uv help` |

Use `uvx ruff check .` for a one-off tool. If the project uses Ruff regularly, add it with `uv add --dev ruff` so its version is shared.

## What to commit

Commit `pyproject.toml`, `uv.lock`, source code, and tests. Do not commit the local environment; add this to `.gitignore`:

```gitignore
.venv/
```

## Git quick start

### Create a repository

```bash
git init
git add .
git commit -m "Initial commit"
```

### Clone a repository

You can clone public repositories, but you can only push code to repositories where you have permission:

```bash
git clone https://github.com/longtongster/uv-git-quick-start.git
cd uv-git-quick-start
```
