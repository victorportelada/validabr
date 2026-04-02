from collections.abc import Callable

from .generators import (
    generate_cep,
    generate_cnh,
    generate_cnj,
    generate_cnpj,
    generate_cpf,
    generate_pis,
    generate_renavam,
    generate_titulo_eleitor,
)
from .parsers import (
    format_cep,
    format_cnh,
    format_cnj,
    format_cnpj,
    format_cpf,
    format_pis,
    format_renavam,
    format_titulo_eleitor,
)
from .validators import (
    is_valid_cep,
    is_valid_cnh,
    is_valid_cnj,
    is_valid_cnpj,
    is_valid_cpf,
    is_valid_pis,
    is_valid_renavam,
    is_valid_titulo_eleitor,
)

_VALIDATORS: dict[str, Callable[[str], bool]] = {
    "cep": is_valid_cep,
    "cnh": is_valid_cnh,
    "cpf": is_valid_cpf,
    "cnpj": is_valid_cnpj,
    "cnj": is_valid_cnj,
    "pis": is_valid_pis,
    "renavam": is_valid_renavam,
    "titulo_eleitor": is_valid_titulo_eleitor,
}

_GENERATORS: dict[str, Callable[[], str]] = {
    "cep": generate_cep,
    "cnh": generate_cnh,
    "cpf": generate_cpf,
    "cnpj": generate_cnpj,
    "cnj": generate_cnj,
    "pis": generate_pis,
    "renavam": generate_renavam,
    "titulo_eleitor": generate_titulo_eleitor,
}

_FORMATTERS: dict[str, Callable[[str], str]] = {
    "cep": format_cep,
    "cnh": format_cnh,
    "cpf": format_cpf,
    "cnpj": format_cnpj,
    "cnj": format_cnj,
    "pis": format_pis,
    "renavam": format_renavam,
    "titulo_eleitor": format_titulo_eleitor,
}


def _resolve_type(doc_type: str) -> str:
    normalized = doc_type.lower()
    if normalized not in _VALIDATORS:
        raise ValueError(f"Unknown doc type: '{doc_type}'. Supported: {sorted(_VALIDATORS)}")
    return normalized


def validate_list(doc_type: str, values: list[str]) -> list[bool]:
    """
    Validates a batch of documents of the same type.

    Args:
        doc_type: Document type (case-insensitive): "cpf", "cnpj", "cnj",
                  "renavam", "titulo_eleitor", "pis", "cep".
        values: List of document strings to validate.

    Returns:
        List of booleans, one per input value.

    Raises:
        ValueError: if doc_type is not recognized.
    """
    normalized = _resolve_type(doc_type)
    validator = _VALIDATORS[normalized]
    return [validator(v) for v in values]


def generate_list(doc_type: str, n: int, formatted: bool = False) -> list[str]:
    """
    Generates n unique valid documents of the same type.

    Args:
        doc_type: Document type (case-insensitive): "cpf", "cnpj", "cnj",
                  "renavam", "titulo_eleitor", "pis", "cep".
        n: Number of documents to generate.
        formatted: If True, returns formatted strings; raw digits otherwise.

    Returns:
        List of n unique valid document strings.

    Raises:
        ValueError: if doc_type is not recognized.
    """
    normalized = _resolve_type(doc_type)
    generator = _GENERATORS[normalized]

    seen: set[str] = set()
    results: list[str] = []

    while len(results) < n:
        value = generator()
        if value not in seen:
            seen.add(value)
            if formatted and normalized in _FORMATTERS:
                value = _FORMATTERS[normalized](value)
            results.append(value)

    return results


def validate_docs(documents: list[tuple[str, str]]) -> list[bool]:
    """
    Validates a mixed-type batch of documents.

    Args:
        documents: List of (doc_type, value) tuples. doc_type is case-insensitive.

    Returns:
        List of booleans, one per input tuple.

    Raises:
        ValueError: if any doc_type is not recognized.
    """
    return [_VALIDATORS[_resolve_type(doc_type)](value) for doc_type, value in documents]
