# Contributing to validabr

Welcome! We're excited that you want to contribute to validabr.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/validabr.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `uv sync`
5. Make your changes

## Code Quality Requirements

All contributions must pass:

```bash
# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run linting
uv run ruff check src/ tests/

# Run type checking
uv run mypy src/ tests/
```

## Requirements

- **Coverage**: 80%+ coverage required for all changes
- **Linting**: `ruff` must pass with no errors
- **Type checking**: `mypy --strict` must pass with no errors
- **Tests**: All existing tests must continue to pass

## Pull Request Workflow

1. Create a feature branch from `main`
2. Make your changes following the coding standards
3. Ensure all quality checks pass locally
4. Push to your fork and open a Pull Request
5. Address any review feedback

## Commit Messages

Use clear, descriptive commit messages that explain the "why" of your changes.

## Questions?

Feel free to open an issue for questions about contributing.
