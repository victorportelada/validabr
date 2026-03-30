import re


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
