# Python Code Formatting & Linting Guide

This project uses industry-standard Python formatting and linting tools configured for **automatic formatting on save** in VS Code. No manual intervention needed—just save your files!

## ⚡ Quick Summary

| When               | What Happens          | Tools                                                 |
| ------------------ | --------------------- | ----------------------------------------------------- |
| **File Saved**     | Automatic formatting  | Black + isort                                         |
| **During Editing** | Live linting feedback | Flake8                                                |
| **Manual Check**   | Run all checks        | `uv run isort . && uv run black . && uv run flake8 .` |

## Tools Configured

| Tool       | Purpose                          | Config           |
| ---------- | -------------------------------- | ---------------- |
| **Black**  | Code formatter (Python standard) | `pyproject.toml` |
| **isort**  | Import sorter                    | `pyproject.toml` |
| **Flake8** | Linter                           | `.flake8`        |
| **Pylint** | Advanced linter                  | `pyproject.toml` |

## Setup Instructions

### 1. Install Development Dependencies

```bash
# Using uv (recommended)
uv sync --extra dev
```

### 2. Install VS Code Extensions

Required extensions for formatting on save:

```bash
ms-python.python          # Python extension
ms-python.black-formatter # Black formatter integration
ms-python.isort          # isort import sorting
```

Or install via command line:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
```

### 3. Verify Configuration

Configuration files are already set up:

- `.vscode/settings.json` - VS Code settings for formatting on save
- `pyproject.toml` - Black, isort, and pylint configurations
- `.flake8` - Flake8 linter configuration

### 4. Using uv Command Runner

This project uses `uv` for dependency management and running tools. All formatting and linting commands can be run with `uv run`:

```bash
# Format with Black
uv run black .

# Sort imports with isort
uv run isort .

# Lint with flake8
uv run flake8 .

# Lint with pylint
uv run pylint --recursive=y .
```

## Features

✅ **Format on Save** - Black automatically formats files on save
✅ **Import Sorting on Save** - isort automatically organizes imports on save
✅ **Live Linting** - Flake8 provides real-time linting feedback
✅ **Line Length** - 100 character line limit (Black standard)
✅ **Python 3.10+** - Target version configured
✅ **Black + isort Compatible** - Tools configured to work seamlessly together
✅ **Virtual Environment Safe** - Excludes `.venv` and `__pycache__`
✅ **uv Support** - All tools work with uv command runner

## Manual Usage

### Format a File

```bash
# Format with Black (using uv)
uv run black 1_simple_llm_agent_tool_func/main.py
uv run black 2_llm_agent_context_pydantic_tool/main.py

# Sort imports with isort (using uv)
uv run isort 1_simple_llm_agent_tool_func/main.py
uv run isort 2_llm_agent_context_pydantic_tool/main.py
```

### Format Entire Project

```bash
# Format all Python files with Black
uv run black .

# Sort all imports with isort
uv run isort .

# Format + sort imports in one command
uv run isort . && uv run black .
```

### Lint Code

```bash
# Check with flake8 (using uv)
uv run flake8 .
uv run flake8 1_simple_llm_agent_tool_func/main.py
uv run flake8 2_llm_agent_context_pydantic_tool/main.py

# Check with pylint (using uv)
uv run pylint 1_simple_llm_agent_tool_func/main.py
uv run pylint 2_llm_agent_context_pydantic_tool/main.py
```

## Configuration Details

### Black Settings (100 character lines)

- Line length: 100 characters
- Target Python: 3.10+
- Excludes: `.git`, `.venv`, `__pycache__`, `.pytest_cache`, `.vscode`

### isort Settings

- Profile: Black (compatible with Black formatter)
- Line length: 100 characters
- Skip: Git-ignored files

### Flake8 Settings

- Max line length: 100 characters
- Ignores: E203 (whitespace before ':'), W503 (line break before operator)
- Excludes: `.venv`, `__pycache__`, `.git`, `.pytest_cache`
- Per-file ignores: F401 (unused imports) in `__init__.py`

## VS Code On-Save Behavior

When you save a Python file (`.py`):

1. **isort** runs automatically - Organizes and sorts imports at the top
2. **Black** runs automatically - Formats code to project standards (100 char lines)
3. **Flake8** runs automatically - Reports linting issues (non-blocking, visual feedback only)

No manual intervention needed—files are formatted automatically as you work.

## Troubleshooting

### Verify Setup is Working

Test that everything is installed and configured:

```bash
# Check Black is available
uv run black --version

# Check isort is available
uv run isort --version

# Check Flake8 is available
uv run flake8 --version

# Run formatting on entire project
uv run isort . && uv run black .

# Check for linting issues
uv run flake8 .
```

### Extensions not found

Ensure Python extensions are installed:

```bash
code --list-extensions | grep ms-python
```

### Format on save not working

1. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
2. Check `.vscode/settings.json` is present
3. Verify extensions are enabled: Settings → Extensions → Python

### Black conflicts with other formatters

- Pylance format provider is disabled in `.vscode/settings.json`
- isort is configured with `profile=black` for compatibility

### Import sorting issues

isort is set to skip git-ignored files. Ensure imports are in tracked files.

## Pre-commit Hook (Optional)

To run formatting checks before commits, you can set up pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml in project root
# Then: pre-commit install
```

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.10
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.0
    hooks:
      - id: isort
        args: ["--profile=black"]
```

## Related Files

- `.vscode/settings.json` - VS Code workspace settings
- `pyproject.toml` - Project metadata and tool configurations
- `.flake8` - Flake8 linter configuration
- `.python-version` - Python version specification

## More Information

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pylint Documentation](https://pylint.pycqa.org/)
