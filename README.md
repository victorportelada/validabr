# pybrdoc

Zero-dependency Python library for validating, generating, and formatting Brazilian document numbers — CPF, CNPJ, CNJ, IE (all 27 states), RENAVAM, and Título de Eleitor.

[![PyPI](https://img.shields.io/pypi/v/pybrdoc.svg)](https://pypi.org/project/pybrdoc/)
[![Python](https://img.shields.io/pypi/pyversions/pybrdoc.svg)](https://pypi.org/project/pybrdoc/)
[![CI](https://github.com/victorportelada/pybrdoc/actions/workflows/ci.yml/badge.svg)](https://github.com/victorportelada/pybrdoc/actions)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)]()
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## Installation

```bash
pip install pybrdoc
```

```bash
uv add pybrdoc
```

---

## Quick Start

```python
import pybrdoc

# Validate
pybrdoc.is_valid_cpf("529.982.247-25")        # True
pybrdoc.is_valid_cnpj("11.222.333/0001-81")   # True
pybrdoc.is_valid_ie("110.042.490.114", "SP")  # True

# Format (strips punctuation and re-applies canonical mask)
pybrdoc.format_cpf("52998224725")             # "529.982.247-25"
pybrdoc.format_cnpj("11222333000181")         # "11.222.333/0001-81"
pybrdoc.format_ie("110042490114", "SP")       # "110.042.490.114"

# Generate valid random documents
pybrdoc.generate_cpf()                        # e.g. "52998224725"
pybrdoc.generate_cpf(formatted=True)          # e.g. "529.982.247-25"
pybrdoc.generate_ie("MG")                     # e.g. "0621071700110"
```

---

## API Reference

### Validators

| Function | Document | Notes |
|----------|----------|-------|
| `is_valid_cpf(cpf)` | CPF | Accepts raw or formatted (`NNN.NNN.NNN-NN`) |
| `is_valid_cnpj(cnpj)` | CNPJ | Accepts raw or formatted (`NN.NNN.NNN/NNNN-NN`) |
| `is_valid_cnj(cnj)` | Processo CNJ | ISO 7064 mod 97 |
| `is_valid_ie(ie, state)` | IE | All 27 states, per-SEFAZ algorithm |
| `is_valid_renavam(renavam)` | RENAVAM | Accepts 8–11 digits |
| `is_valid_titulo_eleitor(titulo)` | Título de Eleitor | SP/MG special rule |

### Generators

| Function | Document | Notes |
|----------|----------|-------|
| `generate_cpf(formatted=False)` | CPF | |
| `generate_cnpj(formatted=False)` | CNPJ | |
| `generate_cnj()` | Processo CNJ | |
| `generate_ie(state)` | IE | `state` = 2-letter code, e.g. `"SP"` |
| `generate_renavam()` | RENAVAM | |
| `generate_titulo_eleitor()` | Título de Eleitor | |

### Formatters (parsers)

| Function | Document | Canonical format |
|----------|----------|-----------------|
| `format_cpf(cpf)` | CPF | `NNN.NNN.NNN-NN` |
| `format_cnpj(cnpj)` | CNPJ | `NN.NNN.NNN/NNNN-NN` |
| `format_cnj(cnj)` | Processo CNJ | `NNNNNNN-DD.AAAA.J.TT.OOOO` |
| `format_ie(ie, state)` | IE | State-specific (see table below) |
| `format_renavam(renavam)` | RENAVAM | `XXXXXXXXXX-X` |
| `format_titulo_eleitor(titulo)` | Título de Eleitor | `XXXX XXXX XXXX` |

All formatters accept raw digit strings or already-formatted strings and raise `ValueError` on invalid input.

---

## IE — Canonical Formats by State

<details>
<summary>All 27 states</summary>

| State | Digits | Canonical format |
|-------|--------|-----------------|
| AC | 13 | `XXX.XXX.XXX/XXX-XX` |
| AL | 9 | raw digits |
| AP | 9 | raw digits |
| AM | 9 | `XX.XXX.XXX-X` |
| BA | 8 or 9 | `XXXXXX-XX` / `XXXXXXX-XX` |
| CE | 9 | `XX.XXX.XXX-X` |
| DF | 13 | `XXX.XXX.XXX/XXX-XX` |
| ES | 9 | raw digits |
| GO | 9 | `XX.XXX.XXX-X` |
| MA | 9 | raw digits |
| MT | 11 | raw digits |
| MS | 9 | raw digits |
| MG | 13 | `XXX.XXX.XXX/XXXX` |
| PA | 9 | `XX-XXXXXX-X` |
| PB | 9 | raw digits |
| PR | 10 | `XXX.XXXXX-XX` |
| PE | 9 or 14 | `XXXXXXX-XX` / `XX.X.XXX.XXXXXXX-X` |
| PI | 9 | raw digits |
| RJ | 8 | `XX.XXX.XX-X` |
| RN | 9 or 10 | `XX.XXX.XXX-X` / `XX.XXX.XXX.X-X` |
| RS | 10 | `XXX/XXXXXXX` |
| RO | 9 or 14 | raw digits |
| RR | 9 | raw digits |
| SC | 9 | `XXX.XXX.XXX` |
| SP | 12 | `XXX.XXX.XXX.XXX` |
| SE | 9 | raw digits |
| TO | 11 | raw digits |

</details>

---

## Design Principles

- **Zero dependencies** — stdlib only
- **100% test coverage** — every branch, every state
- **Strict typing** — `mypy --strict` passes
- **Ruff clean** — format + lint
- **Semantic versioning** — auto-releases via `python-semantic-release`

---

## Roadmap

- [ ] `parse_ie()` — structured parser returning a named dict (sequential, state, check digits)
- [ ] CLI wrapper — `pybrdoc validate cpf 529.982.247-25`
