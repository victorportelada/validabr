import re
from typing import NamedTuple


class CNPJData(NamedTuple):
    root: str  # first 8 digits (company identifier)
    branch: str  # 4 digits (branch number; "0001" = matriz)
    check_digits: str  # last 2 digits
    is_matriz: bool  # True when branch == "0001"


def parse_cnpj(cnpj: str) -> CNPJData:
    """
    Decomposes a CNPJ string into its semantic parts.

    Accepts raw digit strings or already-formatted strings (punctuation stripped).

    Returns:
        CNPJData with root (8 digits), branch (4 digits), check_digits (2 digits),
        and is_matriz (True when branch is "0001").

    Raises:
        ValueError: if input is not a str or does not contain exactly 14 digits.
    """
    if not isinstance(cnpj, str):
        raise ValueError(f"Expected str, got {type(cnpj).__name__}")

    digits = re.sub(r"\D", "", cnpj)

    if len(digits) != 14:
        raise ValueError(f"CNPJ must have 14 digits, got {len(digits)}")

    branch = digits[8:12]
    return CNPJData(
        root=digits[:8],
        branch=branch,
        check_digits=digits[12:],
        is_matriz=branch == "0001",
    )


def format_cnpj(cnpj: str) -> str:
    """
    Formats a CNPJ string to the canonical NN.NNN.NNN/NNNN-NN pattern.

    Accepts any string containing exactly 14 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 14 digits.
    """
    if not isinstance(cnpj, str):
        raise ValueError(f"Expected str, got {type(cnpj).__name__}")

    digits = re.sub(r"\D", "", cnpj)

    if len(digits) != 14:
        raise ValueError(f"CNPJ must have 14 digits, got {len(digits)}")

    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
