# brdocs — Agent Instructions

## Project

Python library for validating, generating, formatting, and parsing Brazilian documents (CPF, CNPJ, CNJ, IE, RENAVAM, Título de Eleitor, and more).

**Stack:** Python 3.10+, uv, pytest, ruff, mypy --strict

---

## STEP 0 — Always do this first

Before writing any code, read `ROADMAP.md` in full. It is the canonical spec.
Pay special attention to the **Principles & Guardrails** section at the top — those are hard constraints, not suggestions.

---

## Non-Negotiable Constraints

Violating any of these is a blocker. Do not ship without satisfying all of them.

1. **Zero core dependencies** — `src/brdocs/` (excluding `integrations/`) must only use the Python Standard Library. No third-party imports in core.

2. **try/except ImportError on all integrations** — Every file under `src/brdocs/integrations/` must wrap its framework imports in `try/except ImportError` and re-raise with a clear message pointing to the install extra (e.g. `pip install brdocs[django]`). This is required so that `import brdocs` never fails in environments where Django/Pydantic are not installed.

3. **100% branch coverage** — `uv run pytest --cov=src --cov-report=term-missing` must show 100% for every file you touch. No exceptions.

4. **mypy --strict must pass** — Fix type errors precisely. Do NOT add `# type: ignore` on entire files or `ignore_errors = true` for test modules in `pyproject.toml`. Only add targeted `# type: ignore[specific-code]` on individual lines where the framework's own stubs are incomplete.

5. **ruff must pass** — Fix linting errors at the source. Do NOT add broad `per-file-ignores` to suppress entire rule categories across all test files.

6. **Symmetric API** — Every new document type must implement all four: `is_valid_*`, `generate_*`, `format_*`, `parse_*`.

---

## Before Implementing Complex Integrations

For anything touching `integrations/` (Django, Pydantic, etc.), state your plan explicitly before writing code:
- Which base classes you will subclass
- Which methods you will override and why
- How you will handle the `try/except ImportError` pattern
- What `max_length` values the model fields need (formatted string length, not raw digit count)

This prevents the expensive iteration loop of writing → breaking → rewriting.

---

## Dev Commands

```bash
uv sync                                          # install deps
uv run pytest                                    # run tests
uv run pytest --cov=src --cov-report=term-missing  # with coverage
uv run ruff check src/ tests/                    # lint
uv run ruff format src/ tests/                   # format
uv run mypy src/ tests/                          # type check
```

All four must pass before any task is considered done.

---

## Directory Layout

```
src/brdocs/
  validators/      is_valid_*
  generators/      generate_*
  parsers/         format_*, parse_*, *Data NamedTuples
  integrations/    pydantic.py, django.py  (optional deps, try/except ImportError)
  bulk.py          validate_list, generate_list, validate_docs
  cli.py           argparse CLI
tests/
  parsers/
  integrations/
  test_bulk.py
  test_cli.py
```

## Naming Conventions

- Validators: `is_valid_cpf(cpf: str) -> bool`
- Generators: `generate_cpf() -> str` (returns raw digits)
- Formatters: `format_cpf(cpf: str) -> str` (idempotent — handles raw or already-formatted)
- Parsers: `parse_cpf(cpf: str) -> CPFData` (NamedTuple, raises ValueError on bad input)
