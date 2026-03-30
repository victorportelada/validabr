# pybrdoc Handoff Documentation

This document summarizes recent progress and outlines what remains to be built.

## Status: Feature-Complete on `develop` (2026-03-29)

- ✅ **100% test coverage** — 371 tests, 652 statements, zero misses
- ✅ **Ruff clean** — no linting violations
- ✅ **Mypy clean** — no type errors
- ✅ **Pushed to `origin/develop`**

---

## What We've Built

### Dev Environment
- Streamlit dashboard (`scripts/dashboard.py`) — live CI/CD + coverage display
- `python-dotenv` for zero-config `.env` secrets (GITHUB_TOKEN)
- `watchdog` for Streamlit hot-reload
- CI fix: lowered `requires-python` from `>=3.14` → `>=3.10`

### Validators (`src/pybrdoc/validators/`)
| Module | Coverage |
|---|---|
| `cpf.py` | 100% |
| `cnpj.py` | 100% |
| `cnj.py` | 100% |
| `ie.py` (27 states) | 100% |
| `renavam.py` | 100% |
| `titulo_eleitor.py` | 100% |

### Generators (`src/pybrdoc/generators/`)
Same modules, same 100% coverage.

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `develop` | Daily work, active development |
| `main` | Tagged releases only (PyPI-ready) |

**Don't merge to `main` until:**
1. `src/pybrdoc/parsers/` is implemented (`format_cpf()`, `mask_cnpj()`, etc.)
2. `src/pybrdoc/__init__.py` exports real public API (not just `hello()`)
3. `pyproject.toml` version bumped to `0.1.0`
4. `uv build` + `uv publish --dry-run` validated

---

## Next Steps
1. Implement `src/pybrdoc/parsers/` — formatting and masking per document type
2. Replace `hello()` stub in `__init__.py` with real public API
3. Run `uv build` to validate packaging
4. Merge `develop` → `main` + tag `v0.1.0` → PyPI release

---

## Running Locally

```bash
# Run tests with coverage
uv run pytest

# Start dev dashboard
uv run streamlit run scripts/dashboard.py

# Lint + type check
uv run ruff check src/ tests/
uv run mypy src/ tests/
```

Environment: requires `GITHUB_TOKEN` in `.env` for dashboard CI data.
