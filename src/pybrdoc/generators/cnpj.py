import random


def generate_cnpj(formatted: bool = False) -> str:
    """
    Generates a valid random Brazilian CNPJ.

    Args:
        formatted: If True, returns in the NN.NNN.NNN/NNNN-NN format.

    Returns:
        A string representing a valid CNPJ.
    """
    # First 8 digits are the company base; last 4 are the branch (0001 = headquarters)
    base = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]

    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    r1 = sum(d * w for d, w in zip(base, weights_1, strict=False)) % 11
    d1 = 0 if r1 < 2 else 11 - r1

    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    r2 = sum(d * w for d, w in zip([*base, d1], weights_2, strict=False)) % 11
    d2 = 0 if r2 < 2 else 11 - r2

    digits = [*base, d1, d2]
    raw = "".join(str(d) for d in digits)

    if formatted:
        return f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:12]}-{raw[12:]}"
    return raw
