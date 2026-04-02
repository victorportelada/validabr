import re


def is_valid_cep(cep: str) -> bool:
    """
    Validates a Brazilian CEP (Código de Endereçamento Postal).

    Args:
        cep (str): The CEP string to validate. Can contain the hyphen.

    Returns:
        bool: True if the CEP is valid, False otherwise.
    """
    if not isinstance(cep, str):
        return False

    numbers = re.sub(r"\D", "", cep)

    if len(numbers) != 8:
        return False

    return numbers != numbers[0] * 8
