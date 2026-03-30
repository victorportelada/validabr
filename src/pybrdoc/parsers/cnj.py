import re


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
