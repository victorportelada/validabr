import re


def is_valid_pis(pis: str) -> bool:
    """
    Validates a Brazilian PIS/PASEP/NIT.

    Args:
        pis (str): The PIS string to validate. Can contain punctuation.

    Returns:
        bool: True if the PIS is valid, False otherwise.
    """
    if not isinstance(pis, str):
        return False

    numbers = re.sub(r"\D", "", pis)

    if len(numbers) != 11:
        return False

    if numbers == numbers[0] * 11:
        return False

    weights = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_ = sum(int(numbers[i]) * weights[i] for i in range(10))

    remainder = sum_ % 11
    check_digit = 0 if remainder < 2 else 11 - remainder

    return check_digit == int(numbers[10])
