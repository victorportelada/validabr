import re


def format_cpf(cpf: str) -> str:
    """
    Formats a CPF string to the canonical NNN.NNN.NNN-NN pattern.

    Accepts any string containing exactly 11 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 11 digits.
    """
    if not isinstance(cpf, str):
        raise ValueError(f"Expected str, got {type(cpf).__name__}")

    digits = re.sub(r"\D", "", cpf)

    if len(digits) != 11:
        raise ValueError(f"CPF must have 11 digits, got {len(digits)}")

    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
