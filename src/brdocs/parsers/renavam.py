import re
from typing import NamedTuple


class RenavamData(NamedTuple):
    base: str  # first 10 digits (left-padded to 11 total)
    check_digit: str  # last digit


def parse_renavam(renavam: str) -> RenavamData:
    """
    Decomposes a RENAVAM string into its semantic parts.

    Accepts 8-11 digit strings; shorter values are left-padded with zeros to 11 digits.

    Returns:
        RenavamData with base (10 digits) and check_digit (1 digit).

    Raises:
        ValueError: if input is not a str or has fewer than 8 or more than 11 digits.
    """
    if not isinstance(renavam, str):
        raise ValueError(f"Expected str, got {type(renavam).__name__}")

    digits = re.sub(r"\D", "", renavam)

    if len(digits) < 8 or len(digits) > 11:
        raise ValueError(f"RENAVAM must have 8-11 digits, got {len(digits)}")

    digits = digits.zfill(11)
    return RenavamData(base=digits[:10], check_digit=digits[10])


def format_renavam(renavam: str) -> str:
    """
    Formats a RENAVAM string to the canonical XXXXXXXXXX-X pattern (11 digits with
    a hyphen before the check digit).

    Accepts 8-11 digit strings; shorter values are left-padded with zeros to 11 digits.

    Raises:
        ValueError: if the input has fewer than 8 or more than 11 digits.
    """
    if not isinstance(renavam, str):
        raise ValueError(f"Expected str, got {type(renavam).__name__}")

    digits = re.sub(r"\D", "", renavam)

    if len(digits) < 8 or len(digits) > 11:
        raise ValueError(f"RENAVAM must have 8-11 digits, got {len(digits)}")

    digits = digits.zfill(11)

    return f"{digits[:10]}-{digits[10]}"
