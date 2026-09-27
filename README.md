# uv-git-quick-start
This is a quick start to install the package manager uv and git locally

# uv quick start

### Background
The Python ecosystem relies on several foundational package managers, each serving distinct deployment and workflow needs. **Pip** is the universal, standard installer bundled with Python for retrieving packages from the Python Package Index (PyPI), traditionally paired with **venv** for environment isolation. In contrast, **Conda** is a cross-platform, language-agnostic manager widely adopted in data science for its ability to seamlessly handle complex non-Python binaries and virtual environments. For unified application workflows, first-generation lockfile tools like **Pipenv** and **Poetry** bridge the gap by combining dependency resolution, environment isolation, and strict reproducibility into a single developer experience.

### Why uv?
Modern Python development often suffers from slow dependency resolution and fragmented tooling when juggling legacy managers like Conda and Pipenv. **uv** solves these pain points by acting as a single, ultra-fast tool written in Rust that replaces pip, pip-tools, virtualenv, and poetry/pipenv workflows entirely. While Conda is notoriously slow and resource-heavy when solving complex binary environments, and Pipenv frequently struggles with slow locking times and deterministic stability, **uv** delivers up to **10–100x faster installations** and seamless, zero-config environment management, drastically reducing developer friction and CI/CD pipeline costs.

### Installation on Ubuntu WSL

To install **uv**, run the official standalone installer script in your WSL terminal:

```bash
curl -LsSf https://astral.sh | sh
```

### Next Steps
1. **Restart your terminal** (or run `source ~/.bashrc`) to apply the changes.
2. Verify that it works by checking the version:
3. 
   ```bash
   uv --version
   ```

# git quick start

### Create a repository

### Clone a repository
You can clone (download) public repositories but you can only push (check in) your code in a repos for which you are authorised.

``bash
git clone https://github.com/longtongster/uv-git-quick-start.git
```

