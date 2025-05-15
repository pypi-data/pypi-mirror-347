# Arc Memory Agent Guide

## Build/Test/Lint Commands
- **Install dependencies**: `pip install -e ".[dev]"`
- **Run all tests**: `pytest tests/`
- **Run a single test**: `pytest tests/path/to/test_file.py::test_function_name -v`
- **Run with coverage**: `pytest --cov=arc_memory tests/`
- **Type check**: `mypy arc_memory/`
- **Format code**: `black arc_memory/ tests/`
- **Sort imports**: `isort arc_memory/ tests/`
- **Lint code**: `ruff arc_memory/ tests/`

## Code Style Guidelines
- **Formatting**: Black with 88 character line length
- **Imports**: Use isort with Black profile
- **Types**: Strict typing required - disallow_untyped_defs=true
- **Naming**: Use snake_case for functions/variables, PascalCase for classes
- **Error handling**: Use explicit error types and meaningful error messages
- **Documentation**: Docstrings for all public functions/classes
- **Testing**: Write pytest tests for all new functionality

Pre-commit hooks are set up to enforce code style standards.