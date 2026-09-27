# Git and uv quick start

This quick start is written for Daan van Weeren and his astronomy matties. I hope it is clear. Let me know if you have any questions.

This repository is a practical introduction to Git and [uv](https://docs.astral.sh/uv/): Git tracks our code, while uv creates a fast, reproducible Python workflow.

## Git and GitHub quick start

Git is a tool for keeping a reliable history of your code. Instead of having only the latest copy of a file, you can save meaningful snapshots, see what changed, undo mistakes, and return to an earlier working version.

Git is also useful beyond version control. Your Git repository normally lives on your computer, but you can push it to a remote service such as GitHub. That gives you an off-computer backup if your laptop is lost or breaks, and makes collaboration possible. GitHub is not an automatic backup, though: your recent commits are protected only after you push them.

### Install Git on Ubuntu/WSL

Update the package list and install Git from the Ubuntu repositories:

```bash
sudo apt update
sudo apt install git
```

Check the installation:

```bash
git --version
```

Set your identity once. Use the same name and email associated with your GitHub account:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Create or clone a repository

To start a new local project:

```bash
mkdir my-project
cd my-project
git init
```

To download an existing GitHub repository:

```bash
git clone https://github.com/your-user/your-repository.git
cd your-repository
```

### Typical GitHub workflow

The usual cycle is: get the latest changes, edit files, inspect the changes, commit them, and push the commit to GitHub.

```bash
# Start from the latest version on GitHub
git pull

# Edit files, then inspect what changed
git status
git diff

# Select changes and save a snapshot locally
git add README.md
git commit -m "Explain the project workflow"

# Upload your local commits to GitHub
git push
```

`git add` selects what belongs in the next commit. `git commit` records that snapshot locally. `git push` publishes it on GitHub. You can stage all changed files with `git add .`, but review `git status` first.

### Undo changes safely

Git gives you several ways to recover when something goes wrong. Check `git status` before choosing an action:

```bash
# Discard uncommitted changes in one file
# Warning: the edits in this file cannot be recovered easily
git restore README.md

# Remove a file from the staging area, but keep its edits
git restore --staged README.md
```

If a commit has already been made, use `git revert`. This creates a new commit that reverses the earlier one, which is safe for commits already shared on GitHub:

```bash
# Reverse the most recent commit
git revert HEAD
```

For an earlier commit, find its identifier with `git log --oneline`, then run:

```bash
git revert <commit-id>
git push
```

Avoid rewriting shared history with commands such as `git reset --hard` unless you fully understand the consequences. A revert keeps the history visible and works safely for collaborative repositories.

For a new local repository, create an empty repository on GitHub, connect it as a remote, and push the first commit:

```bash
git remote add origin https://github.com/your-user/your-repository.git
git branch -M main
git add .
git commit -m "Initial commit"
git push -u origin main
```

You need permission to push to a GitHub repository. For repositories you do not own, create a fork or work on a branch and open a pull request.

## uv quick start

### Why uv?

Python projects need more than an interpreter: they need isolated environments, installed packages, and a way to reproduce the same setup on another computer. The traditional approach combines `venv` for isolation with `pip` for installation, plus extra tools or manual steps for locking dependencies and managing Python versions.

uv is a modern Python package and project manager written in Rust. Its biggest practical advantage is speed: the uv project reports installations up to **10–100 times faster than pip**, depending on the workload and whether packages are cached. It also uses a global cache so the same packages do not need to be downloaded repeatedly. See the [official uv overview](https://docs.astral.sh/uv/) for benchmarks and details.

More importantly for this tutorial, uv combines the whole project workflow in one tool. It creates virtual environments, resolves and installs packages, maintains a lockfile, can install Python versions, and runs project commands. The result is a short, consistent workflow: declare requirements in `pyproject.toml`, record exact versions in `uv.lock`, and run commands with `uv run`.

### Why prefer uv?

- Compared with `pip` and `venv` alone, uv is much faster and provides dependency resolution, locking, and environment management in one workflow.
- Compared with Pipenv or Poetry, uv provides the same general project-and-lockfile experience with a particularly fast resolver and a lightweight, unified CLI.
- Compared with Conda, uv is the better default for ordinary Python applications and libraries: it is focused and much faster for resolving and installing Python packages. Conda is a larger, heavier environment manager and can be noticeably—or sometimes dramatically—slower, especially while solving complex environments. Its broader support for non-Python binaries can still be useful in specialized scientific projects, but it is more tooling than most Python applications need.

For this tutorial, we recommend uv as the default Python tool. Other tools remain valid in projects that already depend on them, but a new Python project can start with fewer moving parts using uv. Commit both `pyproject.toml` and `uv.lock` so teammates and CI can recreate the same environment.

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

You can choose the version by adding a version requirement. Use quotes so the shell does not interpret characters such as `>` or `<`:

```bash
# Install exactly version 2.31.0
uv add "requests==2.31.0"

# Allow compatible releases from 2.31 up to, but not including, 3.0
uv add "requests>=2.31,<3"
```

The selected version is written to `pyproject.toml`, resolved in `uv.lock`, and installed into `.venv`. If you later want to change the requirement, run `uv add` again with the new version constraint.

You can also declare or edit the requirement directly in `pyproject.toml`:

```toml
[project]
dependencies = [
    "requests>=2.31,<3",
]
```

After editing the file, resolve the dependency and update the environment:

```bash
uv lock    # Resolve dependencies and update uv.lock
uv sync    # Install the locked dependencies into .venv
```

This is similar to `poetry update`, but the uv commands make the two actions explicit. `uv sync` normally updates the lockfile when needed as well, so the short version is often just:

```bash
uv sync
```

To update a package to the newest version allowed by the requirement in `pyproject.toml`, use:

```bash
uv lock --upgrade-package requests
uv sync
```

To upgrade all dependencies allowed by their requirements, use `uv lock --upgrade` followed by `uv sync`. Review and commit the resulting `uv.lock` change.

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

### Activate the environment explicitly (optional)

You do not need to activate the environment when using `uv run`. For an interactive terminal session, however, you can activate the `.venv` created by `uv sync`:

```bash
source .venv/bin/activate
python main.py
pytest
deactivate
```

After activation, `python` and tools such as `pytest` refer to the project environment until you run `deactivate` or close the terminal. When possible, prefer `uv run ...` in documentation and scripts because it makes the environment being used explicit.

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

## Practice exercise: run a small pandas project

This repository includes a tiny sales analysis so you can practice the complete workflow. The Python script uses `pandas`, which is declared in `pyproject.toml`; the exact dependency versions are recorded in `uv.lock`.

After cloning the repository, run:

```bash
uv sync
uv run python analyze_sales.py
```

The first command reads `pyproject.toml` and `uv.lock`, creates `.venv`, and installs pandas and its dependencies. The second command runs the script inside that environment and prints each product’s revenue and the total revenue. The script would fail with a plain `python analyze_sales.py` on a clean machine because pandas would not be installed in that machine’s default Python environment.

Try changing `sales.csv`, run the script again, and inspect the files Git sees as changed:

```bash
git status
git diff
```

You can also see which packages uv installed:

```bash
uv tree
```

The exercise demonstrates the main idea: the source code, `pyproject.toml`, and `uv.lock` are shared through Git; `.venv` is created locally by `uv sync` and is not committed.

## Appendix: Visual Studio Code with WSL

Visual Studio Code is optional. For a WSL-based workflow, install the VS Code application on **Windows**, then connect it to Ubuntu/WSL with the Microsoft **WSL** extension. You normally do not need to install a second copy of VS Code inside WSL.

### Setup

1. Install [Visual Studio Code](https://code.visualstudio.com/) on Windows.
2. Open VS Code and install the **WSL** extension from Microsoft.
3. In an Ubuntu/WSL terminal, go to the project directory and run:

   ```bash
   code .
   ```

VS Code opens the project using the WSL environment. The editor runs on Windows, while terminals, Python, Git, uv, and project files are accessed through Linux/WSL.

### Select the project Python interpreter

Install the Microsoft **Python** extension if VS Code suggests it. Then open the Command Palette with `Ctrl+Shift+P`, choose **Python: Select Interpreter**, and select the interpreter inside the project:

```text
.venv/bin/python
```

If it is not listed, run `uv sync` in the VS Code terminal first and reload the window. Commands run from the integrated terminal should then work as they do in the WSL terminal:

```bash
uv run python analyze_sales.py
uv run pytest
```

Keep the project files inside the WSL filesystem, for example under `~/projects`, rather than under `/mnt/c`, when possible. This generally gives better performance and avoids file-permission surprises.

## Further reading

- Git: [Pro Git book](https://git-scm.com/book/en/v2)
- uv: [Official uv documentation](https://docs.astral.sh/uv/)
