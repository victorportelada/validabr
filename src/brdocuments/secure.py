"""
LGPD-oriented PII masking and redaction utilities.

Provides:
- mask_cpf / mask_cnpj / mask_pis / mask_cep / mask_cns — named masking functions
- redact_text()  — scan arbitrary text, replace valid Brazilian docs with asterisks
- BRDocFilter    — Python logging.Filter that auto-redacts log records
"""

import logging
import re
from collections.abc import Sequence

from .validators.cnpj import is_valid_cnpj
from .validators.cpf import is_valid_cpf

# ---------------------------------------------------------------------------
# Named mask functions (LGPD-compliant partial masking)
# ---------------------------------------------------------------------------


def mask_cpf(cpf: str) -> str:
    """Mask a CPF: ``529.982.247-25`` → ``***.982.247-**``.

    Accepts formatted or raw digits. Falls back to full asterisks for
    non-standard lengths.
    """
    digits = re.sub(r"\D", "", cpf)
    if len(digits) == 11:
        return f"***.{digits[3:6]}.{digits[6:9]}-**"
    return "*" * len(cpf)


def mask_cnpj(cnpj: str) -> str:
    """Mask a CNPJ: ``11.222.333/0001-81`` → ``**.222.333/****-**``.

    Accepts formatted or raw digits. Falls back to full asterisks for
    non-standard lengths.
    """
    digits = re.sub(r"\D", "", cnpj)
    if len(digits) == 14:
        return f"**.{digits[2:5]}.{digits[5:8]}/****-**"
    return "*" * len(cnpj)


def mask_pis(pis: str) -> str:
    """Mask a PIS: ``123.45678.90-1`` → ``123.45678.**-*``.

    Accepts formatted or raw digits. Falls back to full asterisks for
    non-standard lengths.
    """
    digits = re.sub(r"\D", "", pis)
    if len(digits) == 11:
        return f"{digits[:3]}.{digits[3:8]}.**-{digits[10]}"
    return "*" * len(pis)


def mask_cep(cep: str) -> str:
    """Mask a CEP: ``01310-100`` → ``01310-***``.

    Accepts formatted or raw digits. Falls back to full asterisks for
    non-standard lengths.
    """
    digits = re.sub(r"\D", "", cep)
    if len(digits) == 8:
        return f"{digits[:5]}-***"
    return "*" * len(cep)


def mask_cns(cns: str) -> str:
    """Mask a CNS: ``167 4416 4003 0005`` → ``167 **** **** ****``.

    Accepts formatted or raw digits. Falls back to full asterisks for
    non-standard lengths.
    """
    digits = re.sub(r"\D", "", cns)
    if len(digits) == 15:
        return f"{digits[:3]} **** **** ****"
    return "*" * len(cns)


# ---------------------------------------------------------------------------
# Regex patterns — broad enough to capture candidates; validation narrows them
# ---------------------------------------------------------------------------

_CPF_RE = re.compile(r"\b(\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2})\b")
_CNPJ_RE = re.compile(r"\b(\d{2}[.\s]?\d{3}[.\s]?\d{3}[/\s]?\d{4}[-\s]?\d{2})\b")

_SUPPORTED = ("cpf", "cnpj")

# Map type → (pattern, validator, mask_fn)
_REDACTORS: dict[
    str,
    tuple[re.Pattern[str], object, str],
] = {
    "cpf": (_CPF_RE, is_valid_cpf, "***.***.***-**"),
    "cnpj": (_CNPJ_RE, is_valid_cnpj, "**.***.***/****-**"),
}


def _mask(value: str, placeholder: str) -> str:
    """Return placeholder of same character count as value (digits only preserved)."""
    digits = re.sub(r"\D", "", value)
    return "*" * len(digits)


def redact_text(
    text: str,
    types: Sequence[str] | None = None,
) -> str:
    """
    Scan *text* and replace any valid Brazilian document numbers with asterisks.

    Args:
        text:  Arbitrary string (log line, user input, etc.)
        types: Document types to redact. Defaults to all supported: ``["cpf", "cnpj"]``.
               Pass a subset to limit scope.

    Returns:
        New string with PII replaced. Original string is never mutated.

    Raises:
        ValueError: If an unsupported type is requested.

    Example::

        >>> redact_text("Cliente CPF 529.982.247-25 pagou R$100")
        'Cliente CPF *********** pagou R$100'
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")

    active = list(types) if types is not None else list(_SUPPORTED)

    for doc_type in active:
        if doc_type not in _REDACTORS:
            raise ValueError(f"Unsupported type {doc_type!r}. Supported: {_SUPPORTED}")

    result = text
    for doc_type in active:
        pattern, validator, _ = _REDACTORS[doc_type]

        from collections.abc import Callable

        _validator: Callable[[str], bool] = validator  # type: ignore[assignment]

        def _replace(m: re.Match[str], _v: Callable[[str], bool] = _validator) -> str:
            candidate = m.group(1)
            if _v(candidate):
                return _mask(candidate, "")
            return candidate

        result = pattern.sub(_replace, result)

    return result


# ---------------------------------------------------------------------------
# Logging integration
# ---------------------------------------------------------------------------


class BRDocFilter(logging.Filter):
    """
    A :class:`logging.Filter` that redacts Brazilian PII from log records.

    Attach to any handler or logger to automatically strip CPFs/CNPJs before
    they reach files, stdout, or external sinks (e.g. DataDog, CloudWatch).

    Args:
        types: Document types to redact (default: all supported).
        fields: LogRecord string attributes to scan (default: ``["msg"]``).

    Example::

        import logging
        from brdocuments.secure import BRDocFilter

        handler = logging.StreamHandler()
        handler.addFilter(BRDocFilter())
        logging.getLogger().addHandler(handler)
    """

    def __init__(
        self,
        name: str = "",
        types: Sequence[str] | None = None,
        fields: Sequence[str] | None = None,
    ) -> None:
        super().__init__(name)
        self._types = list(types) if types is not None else list(_SUPPORTED)
        self._fields = list(fields) if fields is not None else ["msg"]

    def filter(self, record: logging.LogRecord) -> bool:
        for field in self._fields:
            value = getattr(record, field, None)
            if isinstance(value, str):
                setattr(record, field, redact_text(value, self._types))
        return True
