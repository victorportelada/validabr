import re

_EXCLUDED_LETTERS = frozenset("IOUQF")
_ALLOWED_CHARS = frozenset(
    "0123456789" + "".join(c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in _EXCLUDED_LETTERS)
)
_WEIGHTS_DV1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_WEIGHTS_DV2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def _char_value(c: str) -> int:
    return ord(c) - 48


def is_valid_cnpj(cnpj: str) -> bool:
    """
    Validates a Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica).

    Accepts both the classic numeric format (12.345.678/0001-95) and the new
    alphanumeric format introduced by IN RFB 2.229/2024 (12.ABC.345/01DE-35).
    Formatted and unformatted strings are both accepted.
    """
    if not isinstance(cnpj, str):
        return False

    cleaned = re.sub(r"[\s.\/-]", "", cnpj).upper()

    if len(cleaned) != 14:
        return False

    # First 12 positions: digits or allowed letters (excludes I, O, U, Q, F)
    if not all(c in _ALLOWED_CHARS for c in cleaned[:12]):
        return False

    # Check digits (positions 13-14) must always be numeric
    if not cleaned[12:].isdigit():
        return False

    # Reject trivially invalid all-same sequences
    if cleaned == cleaned[0] * 14:
        return False

    base = cleaned[:12]
    r1 = sum(_char_value(c) * w for c, w in zip(base, _WEIGHTS_DV1, strict=True)) % 11
    d1 = 0 if r1 < 2 else 11 - r1

    if int(cleaned[12]) != d1:
        return False

    r2 = sum(_char_value(c) * w for c, w in zip(base + str(d1), _WEIGHTS_DV2, strict=True)) % 11
    d2 = 0 if r2 < 2 else 11 - r2

    return int(cleaned[13]) == d2
