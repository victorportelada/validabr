import re
from typing import NamedTuple


class CEPData(NamedTuple):
    region: str
    suffix: str


def parse_cep(cep: str) -> CEPData:
    """
    Decomposes a CEP string into its semantic parts.

    Accepts raw digit strings or already-formatted strings (punctuation stripped).

    Returns:
        CEPData with region (first 5 digits) and suffix (last 3 digits).

    Raises:
        ValueError: if input is not a str or does not contain exactly 8 digits.
    """
    if not isinstance(cep, str):
        raise ValueError(f"Expected str, got {type(cep).__name__}")

    digits = re.sub(r"\D", "", cep)

    if len(digits) != 8:
        raise ValueError(f"CEP must have 8 digits, got {len(digits)}")

    return CEPData(region=digits[:5], suffix=digits[5:])


def format_cep(cep: str) -> str:
    """
    Formats a CEP string to the canonical XXXXX-XXX pattern.

    Accepts any string containing exactly 8 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 8 digits.
    """
    if not isinstance(cep, str):
        raise ValueError(f"Expected str, got {type(cep).__name__}")

    digits = re.sub(r"\D", "", cep)

    if len(digits) != 8:
        raise ValueError(f"CEP must have 8 digits, got {len(digits)}")

    return f"{digits[:5]}-{digits[5:]}"
