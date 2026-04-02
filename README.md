# brdocs

**The** Python library for validating, generating, formatting, and masking Brazilian documents — CPF to CNH to Pix keys.

[![PyPI](https://img.shields.io/pypi/v/brdocs.svg)](https://pypi.org/project/brdocs/)
[![Python](https://img.shields.io/pypi/pyversions/brdocs.svg)](https://pypi.org/project/brdocs/)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)]()
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## Installation

```bash
pip install brdocs
pip install brdocs[django]     # Django validators and form fields
pip install brdocs[pydantic]   # Pydantic v2 custom types
pip install brdocs[pandas]    # Pandas Series accessor
pip install brdocs[polars]     # Polars DataFrame expressions
```

Core `brdocs` has **zero dependencies** — stdlib only.

---

## Supported Documents

| Document | Validate | Generate | Format | Parse | Mask |
|----------|:-------:|:--------:|:------:|:-----:|:----:|
| CPF | `is_valid_cpf` | `generate_cpf` | `format_cpf` | `parse_cpf` | `mask_cpf` |
| CNPJ | `is_valid_cnpj` | `generate_cnpj` | `format_cnpj` | `parse_cnpj` | `mask_cnpj` |
| CNJ | `is_valid_cnj` | `generate_cnj` | `format_cnj` | `parse_cnj` | — |
| IE (27 states) | `is_valid_ie` | `generate_ie` | `format_ie` | `parse_ie` | — |
| RENAVAM | `is_valid_renavam` | `generate_renavam` | `format_renavam` | `parse_renavam` | — |
| Título de Eleitor | `is_valid_titulo_eleitor` | `generate_titulo_eleitor` | `format_titulo_eleitor` | `parse_titulo_eleitor` | — |
| CNH | `is_valid_cnh` | `generate_cnh` | `format_cnh` | `parse_cnh` | — |
| PIS/PASEP | `is_valid_pis` | `generate_pis` | `format_pis` | `parse_pis` | — |
| CEP | `is_valid_cep` | — | `format_cep` | `parse_cep` | — |
| CNS (SUS) | `is_valid_cns` | `generate_cns` | `format_cns` | `parse_cns` | — |
| NFe/CTe (44 digits) | `is_valid_nfe` | — | `format_nfe` | `parse_nfe` | — |
| Chave Pix | `classify_pix` | — | — | — | — |

---

## Quick Start

### Core API — Validate, Generate, Format, Parse

```python
import brdocs

# Validate
brdocs.is_valid_cpf("529.982.247-25")        # True
brdocs.is_valid_cnpj("11.222.333/0001-81")    # True
brdocs.is_valid_ie("110.042.490.114", "SP")   # True

# Generate
brdocs.generate_cpf()                          # "52998224725"
brdocs.generate_cpf(formatted=True)           # "529.982.247-25"
brdocs.generate_ie("MG")                      # "062.107.170.0110"

# Format — idempotent (handles raw or formatted input)
brdocs.format_cpf("52998224725")              # "529.982.247-25"
brdocs.format_cnpj("11222333000181")          # "11.222.333/0001-81"

# Parse — returns NamedTuple with structured fields
data = brdocs.parse_cpf("529.982.247-25")
print(data.root, data.check_digits)            # "52998224" "25"
```

### Bulk Operations

```python
# Same-type batch
brdocs.validate_list("cpf", ["529.982.247-25", "000.000.000-00"])  # [True, False]
brdocs.generate_list("cnpj", 3, formatted=True)

# Mixed-type batch
brdocs.validate_docs([("cpf", "529.982.247-25"), ("cnpj", "11.222.333/0001-81")])  # [True, True]
```

### CLI

```bash
brdocs validate cpf 529.982.247-25        # exit 0
brdocs generate cpf --formatted           # 529.982.247-25
brdocs format cpf 52998224725              # 529.982.247-25
brdocs parse cpf 529.982.247-25          # {"root": "52998224", "check_digits": "25", ...}
brdocs mask cpf 529.982.247-25            # ***.982.247-**
```

### LGPD / Secure — Mask & Redact

```python
from brdocs import mask_cpf, mask_cnpj, redact_text, BRDocFilter

mask_cpf("529.982.247-25")    # "***.982.247-**"
mask_cnpj("11.222.333/0001-81")  # "**.222.333/****-**"

# Redact all CPF/CNPJ in free text
redact_text("CPF 529.982.247-25 belongs to João")  # "CPF ***.982.247-** belongs to João"

# Logging filter — attach to any Python logger
import logging
logging.getLogger().addFilter(BRDocFilter())
```

### Data Enrichment

```python
from brdocs import enrich_cnpj, enrich_cep

info = enrich_cnpj("11222333000181")
# CNPJEnrichmentData(cnpj='...', razao_social='...', cnae='...', municipio='...', uf='...', ...)

cep = enrich_cep("01310-100")
# CEPEnrichmentData(cep='...', logradouro='...', bairro='...', cidade='...', uf='...')
```

### Pandas

```python
import pandas as pd
import brdocs.integrations.pandas  # registers .brdocs accessor

df = pd.DataFrame({"cpf": ["529.982.247-25", "000.000.000-00"]})
df["valid"] = df["cpf"].brdocs.is_valid_cpf()   # bool Series
df["formatted"] = df["cpf"].brdocs.format_cpf()  # str Series
df["masked"] = df["cpf"].brdocs.mask_cpf()       # str Series
df["tipo_pix"] = df["pix"].brdocs.classify_pix()  # "CPF" | "CNPJ" | "EMAIL" | "PHONE" | ""
```

### Polars

```python
import polars as pl
import brdocs.integrations.polars  # registers .brdocs on Expr

df = pl.DataFrame({"cpf": ["529.982.247-25", "000.000.000-00"]})
df.select(pl.col("cpf").brdocs.is_valid_cpf())   # Expr → [True, False]
df.select(pl.col("cpf").brdocs.format_cpf())    # Expr → ["529.982.247-25", ...]
df.select(pl.col("cpf").brdocs.mask_cpf())      # Expr → ["***.982.247-**", ...]
df.select(pl.col("pix").brdocs.classify_pix())  # Expr → ["CPF", "CNPJ", "EMAIL", "PHONE", ""]
```

### Django

```python
from brdocs.integrations.django import CPFField, CNPJField, BRDocumentField

class Person(models.Model):
    cpf = CPFField(unique=True)          # validates + strips formatting on save
    cnpj = CNPJField(blank=True)
    documento = BRDocumentField()          # polymorphic — accepts CPF or CNPJ
```

### Pydantic

```python
from pydantic import BaseModel
from brdocs.integrations.pydantic import CPF, CNPJ, IE, CNJ, Renavam, TituloEleitor

class Pessoa(BaseModel):
    cpf: CPF
    cnpj: CNPJ | None = None

class Inscricao(BaseModel):
    ie: IE
    estado: str

p = Pessoa(cpf="529.982.247-25")  # auto-strips to "52998224725"
```



---

## License

[MIT](./LICENSE)
