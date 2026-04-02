import re
from typing import NamedTuple


class PISData(NamedTuple):
    base: str
    check_digit: str


def parse_pis(pis: str) -> PISData:
    """
    Decomposes a PIS string into its semantic parts.

    Accepts raw digit strings or already-formatted strings (punctuation stripped).

    Returns:
        PISData with base (first 10 digits) and check_digit (last digit).

    Raises:
        ValueError: if input is not a str or does not contain exactly 11 digits.
    """
    if not isinstance(pis, str):
        raise ValueError(f"Expected str, got {type(pis).__name__}")

    digits = re.sub(r"\D", "", pis)

    if len(digits) != 11:
        raise ValueError(f"PIS must have 11 digits, got {len(digits)}")

    return PISData(base=digits[:10], check_digit=digits[10])


def format_pis(pis: str) -> str:
    """
    Formats a PIS string to the canonical XXX.XXXXX.XX-X pattern.

    Accepts any string containing exactly 11 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 11 digits.
    """
    if not isinstance(pis, str):
        raise ValueError(f"Expected str, got {type(pis).__name__}")

    digits = re.sub(r"\D", "", pis)

    if len(digits) != 11:
        raise ValueError(f"PIS must have 11 digits, got {len(digits)}")

    return f"{digits[:3]}.{digits[3:8]}.{digits[8:10]}-{digits[10]}"
