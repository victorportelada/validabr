import re

_WEIGHTS = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def is_valid_renavam(renavam: str) -> bool:
    """
    Validates a Brazilian RENAVAM (Registro Nacional de Veículos Automotores).

    Accepts 11-digit strings, optionally formatted with a hyphen before the
    last digit (e.g. "0012345678-9"). Shorter numbers (8-10 digits) are
    padded with leading zeros to 11 digits before validation.

    Returns True if the check digit is correct, False otherwise.
    """
    if not isinstance(renavam, str):
        return False

    cleaned = re.sub(r"\D", "", renavam)

    if len(cleaned) < 8 or len(cleaned) > 11:
        return False

    # Pad to 11 digits with leading zeros
    cleaned = cleaned.zfill(11)

    # Reject all-zeros
    if cleaned == "0" * 11:
        return False

    digits = [int(d) for d in cleaned]
    total = sum(d * w for d, w in zip(digits[:10], _WEIGHTS, strict=False))
    remainder = total % 11

    if remainder == 0:
        check = 0
    elif remainder == 1:
        # remainder == 1 means no valid check digit exists → invalid
        return False
    else:
        check = 11 - remainder

    return digits[10] == check
