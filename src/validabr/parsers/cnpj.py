import re
from typing import NamedTuple


class CNPJData(NamedTuple):
    root: str  # first 8 characters (company identifier; may be alphanumeric)
    branch: str  # 4 characters (branch number; may be alphanumeric; "0001" = matriz)
    check_digits: str  # last 2 digits (always numeric)
    is_matriz: bool  # True when branch == "0001"


def parse_cnpj(cnpj: str) -> CNPJData:
    """
    Decomposes a CNPJ string into its semantic parts.

    Accepts raw strings or formatted strings (dots, slashes, hyphens stripped).
    Handles both classic numeric and alphanumeric formats (IN RFB 2.229/2024).

    Returns:
        CNPJData with root (8 chars), branch (4 chars), check_digits (2 digits),
        and is_matriz (True when branch is "0001").

    Raises:
        ValueError: if input is not a str or does not contain exactly 14 characters.
    """
    if not isinstance(cnpj, str):
        raise ValueError(f"Expected str, got {type(cnpj).__name__}")

    cleaned = re.sub(r"[\s.\/-]", "", cnpj).upper()

    if len(cleaned) != 14:
        raise ValueError(f"CNPJ must have 14 characters, got {len(cleaned)}")

    branch = cleaned[8:12]
    return CNPJData(
        root=cleaned[:8],
        branch=branch,
        check_digits=cleaned[12:],
        is_matriz=branch == "0001",
    )


def format_cnpj(cnpj: str) -> str:
    """
    Formats a CNPJ string to the canonical NN.NNN.NNN/NNNN-NN pattern.

    Accepts any string containing exactly 14 characters after stripping
    formatting (dots, slashes, hyphens, whitespace). Handles both classic
    numeric and alphanumeric formats (IN RFB 2.229/2024).

    Raises:
        ValueError: if the input does not contain exactly 14 characters.
    """
    if not isinstance(cnpj, str):
        raise ValueError(f"Expected str, got {type(cnpj).__name__}")

    cleaned = re.sub(r"[\s.\/-]", "", cnpj).upper()

    if len(cleaned) != 14:
        raise ValueError(f"CNPJ must have 14 characters, got {len(cleaned)}")

    return f"{cleaned[:2]}.{cleaned[2:5]}.{cleaned[5:8]}/{cleaned[8:12]}-{cleaned[12:]}"
