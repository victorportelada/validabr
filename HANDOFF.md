# pybrdoc Handoff Documentation

This document summarizes recent progress and outlines what remains to be built.

## Status: v0.2.0 Released (2026-03-30)

- ✅ **99% test coverage** — Over 500 tests covering all validators, generators, and formatters
- ✅ **Ruff clean** — no linting violations
- ✅ **Mypy clean** — no type errors
- ✅ **Released v0.2.0 on PyPI**
- ✅ **Merged to `master`**

---

## What We've Built

### Dev Environment
- Streamlit dashboard (`scripts/dashboard.py`) — live CI/CD + coverage display
- `python-dotenv` for zero-config `.env` secrets (GITHUB_TOKEN)
- `watchdog` for Streamlit hot-reload
- GitHub Actions configured for automatic PyPI publication using Semantic Release

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
All generator modules are complete with 100% coverage.

### Parsers (`src/pybrdoc/parsers/`)
All formatters are complete:
- `format_cpf()`
- `format_cnpj()`
- `format_cnj()`
- `format_ie()` (all 27 states, including dual-length states like BA, PE, RN, RO)
- `format_renavam()`
- `format_titulo_eleitor()`

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `develop` | Daily work, active development |
| `master` | Tagged releases only (PyPI-ready) |

---

## Next Steps

1. Implement `parse_ie()` — structured parser returning a named dict (sequential, state, check digits)
2. Add a CLI wrapper — e.g. `pybrdoc validate cpf 529.982.247-25`

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
