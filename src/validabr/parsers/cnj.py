import re
from typing import NamedTuple


class CNJData(NamedTuple):
    sequence: str  # 7-digit process sequence number
    check_digits: str  # 2-digit check digits (DD, ISO 7064 mod 97)
    year: str  # 4-digit filing year
    justice_segment: str  # 1-digit justice segment (J)
    tribunal: str  # 2-digit tribunal code (TT)
    origin_unit: str  # 4-digit origin unit (OOOO)


def parse_cnj(cnj: str) -> CNJData:
    """
    Decomposes a CNJ process number into its semantic parts.

    Accepts formatted (NNNNNNN-DD.AAAA.J.TT.OOOO) or raw 20-digit strings.

    Returns:
        CNJData with all six fields of the CNJ process number.

    Raises:
        ValueError: if input is not a str or does not contain exactly 20 digits.
    """
    if not isinstance(cnj, str):
        raise ValueError(f"Expected str, got {type(cnj).__name__}")

    digits = re.sub(r"\D", "", cnj)

    if len(digits) != 20:
        raise ValueError(f"CNJ must have 20 digits, got {len(digits)}")

    return CNJData(
        sequence=digits[0:7],
        check_digits=digits[7:9],
        year=digits[9:13],
        justice_segment=digits[13:14],
        tribunal=digits[14:16],
        origin_unit=digits[16:20],
    )


def format_cnj(cnj: str) -> str:
    """
    Formats a CNJ process number to the canonical NNNNNNN-DD.AAAA.J.TT.OOOO pattern.

    Accepts any string containing exactly 20 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 20 digits.
    """
    if not isinstance(cnj, str):
        raise ValueError(f"Expected str, got {type(cnj).__name__}")

    digits = re.sub(r"\D", "", cnj)

    if len(digits) != 20:
        raise ValueError(f"CNJ must have 20 digits, got {len(digits)}")

    nnnnnnn = digits[0:7]
    dd = digits[7:9]
    aaaa = digits[9:13]
    j = digits[13:14]
    tt = digits[14:16]
    oooo = digits[16:20]

    return f"{nnnnnnn}-{dd}.{aaaa}.{j}.{tt}.{oooo}"
