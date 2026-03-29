import re


def is_valid_cpf(cpf: str) -> bool:
    """
    Validates a Brazilian CPF (Cadastro de Pessoas Físicas).

    Args:
        cpf (str): The CPF string to format. Can contain punctuation (dots and hyphens).

    Returns:
        bool: True if the CPF is valid, False otherwise.
    """
    if not isinstance(cpf, str):
        return False

    # Remove all non-digit characters
    numbers = re.sub(r"\D", "", cpf)

    if len(numbers) != 11:
        return False

    # Eliminate known invalid CPFs (all the same digits)
    if numbers == numbers[0] * 11:
        return False

    # Calculate first verifier digit
    sum_1 = sum(int(numbers[i]) * (10 - i) for i in range(9))
    digit_1 = (sum_1 * 10) % 11
    if digit_1 == 10:
        digit_1 = 0

    if digit_1 != int(numbers[9]):
        return False

    # Calculate second verifier digit
    sum_2 = sum(int(numbers[i]) * (11 - i) for i in range(10))
    digit_2 = (sum_2 * 10) % 11
    if digit_2 == 10:
        digit_2 = 0

    return digit_2 == int(numbers[10])
