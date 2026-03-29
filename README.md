# pybrdoc

**The ultimate, zero-dependency Python utility for validating, parsing, and generating Brazilian document numbers.**

[![CI/CD](https://github.com/seunome/pybrdoc/actions/workflows/ci.yml/badge.svg)](https://github.com/seunome/pybrdoc/actions)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)]()
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Semantic Release](https://img.shields.io/badge/semantic--release-active-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)

## Context & Objective

`pybrdoc` was created out of a need for an ultra-fast, robust, strictly typed, and independently tested suite for handling Brazilian-specific structural logic (e.g., CPFs, CNPJs, Processos do CNJ, Renavam).

The goal is to provide **100% mathematical test coverage**, uncompromising performance, and zero bloat for data-engineers, backend developers, and automated systems worldwide dealing with Brazilian data.

---

## Roadmap & Development Progress

We are currently in active development. Our module roadmap outlines the components scheduled for completion.

### ✅ Validators (Completed)

- [x] **CPF:** Modulo 11 check, length & digit repetition validations.
- [x] **CNPJ:** Modulo 11 check, length & sequence validation.

### ⏳ Pending Validators

- [ ] **Processo CNJ:** Validating Brazilian legal process numbering logic.
- [ ] **Renavam:** Vehicle registration numeric format check.
- [ ] **IE (Inscrição Estadual):** State registration keys (per-state math algorithm).
- [ ] **Título de Eleitor:** Voter registration verification.

### 🏗️ Generators & Parsers (Upcoming)

- [ ] **Mock Generators:** Realistic mock document generation for testing databases.
- [ ] **Parsers/Formatters:** Formatting massive data strings into correct punctuation structures (e.g. `12345678909` -> `123.456.789-09`).

---

## Infrastructure

The project maintains top-tier open-source quality:

- **Test-Driven:** Everything begins in `tests/`, asserting false before being architected.
- **CI/CD:** Multi-version parallel testing (Python 3.10 to 3.14).
- **Auto-Releases:** Semantic Release pushes Python versions out on every merge to `main`.
- **Pre-commit:** Ruff and MyPy keep the local state immaculately typed and formatted.

---

## Usage Example (Current State)

```python
from pybrdoc.validators.cnpj import is_valid_cnpj
from pybrdoc.validators.cpf import is_valid_cpf

# Rejects bad CNPJs instantly
assert is_valid_cnpj("11A222333000181") == False

# Validates proper formats
assert is_valid_cnpj("11.222.333/0001-81") == True

# Calculates internal checksums behind the scenes
assert is_valid_cpf("123.456.789-09") == False
```

