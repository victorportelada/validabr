# Brdocs Roadmap & Vision (v0.2.0 → v2.0.0)

This document serves as the canonical source of truth for the future development of `brdocs`. It outlines the strategic direction, architectural decisions, and specific implementation tasks required for future AI agents or developers to elevate the library into the industry standard toolkit for handling, enriching, and securing Brazilian data.

Our vision is no longer just "validation". It is to build an **Enterprise Toolkit** that solves actual business problems (LGPD, Data Engineering, PII Enrichment).

## Principles & Guardrails

Before starting any work on this roadmap, ensure you adhere to the project's core tenets:
1. **Zero Core Dependencies**: The `src/brdocs/` core (excluding `integrations/`) must rely *only* on the Python Standard Library.
2. **100% Branch Coverage**: All validators, generators, and formatters must maintain exact 100% test coverage. Avoid generic `Exception` types; raise precise `ValueError` exceptions with clear, descriptive messages.
3. **Impeccable Linting**: Standardized on `ruff` for linting/formatting and `mypy --strict` for typing. 
4. **Idempotent APIs**: Formatting and parsing functions must handle *both* raw digit strings and already-formatted strings gracefully without crashing. 

---

## Phase 1: Structured Parsers & CLI

The current API (`is_valid_*`, `generate_*`, `format_*`) is complete. The next natural step is to provide structured data representations and developer ergonomics.

### 1. Structured Data Parsers (`parse_*`)

Instead of just returning formatted strings, `brdocs` should offer parsing functions that decompose strings into standard Python `dataclasses` or `NamedTuple` objects.

*   `parse_cpf(cpf: str) -> CPFData`
    *   Decomposes into: `root` (first 8 digits), `region` (9th digit indicating emission state like SP, RJ, etc.), and `check_digits` (last 2 digits).
*   `parse_cnpj(cnpj: str) -> CNPJData`
    *   Decomposes into: `root` (first 8 digits), `branch` (4 digits, e.g., `0001` or `0002`), and `check_digits` (last 2 digits). Provide a boolean helper `is_matriz()`.
*   `parse_cnj(cnj: str) -> CNJData`
    *   Decomposes the complex CNJ process number into: `sequence`, `check_digits`, `year`, `justice_segment`, `tribunal`, and `origin_unit`.
*   `parse_ie(ie: str, state: str) -> IEData`
    *   State-specific decomposition based on SEFAZ schemas (extracting root, registration types, and variable-length check digits per state).
*   `parse_renavam(renavam: str) -> RenavamData`
    *   Decomposes into: `base` and `check_digit`.
*   `parse_titulo_eleitor(titulo: str) -> TituloData`
    *   Decomposes into: `sequential`, `state_code` (UF), and `check_digits`.

### 2. Command-Line Interface (CLI)

Build a zero-dependency CLI using Python's native `argparse`. Expose it via `[project.scripts]` in `pyproject.toml`.

**Commands:**
*   `brdocs validate <type> <value>` (Returns exit code 0 if valid, 1 if invalid, printing standard output).
*   `brdocs generate <type> [--formatted] [--state XX]`
*   `brdocs format <type> <value> [--state XX]`
*   `brdocs mask <type> <value>` (Anonymizes the input).
*   `brdocs parse <type> <value> [--state XX]` (Outputs structured JSON).

---

## Phase 2: Web Framework Integrations

To ensure maximum adoption, the library must integrate seamlessly into modern Python frameworks. We will accomplish this by creating a structured `src/brdocs/integrations/` module. Frameworks will be defined as "optional dependencies" (`pip install brdocs[pydantic]`).

### 1. Pydantic v2 (FastAPI, SQLModel)
Create custom types using `pydantic.functional_validators`.
*   Module: `src/brdocs/integrations/pydantic.py`
*   Exports: `CPF`, `CNPJ`, `IE`, `CNJ`, `Renavam`, `TituloEleitor`
*   Behavior: Provide `BeforeValidator` annotations that validate string inputs using `is_valid_*` and cast them into their canonical string formats or structured dataclasses.
*   Example:
    ```python
    from pydantic import BaseModel
    from brdocs.integrations.pydantic import CPF 

    class UserData(BaseModel):
        document: CPF # Raises standard Pydantic ValidationError if invalid
    ```

### 2. Django & Django REST Framework (DRF)
*   Module: `src/brdocs/integrations/django.py`
*   Exports: `CPFField`, `CNPJField`, `BRDocumentField` (polymorphic constraint).
*   Implement native Django validators (`django.core.exceptions.ValidationError`) and standard DB Form Fields. 

*Agent Implementation Note: All integration modules must use `try/except ImportError` around framework imports so that `brdocs` can still be installed safely in environments without Django/Pydantic.*

---

## Phase 3: Expand Document Coverage

Broaden `brdocs` to be the undisputed standard by supporting the remaining common Brazilian documents:

