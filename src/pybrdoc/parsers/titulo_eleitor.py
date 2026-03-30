import re


def format_titulo_eleitor(titulo: str) -> str:
    """
    Formats a Título de Eleitor string to the canonical XXXX XXXX XXXX pattern
    (three space-separated groups of 4 digits).

    Accepts any string containing exactly 12 digits (punctuation is stripped).

    Raises:
        ValueError: if the input does not contain exactly 12 digits.
    """
    if not isinstance(titulo, str):
        raise ValueError(f"Expected str, got {type(titulo).__name__}")

    digits = re.sub(r"\D", "", titulo)

    if len(digits) != 12:
        raise ValueError(f"Título de Eleitor must have 12 digits, got {len(digits)}")

    return f"{digits[:4]} {digits[4:8]} {digits[8:]}"
