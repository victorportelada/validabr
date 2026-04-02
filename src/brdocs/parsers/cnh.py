import re
from typing import NamedTuple


class CNHData(NamedTuple):
    registration: str  # first 9 digits (base registration number)
    check_digits: str  # last 2 digits (first and second verifiers)


def parse_cnh(cnh: str) -> CNHData:
    """
    Decomposes a CNH string into its semantic parts.

    Accepts raw digit strings or already-formatted strings (punctuation stripped).

    Returns:
        CNHData with registration (9 digits) and check_digits (2 digits).

    Raises:
        ValueError: if input is not a str or does not contain exactly 11 digits.
    """
    if not isinstance(cnh, str):
        raise ValueError(f"Expected str, got {type(cnh).__name__}")

    digits = re.sub(r"\D", "", cnh)

    if len(digits) != 11:
        raise ValueError(f"CNH must have 11 digits, got {len(digits)}")

    return CNHData(registration=digits[:9], check_digits=digits[9:])


def format_cnh(cnh: str) -> str:
    """
    Normalizes a CNH string to its canonical 11-digit form (no separators).

    CNH has no standard punctuation mask — this function strips all non-digit
    characters and validates the length.

    Raises:
        ValueError: if the input does not contain exactly 11 digits.
    """
    if not isinstance(cnh, str):
        raise ValueError(f"Expected str, got {type(cnh).__name__}")

    digits = re.sub(r"\D", "", cnh)

    if len(digits) != 11:
        raise ValueError(f"CNH must have 11 digits, got {len(digits)}")

    return digits