### 1. PIS / PASEP / NIT
*   **Structure:** 11 digits. Formatting: `XXX.XXXXX.XX-X`.
*   **Logic:** Standard Modulo 11 validation check.
*   **Tasks:** Build `is_valid_pis()`, `generate_pis()`, `format_pis()`.

### 2. CNS (Cartão Nacional de Saúde / SUS)
*   **Structure:** 15 digits.
*   **Logic:** Heavily integrated logically (Modulo 11). Often starts with 1, 2, 7, 8, or 9. The check digit logic varies depending on the initial digits (Definitive vs. Temporary cards).
*   **Tasks:** Build `is_valid_cns()`, `generate_cns()`, `format_cns()` (`XXX XXXX XXXX XXXX`).

### 3. Chave de Acesso NFe / CTe / MDFe
*   **Structure:** 44 numeric digits.
*   **Decomposition:** UF (2), AAMM (4), CNPJ (14), Model (2), Series (3), Number (9), Emission Type (1), Random Code (8), Check Digit (1).
*   **Logic:** Standard Modulo 11 validation across all previous 43 digits.
*   **Tasks:** Build `is_valid_nfe()`, `parse_nfe()` (highly valuable for parsing metadata directly out of invoices). 

### 4. CEP (Postal Code)
*   **Structure:** 8 digits.
*   **Logic:** Mostly regex and sequence length. No complex algorithmic check digits, but vital for completeness.
*   **Tasks:** Build `is_valid_cep()` and `format_cep()` (`XXXXX-XXX`).

### 5. Documentos do Pix (Bacen)
*   **Logic:** Validate standard string patterns conforming to Banco Central do Brasil.
*   **Keys:** `CPF / CNPJ`, `Email`, `Telefone Celular` (+55...), `EVP` (Random UUID).
*   **Tasks:** Return an enum or type identifying the validated PIX Key type.

---

## Phase 4: LGPD & Security Toolkit (Anonymization & Scanning)

To differentiate `brdocs` entirely from simple validation scripts, introduce a robust toolset designed to solve LGPD (Lei Geral de Proteção de Dados) challenges.

### 1. PII Redaction (`mask_*` and `anonymizer`)
*   Create a module (`src/brdocs/secure.py` or similar) containing masking operators.
*   Examples: `mask_cpf("123.456.789-00")` -> `"***.456.789-**"`
*   Build a global text scanner: `brdocs.secure.redact_text(log_string, types=["CPF", "CNPJ"])`. This should scan standard text logs, identify potentially valid documents (via regex + modulo 11 validation combined), and replace them with asterisks natively.

### 2. Log Middleware & Integrations
*   Provide a drop-in Python `logging.Filter` to attach to enterprise loggers, automatically filtering out sensitive CPFs/CNPJs before saving logs to a file or DataDog.

---

## Phase 5: Open API Data Enrichment

Move beyond mathematical validation to real-world context data by connecting to freely available public APIs. Give developers *business value*.

### 1. `brdocs.enrich` Module
*   Add optional API-fetching methods (e.g., `enrich_cnpj(cnpj: str)`).
*   **Integrations:**
    *   Fetch CNPJ data (ReceitaWS or BrasilAPI) to pull: `razao_social`, `cnae`, `status_ativo`, `endereco`.
    *   Fetch CEP data (BrasilAPI) to pull: `logradouro`, `cidade`, `estado`.
*   **Architecture:** Use pure `urllib` to retain the zero-dependency rule, but return strongly-typed datastructures (or dicts) handling error states perfectly (rate limits, network errors).

---

## Phase 6: Enterprise Data Engineering (Pandas / Polars)

Position `brdocs` as the defacto library for Brazilian Data Engineering workloads. 1 million rows of CPFs should validate in less than a second.

### 1. Pandas `Series` Accessor Extensions (`.brdocs` accessor)
*   **Feature:** Add a standard Pandas accessor when `pandas` is installed.
*   **Example:** `df['is_valid'] = df['cpf'].brdocs.is_valid_cpf()`
### 2. Polars Native Extensions (Python API)
*   **Feature:** Integrate vectorised support for incredibly massive datasets via Polars Extension API logic.
*   **Why:** Cleaning big datasets that contain "bad" CNPJs or CPFs is a standard and massive pain point for any Data team traversing Brazilian CRM data.

---

## Agent Handoff Checklist

If you are an AI reading this file to continue work:
1. Ensure your implementation remains inside `src/brdocs/`.
2. Do not introduce requirements directly into `pyproject.toml` base dependencies. Use `[project.optional-dependencies]` if strictly needed.
3. Every new algorithm requires a symmetric implementation of: _Generator_, _Validator_, _Formatter_, and _Parser_.
4. Achieve exactly 100% code coverage. Run tests using `uv run pytest`. Verify linting using `uv run ruff check src/ tests/` and `uv run mypy src/ tests/`. 
5. Always mark Python string masks strictly (e.g., distinguishing strictly between CNPJ roots and branch indicators).
