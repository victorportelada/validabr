import re


def is_valid_cnh(cnh: str) -> bool:
    """
    Validates a Brazilian CNH (Carteira Nacional de Habilitação).

    Accepts formatted or unformatted strings (punctuation is stripped).
    Uses two-pass Modulo 11 with distinct ascending/descending weights and
    a DSC (discriminator) flag carried from the first pass into the second.

    Returns:
        True if the CNH is structurally valid, False otherwise.
    """
    if not isinstance(cnh, str):
        return False

    digits = re.sub(r"\D", "", cnh)

    if len(digits) != 11:
        return False

    if digits == digits[0] * 11:
        return False

    nums = [int(d) for d in digits]

    # First pass — descending weights [9, 8, 7, 6, 5, 4, 3, 2, 1]
    sum1 = sum(nums[i] * (9 - i) for i in range(9))
    remainder1 = sum1 % 11
    if remainder1 >= 10:
        first_digit = 0
        dsc = 2
    else:
        first_digit = remainder1
        dsc = 0

    if nums[9] != first_digit:
        return False

    # Second pass — ascending weights [1, 2, 3, 4, 5, 6, 7, 8, 9] + DSC
    sum2 = dsc + sum(nums[i] * (i + 1) for i in range(9))
    remainder2 = sum2 % 11
    second_digit = 0 if remainder2 >= 10 else remainder2

    return nums[10] == second_digit
