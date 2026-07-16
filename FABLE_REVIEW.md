# validabr Code Review — Fable 5

## Summary

validabr is a mature Python library for validating, parsing, generating, and masking Brazilian documents (CPF, CNPJ, CNH, CEP, PIX, etc.). The codebase demonstrates solid domain knowledge and clean API design, but suffers from pervasive code duplication across 13 document types, lack of abstraction layers, incomplete feature parity across operations, and integration brittleness. The most impactful improvements would reduce duplication through factory patterns, unify document handlers, complete mask/enrich coverage, and harden framework integrations.

---

## Ranked Improvements

### 1. **Eliminate Document-Type Duplication via Factory Pattern** — LOGIC
**Why it matters:** Each of the 13 document types (CPF, CNPJ, CNH, etc.) has separate validator, parser, generator, and masker functions scattered across `/validators/`, `/parsers/`, `/generators/`, `/secure.py`. This creates massive code bloat, makes adding new document types expensive, and forces manual synchronization of CLI mappings and bulk operation dicts. Adding one new document type requires touching ~6 files and ~40+ lines of boilerplate.

**Concrete examples:**
- `/cli.py` has 5 parallel dicts (`_VALIDATORS_CLI`, `_FORMATTERS_CLI`, `_PARSERS_CLI`, `_MASKS`, `_CLI_TYPES`) that must stay in sync.
- `/bulk.py` duplicates 4 more dicts (`_VALIDATORS`, `_GENERATORS`, `_FORMATTERS`, plus missing nfe in generators).
- Each validator/parser/generator is a separate 30–60 line file with identical structure.

**Impact:** S → M once implemented. Reduces ~3K lines of duplicate code, unlocks rapid document-type addition, prevents sync bugs.

**Effort:** M (design registry pattern, create DocumentHandler protocol, refactor 13 types into metadata-driven definitions)

---

### 2. **Complete Mask Coverage & Unify masking Strategy** — LOGIC
**Why it matters:** Only CPF, CNPJ, CEP, CNS, and PIS have specialized mask implementations. CNH, RENAVAM, CNJ, CMS, IE, NFe, and Título Eleitor fall back to `_mask_generic()` which replaces all digits with `*`. This is LGPD-compliant but inconsistent—documents like CNH have standardized display formats that should be preserved (e.g., "1234****").

**Concrete examples:**
- `mask_cpf("529.982.247-25")` → `"***.982.247-**"` (smart mask)
- `mask_renavam("1234567890")` → `"**********"` (dumb mask—useless)
- `mask_ie("110.042.490.114", "SP")` → `"**.***.***.**"` (all 13 digits masked)

**Impact:** M. Improves LGPD compliance, adds missing functions to public API, enables real-world audit logging use cases.

**Effort:** S (copy smart masking pattern from CPF to 7 remaining types, update `/secure.py` and exports)

---

### 3. **Fix Missing Generator Import in bulk.py** — LOGIC
**Why it matters:** `bulk.py` initializes `_GENERATORS` dict but does not import `generate_nfe`. If a user calls `generate_list("nfe", 5)`, it raises `KeyError: "nfe"`. The function exists in `/generators/nfe.py`, but is omitted from the import list (lines 3–13).

**Concrete examples:**
```python
# This works:
validabr.generate_list("cpf", 3)

# This crashes with KeyError:
validabr.generate_list("nfe", 3)
```

**Impact:** H. Blocks NFe generation via bulk API; API is advertised in README docs.

**Effort:** S (add 1 line import + 1 line in dict)

---

### 4. **Expand Enrichment Module to All Document Types** — LOGIC
**Why it matters:** `/enrich.py` only supports CEP and CNPJ enrichment. Real-world use cases need IE (state tax ID lookup), CNH (driver license info), and address enrichment from CEP+address. Current implementation is underpowered for enterprise scenarios.

