import re
from typing import Literal, NamedTuple


class CNSData(NamedTuple):
    digits: str
    card_type: Literal["definitive", "temporary"]


def parse_cns(cns: str) -> CNSData:
    """
    Decomposes a CNS string into its semantic parts.

    Accepts raw digit strings or already-formatted strings (punctuation stripped).

    Returns:
        CNSData with digits (15 digits) and card_type ("definitive" or "temporary").

    Raises:
        ValueError: if input is not a str or does not contain exactly 15 digits.
    """
    if not isinstance(cns, str):
        raise ValueError(f"Expected str, got {type(cns).__name__}")

    digits = re.sub(r"\D", "", cns)

    if len(digits) != 15:
        raise ValueError(f"CNS must have 15 digits, got {len(digits)}")

    nums = [int(d) for d in digits]
    if nums[0] in (1, 2):
        card_type: Literal["definitive", "temporary"] = "definitive"
    elif nums[0] in (7, 8, 9):
        card_type = "temporary"
    else:
        card_type = "definitive"

    return CNSData(digits=digits, card_type=card_type)


def format_cns(cns: str) -> str:
    """
    Formats a CNS string to the canonical XXX XXXX XXXX XXXX pattern.

    Accepts any string containing exactly 15 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 15 digits.
    """
    if not isinstance(cns, str):
        raise ValueError(f"Expected str, got {type(cns).__name__}")

    digits = re.sub(r"\D", "", cns)

    if len(digits) != 15:
        raise ValueError(f"CNS must have 15 digits, got {len(digits)}")

    return f"{digits[:3]} {digits[3:7]} {digits[7:11]} {digits[11:]}"
