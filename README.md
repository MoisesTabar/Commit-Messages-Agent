# Git Commit Messages Agent

A command-line tool that helps generate meaningful Git commit messages by analyzing staged changes and providing AI-powered suggestions.

## Features

- Interactive staging of changes using `git add --patch`
- Automatic detection of staged changes
- AI-powered commit message generation
- Support for both interactive and non-interactive modes
- Clean and user-friendly command-line interface

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MoisesTabar/Commit-Messages-Agent.git
   ```

2. Install project dependencies using uv:
   ```bash
   uv pip install -e .
   ```

3. Set up your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

## Usage

### Basic Usage

```bash
uv run python3 main.py
```

The tool will automatically detect staged changes and prompt you to stage any unstaged changes if needed.

### Options

- `--help`: Show help message and exit

## Development

### Package Management

This project uses `uv` for fast and reliable package management. Install it with:

```bash
curl -sSf https://astral.sh/uv/install.sh | sh
```

### Running Tests

```bash
uv run pytest
```

### Code Style and Linting

This project uses `pre-commit` to ensure code quality. It runs several hooks including:
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting
- `mypy` for type checking

To set up pre-commit hooks:

```bash
uv run pre-commit install
```

The hooks will run automatically on each commit. You can also run them manually:

```bash
uv run pre-commit
```

## Pre-commit Configuration

The project includes a `.pre-commit-config.yaml` file that defines the following hooks:
- `trailing-whitespace`: Removes trailing whitespace
- `end-of-file-fixer`: Ensures files end with a newline
- `check-yaml`: Validates YAML files
- `black`: Python code formatter
- `isort`: Sorts Python imports
- `flake8`: Python linter
- `mypy`: Static type checker

## Project Structure

```
.
├── main.py              # Main application entry point
├── prompts.py           # Contains AI prompt templates and message formatting
├── tools.py             # Defines tools and utilities for AI interaction
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── cli.py           # Command-line interface utilities
│   └── git.py           # Git-related utilities
├── tests/               # Test files
│   ├── __init__.py
│   ├── test_utils_cli.py
│   └── test_utils_git.py
```
