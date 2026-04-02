import re


def is_valid_nfe(key: str) -> bool:
    """
    Validates a Brazilian NFe/CTe/MDFe Access Key (Chave de Acesso).

    Structure: 44 digits
    Format: XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXX
            (8 groups of 5 + 1 group of 4)

    Validation: Modulo 11 over first 43 digits.
    Weights cycle [2,3,4,5,6,7,8,9,2,3,...] applied right-to-left.
    If remainder is 0 or 1, check digit = 1.
    Otherwise, check digit = 11 - remainder.

    Returns:
        True if the key is valid, False otherwise.
    """
    if not isinstance(key, str):
        return False

    digits = re.sub(r"\D", "", key)

    if len(digits) != 44:
        return False

    if digits == digits[0] * 44:
        return False

    weights = []
    for i in range(42, -1, -1):
        weights.append([2, 3, 4, 5, 6, 7, 8, 9][i % 8])

    total = sum(int(digits[i]) * weights[i] for i in range(43))

    remainder = total % 11

    expected_check = 1 if remainder <= 1 else 11 - remainder
    return int(digits[43]) == expected_check
