import re
from typing import NamedTuple


class CPFData(NamedTuple):
    root: str  # first 9 digits
    region_digit: str  # 9th digit (indicates emission region)
    check_digits: str  # last 2 digits


def parse_cpf(cpf: str) -> CPFData:
    """
    Decomposes a CPF string into its semantic parts.

    Accepts raw digit strings or already-formatted strings (punctuation stripped).

    Returns:
        CPFData with root (9 digits), region_digit (9th digit), check_digits (2 digits).

    Raises:
        ValueError: if input is not a str or does not contain exactly 11 digits.
    """
    if not isinstance(cpf, str):
        raise ValueError(f"Expected str, got {type(cpf).__name__}")

    digits = re.sub(r"\D", "", cpf)

    if len(digits) != 11:
        raise ValueError(f"CPF must have 11 digits, got {len(digits)}")

    return CPFData(root=digits[:9], region_digit=digits[8], check_digits=digits[9:])


def format_cpf(cpf: str) -> str:
    """
    Formats a CPF string to the canonical NNN.NNN.NNN-NN pattern.

    Accepts any string containing exactly 11 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 11 digits.
    """
    if not isinstance(cpf, str):
        raise ValueError(f"Expected str, got {type(cpf).__name__}")

    digits = re.sub(r"\D", "", cpf)

    if len(digits) != 11:
        raise ValueError(f"CPF must have 11 digits, got {len(digits)}")

    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
