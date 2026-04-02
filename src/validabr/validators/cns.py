import re


def is_valid_cns(cns: str) -> bool:
    """
    Validates a Brazilian CNS (Cartão Nacional de Saúde).

    Accepts formatted or unformatted strings (punctuation is stripped).

    Definitive cards (start with 1 or 2):
        sum(digit[i] * (15 - i) for i in range(15)) % 11 == 0

    Temporary cards (start with 7, 8, or 9):
        pis_sum = sum(digit[i] * (15 - i) for i in range(12))
        remainder = pis_sum % 11
        result = pis_sum + 2 * (11 - remainder)
        result % 11 == 0

    Returns:
        True if the CNS is valid, False otherwise.
    """
    if not isinstance(cns, str):
        return False

    digits = re.sub(r"\D", "", cns)

    if len(digits) != 15:
        return False

    if digits == digits[0] * 15:
        return False

    nums = [int(d) for d in digits]

    if nums[0] in (1, 2):
        total = sum(nums[i] * (15 - i) for i in range(15))
        return total % 11 == 0
    elif nums[0] in (7, 8, 9):
        pis_sum = sum(nums[i] * (15 - i) for i in range(12))
        remainder = pis_sum % 11
        result = pis_sum + 2 * (11 - remainder)
        return result % 11 == 0

    return False
