import re
from typing import NamedTuple


class TituloData(NamedTuple):
    sequential: str  # 8-digit sequential registration number
    state_code: str  # 2-digit state code (01-28)
    check_digits: str  # last 2 digits (V1 and V2)


def parse_titulo_eleitor(titulo: str) -> TituloData:
    """
    Decomposes a Título de Eleitor string into its semantic parts.

    Accepts raw digit strings or already-formatted strings (punctuation stripped).

    Returns:
        TituloData with sequential (8 digits), state_code (2 digits),
        and check_digits (2 digits).

    Raises:
        ValueError: if input is not a str or does not contain exactly 12 digits.
    """
    if not isinstance(titulo, str):
        raise ValueError(f"Expected str, got {type(titulo).__name__}")

    digits = re.sub(r"\D", "", titulo)

    if len(digits) != 12:
        raise ValueError(f"Título de Eleitor must have 12 digits, got {len(digits)}")

    return TituloData(
        sequential=digits[:8],
        state_code=digits[8:10],
        check_digits=digits[10:],
    )


def format_titulo_eleitor(titulo: str) -> str:
    """
    Formats a Título de Eleitor string to the canonical XXXX XXXX XXXX pattern
    (three space-separated groups of 4 digits).

    Accepts any string containing exactly 12 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 12 digits.
    """
    if not isinstance(titulo, str):
        raise ValueError(f"Expected str, got {type(titulo).__name__}")

    digits = re.sub(r"\D", "", titulo)

    if len(digits) != 12:
        raise ValueError(f"Título de Eleitor must have 12 digits, got {len(digits)}")

    return f"{digits[:4]} {digits[4:8]} {digits[8:]}"
