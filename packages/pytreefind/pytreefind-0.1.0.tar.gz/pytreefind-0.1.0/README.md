# pytreefind

A minimalist CLI tool that lists Python files in a clean tree structure.

## Quick Start

```bash
# Basic usage (current directory, 3 levels deep)
pytreefind

# Custom directory and depth
pytreefind -L 2 /path/to/project
```

## Features

<details>
<summary>What it does</summary>

- Shows only Python (`.py`) files
- Automatically excludes:
  - `__pycache__`
  - Virtual environments (`env`, `venv`)
  - Version control (`.git`)
  - Node modules (`node_modules`)
  - Test artifacts (`.pytest_cache`)
  - Package metadata (`*.egg-info`)
- Customizable depth level
</details>

<details>
<summary>Requirements</summary>

- Python 3.7+
- `tree` command installed on your system
  - Ubuntu/Debian: `apt install tree`
  - macOS: `brew install tree`
  - Windows: `choco install tree`
</details>

## Installation

```bash
pip install pytreefind
```

<details>
<summary>Development Installation</summary>

```bash
git clone git@github.com:preston-56/pytreefind.git
cd pytreefind
pip install -e .
```
</details>

<details>
<summary>For Maintainers</summary>

```bash
python3 -m build
twine upload dist/*
```
</details>

## License

[MIT License](LICENSE) - Preston Osoro