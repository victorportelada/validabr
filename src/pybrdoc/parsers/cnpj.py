import re


def format_cnpj(cnpj: str) -> str:
    """
    Formats a CNPJ string to the canonical NN.NNN.NNN/NNNN-NN pattern.

    Accepts any string containing exactly 14 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 14 digits.
    """
    if not isinstance(cnpj, str):
        raise ValueError(f"Expected str, got {type(cnpj).__name__}")

    digits = re.sub(r"\D", "", cnpj)

    if len(digits) != 14:
        raise ValueError(f"CNPJ must have 14 digits, got {len(digits)}")

    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
