import random


def generate_cep(formatted: bool = False) -> str:
    """
    Generates a valid random Brazilian CEP.

    Args:
        formatted: If True, returns in the XXXXX-XXX format.

    Returns:
        A string representing a valid CEP.
    """
    while True:
        digits = [random.randint(0, 9) for _ in range(8)]

        if len(set(digits)) == 1:
            continue

        raw = "".join(str(d) for d in digits)

        if formatted:
            return f"{raw[:5]}-{raw[5:]}"
        return raw