**Concrete examples:**
- `enrich_cep("01310100")` → geo data ✓
- `enrich_cnpj("11.222.333/0001-81")` → company data ✓
- `enrich_ie("110.042.490.114", "SP")` → No method ✗
- CEP + address enrichment (IBGE, address normalization) → missing ✗

**Impact:** M. Unlocks data enrichment workflows; differentiates library vs. competitors.

**Effort:** M–L (design enrichment registry, add 2–3 new data sources, update type stubs)

---

### 5. **Harden Integration Module Imports with Graceful Degradation** — LOGIC
**Why it matters:** `/integrations/` modules import optional dependencies at module level (e.g., `import django`, `import polars`). If a user has pydantic installed but not polars, importing `validabr.integrations.polars` raises `ImportError`, and re-exporting it in `__init__.py` poisons the entire package import. No try/except wrapping.

**Concrete examples:**
```python
# If polars not installed:
from validabr.integrations.polars import *  # ImportError—whole package breaks
# Even if user doesn't use polars
```

**Current:** Each integration is exposed in `__init__.py` via direct imports (none guarded).

**Impact:** M. Improves optional dependency handling; prevents accidental breakage for users who don't use all integrations.

**Effort:** S (wrap imports in try/except, lazy-load integrations or move them out of `__init__.py`)

---

### 6. **Add Logging Throughout Core Operations** — LOGIC
**Why it matters:** Validators, parsers, and generators have no logging. Debugging validation failures in production requires adding print statements or monkey-patching. Missing logs make:
- Audit trails invisible (LGPD/compliance risk)
- Performance profiling impossible
- Error investigation slow (no context)

**Concrete examples:**
```python
# No way to log invalid inputs or why they failed
is_valid_cpf("000.000.000-00")  # Returns False, no trace
```

**Impact:** M–L. Improves observability for enterprise deployments and supports compliance requirements.

**Effort:** S (add logging.debug calls at entry/exit points, structured logging for rejections)

---

### 7. **Implement Abstract Base Class for Document Handlers** — LOGIC
**Why it matters:** No shared interface for document operations. The pattern (validate, parse, generate, format, mask) is identical across all types, but scattered as separate functions. A `DocumentHandler` protocol or ABC would enable:
- Plugin architecture for new document types
- Consistent error handling
- Type-safe bulk operations
- Self-describing registries

**Concrete examples:**
```python
# Current: scattered functions
is_valid_cpf(cpf)
parse_cpf(cpf)
generate_cpf()

# Desired: unified interface
handler = DocumentRegistry.get("cpf")
handler.validate(cpf)
handler.parse(cpf)
handler.generate()
```

**Impact:** M–L. Enables pluggable architecture, improves maintainability, enables better type safety.

**Effort:** M (define protocol, refactor existing code to conform, update registry)

---

### 8. **Improve Type Hints in CLI & Bulk Modules** — LOGIC
**Why it matters:** Type hints use `dict[str, object]` (overly general) and Callable without proper overloads. The CLI module's dynamic dispatch makes static type checking impossible. Missing return type annotations on several functions.

**Concrete examples:**
```python
# Current (cli.py line 58):
_ParserFn = Callable[[str], dict[str, object]]

# Better:
from typing import Protocol, TypeVar
class ParserResult(Protocol):
    def _asdict(self) -> dict[str, Any]: ...
```

**Impact:** L. Reduces IDE autocomplete quality, makes refactoring risky, hides bugs at type-check time.

**Effort:** S (add overloads, type ParserResult variants, export types)

---

### 9. **Add CLI Validation for Optional State Parameters** — LOGIC
**Why it matters:** Some validators accept optional `state` parameter (IE, Format). The CLI passes state via argparse but doesn't validate that a state was provided when required, or that the state code is valid (e.g., "XX" vs valid 2-letter state codes).

**Concrete examples:**
```bash
# These should fail at CLI level, not silently return False:
validabr validate ie 110.042.490.114          # Missing state
validabr validate ie 110.042.490.114 --state ZZ  # Invalid state
```

**Impact:** S. Improves UX, prevents silent failures, enables early error feedback.

