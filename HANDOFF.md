# pybrdoc Handoff Documentation

This document summarizes recent progress and outlines exactly what remains to be built in this codebase so you can jump right in.

## What We Have Done (Completed)
- **Dashboard & CI Integration**: Built a local Streamlit dashboard (`scripts/dashboard.py`) to monitor `pytests` output and query live GitHub Actions CI API (`victorportelada/pybrdoc`).
- **Dev Environment Quality of Life**: Added `python-dotenv` for zero-configuration testing via `.env` file instead of passing terminal args, and `watchdog` to streamline Streamlit hot-reloading.
- **CI Dependency Fix**: Fixed GitHub Actions failing `uv` builds by lowering the `requires-python` check in `pyproject.toml` from `>=3.14` down to `>=3.10`.
- **Validators & Parsers Core**:
  - Implemented the `CPF` and `CNPJ` robust validation logic.
  - Implemented generic text sanitization (stripping non-digits) in `utils/cleaner.py`.
  - Implemented generation logic (`generators/`) for CNPJ and CPF masks.
  - Fixed edge-case bugs in the validation regex.

## Work Division (2 parallel Claude instances)

### Instance A — `pybrdoc` (this instance): IE (Inscrição Estadual)
- `src/pybrdoc/validators/ie.py` — all 27 states
- `src/pybrdoc/generators/ie.py`
- `tests/validators/test_ie.py`
- `tests/generators/test_ie.py`

### Instance B — other instance: Processo CNJ + Título de Eleitor
- `src/pybrdoc/validators/processo_cnj.py`
- `src/pybrdoc/generators/processo_cnj.py`
- `src/pybrdoc/validators/titulo_eleitor.py`
- `src/pybrdoc/generators/titulo_eleitor.py`
- respective test files

## What We Need To Do (Next Steps)
1. ~~**Renavam**~~: Done (validator + generator + tests).
2. **IE (Inscrição Estadual)**: [IN PROGRESS — Instance A] All 27 states.
3. **Processo CNJ**: [Instance B] 20-digit judicial process number.
4. **Título de Eleitor**: [Instance B] 12-digit voter registry (mod-11 check on state IDs).
5. **Expand Test Coverage**: 80%+ coverage on all generators and validators.

## Important Project Notes
- **Testing**: Run `uv run pytest` to execute tests locally (the dashboard also parses this out).
- **Environment Run**: Start the dashboard via `uv run streamlit run scripts/dashboard.py`
- All remaining logic logic should be added into the `src/pybrdoc/validators/`, `src/pybrdoc/generators/`, and `src/pybrdoc/parsers/` modules.