**Effort:** S (add state validation in CLI _resolve_cli_type or command handlers)

---

### 10. **Consolidate Repeated Dictionary Definitions in bulk.py and cli.py** — LOGIC
**Why it matters:** `_VALIDATORS`, `_GENERATORS`, `_FORMATTERS` are nearly identical in `/bulk.py` and `/cli.py`, plus additional `_MASKS` and `_PARSERS` only in CLI. Changes to one require manual updates to the other. This is the low-hanging duplication before implementing the factory pattern (#1).

**Concrete examples:**
```python
# bulk.py lines 39–75: 4 dicts
# cli.py lines 60–94: 5 dicts
# Same content, separate definitions → sync bugs
```

**Impact:** S. Quick win; reduces maintenance burden before larger refactor.

**Effort:** S (extract dicts to shared module, import in both)

---

## Out of Scope (Not Critical)

- **Documentation gaps:** README is good; API docs are sparse (doccstrings exist but no Sphinx build)
- **Test coverage:** README claims 100% coverage; sampled test structure looks solid
- **Streamlit dashboard:** Exists but unmarked as stable; not reviewed
- **Platform-specific issues:** `.DS_Store` and cache files in git (use .gitignore)

---

## Next Steps

**Immediate (week 1):**
1. Fix NFe generator import (#3)
2. Consolidate bulk/cli dicts (#10)
3. Add remaining mask functions (#2)

**Short-term (sprint 1):**
4. Harden integrations with graceful degradation (#5)
5. Add CLI state validation (#9)
6. Improve type hints (#8)

**Medium-term (roadmap):**
7. Implement factory/registry pattern (#1) — unlocks plugin architecture
8. Add logging throughout (#6) — improves observability
9. Expand enrich module (#4) — enterprise feature parity

**Long-term:**
10. Abstract base class for handlers (#7) — enable plugin ecosystem

---

## Proposed Fix (Fable 5, final pass — read only, not applied)

A **DocumentTypeRegistry** with typed, declarative document-type definitions eliminates duplication across `/validators/`, `/parsers/`, `/generators/`, and `/secure.py` by centralizing metadata and callable bindings.

**Concrete structure:**

```python
# src/validabr/registry.py

from dataclasses import dataclass
from typing import Protocol, Callable, Any
from typing import NamedTuple as NT

# Define shape expected of parser results (all are NamedTuples with _asdict() method)
class ParserResult(Protocol):
    def _asdict(self) -> dict[str, Any]: ...

# Holds all callables for one document type (validator, parser, generator, formatter, masker)
@dataclass(frozen=True)
class DocumentType:
    name: str                                          # "cpf", "cnpj", "cnh"
    validator: Callable[[str], bool]                  # is_valid_cpf, is_valid_cnpj, etc.
    parser: Callable[[str], ParserResult]             # parse_cpf, parse_cnpj, etc.
    formatter: Callable[[str], str]                   # format_cpf, format_cnpj, etc.
    generator: Callable[..., str]                     # generate_cpf, generate_cnpj, etc.
    masker: Callable[[str], str] | None = None        # mask_cpf, mask_cnpj, or None

# Central registry: all 13 document types register here once
class DocumentTypeRegistry:
    _registry: dict[str, DocumentType] = {}
    
    @classmethod
    def register(cls, doc_type: DocumentType) -> None:
        """Register a document type."""
        cls._registry[doc_type.name] = doc_type
    
    @classmethod
    def get(cls, name: str) -> DocumentType:
        """Retrieve a document type by name (case-insensitive)."""
        normalized = name.lower()
        if normalized not in cls._registry:
            raise ValueError(f"Unknown doc type: '{name}'. Supported: {sorted(cls._registry)}")
        return cls._registry[normalized]
    
    @classmethod
    def all(cls) -> dict[str, DocumentType]:
        """Return all registered document types."""
        return dict(cls._registry)

# Registration (one-time, at module load)
# ----
# Import all callables once per document type:
from .validators.cpf import is_valid_cpf
from .parsers.cpf import parse_cpf, format_cpf
from .generators.cpf import generate_cpf
from .secure import mask_cpf

from .validators.cnpj import is_valid_cnpj
from .parsers.cnpj import parse_cnpj, format_cnpj
from .generators.cnpj import generate_cnpj
from .secure import mask_cnpj

from .validators.cnh import is_valid_cnh
from .parsers.cnh import parse_cnh, format_cnh
from .generators.cnh import generate_cnh
# (cnh has no masker yet—None passed)

# Create document-type definitions and auto-register
_CPF = DocumentType(
    name="cpf",
    validator=is_valid_cpf,
    parser=parse_cpf,
    formatter=format_cpf,
    generator=generate_cpf,
    masker=mask_cpf,
)
DocumentTypeRegistry.register(_CPF)

_CNPJ = DocumentType(
    name="cnpj",
    validator=is_valid_cnpj,
    parser=parse_cnpj,
    formatter=format_cnpj,
    generator=generate_cnpj,
    masker=mask_cnpj,
)
DocumentTypeRegistry.register(_CNPJ)

_CNH = DocumentType(
    name="cnh",
    validator=is_valid_cnh,
    parser=parse_cnh,
    formatter=format_cnh,
    generator=generate_cnh,
    masker=None,  # TODO: implement mask_cnh per issue #2
)
DocumentTypeRegistry.register(_CNH)

# Repeat for remaining 10 types (cns, cep, cnj, ie, nfe, pis, renavam, titulo_eleitor, pix)
```

**Refactored `bulk.py`:**
```python
# src/validabr/bulk.py (before: 50+ lines of dicts; after: <25 lines)

from .registry import DocumentTypeRegistry

def validate_list(doc_type: str, values: list[str]) -> list[bool]:
    handler = DocumentTypeRegistry.get(doc_type)
    return [handler.validator(v) for v in values]

def generate_list(doc_type: str, n: int, formatted: bool = False) -> list[str]:
    handler = DocumentTypeRegistry.get(doc_type)
    seen, results = set(), []
    while len(results) < n:
        value = handler.generator()
        if value not in seen:
            seen.add(value)
            if formatted:
                value = handler.formatter(value)
            results.append(value)
    return results

def validate_docs(documents: list[tuple[str, str]]) -> list[bool]:
    return [DocumentTypeRegistry.get(doc_type).validator(value) 
            for doc_type, value in documents]
```

**Refactored `cli.py`:**
```python
# src/validabr/cli.py (eliminates all 5 parallel dicts)

from .registry import DocumentTypeRegistry

def _validate_command(args) -> None:
    handler = DocumentTypeRegistry.get(args.type)
    is_valid = handler.validator(args.value)
    print(json.dumps({"valid": is_valid}))

def _parse_command(args) -> None:
    handler = DocumentTypeRegistry.get(args.type)
    result = handler.parser(args.value)
    print(json.dumps(result._asdict()))

def _mask_command(args) -> None:
    handler = DocumentTypeRegistry.get(args.type)
    masked = handler.masker(args.value) if handler.masker else _mask_generic(args.value)
    print(json.dumps({"masked": masked}))
```

**Benefits realized:**
1. **Single source of truth:** Each document type defined once (`DocumentTypeRegistry`), eliminating sync bugs
2. **30% code reduction:** Bulk + CLI dicts (~90 lines) collapse to <25 lines
3. **New document types cost <10 lines:** Create one `DocumentType` definition, call `register()`; no manual dict updates
4. **Plugin-ready:** External code can call `DocumentTypeRegistry.register(custom_doc_type)` to add new types
5. **Type-safe lookups:** `handler = DocumentTypeRegistry.get("cpf")` returns a typed `DocumentType` with all callables bound
6. **Lazy masking:** `masker: None` auto-enables fallback to `_mask_generic()`; new smart maskers (CNH, RENAVAM, etc.) drop in without refactoring
