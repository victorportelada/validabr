import random

_EXCLUDED_LETTERS = frozenset("IOUQF")
_ALFA_CHARS = list(
    "0123456789" + "".join(c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in _EXCLUDED_LETTERS)
)
_WEIGHTS_DV1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_WEIGHTS_DV2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def _char_value(c: str) -> int:
    return ord(c) - 48


def generate_cnpj(formatted: bool = False, alfa: bool = False) -> str:
    """
    Generates a valid random Brazilian CNPJ.

    Args:
        formatted: If True, returns in the NN.NNN.NNN/NNNN-NN format.
        alfa: If True, generates an alphanumeric CNPJ (IN RFB 2.229/2024).
              The first 8 characters may contain letters (A-Z excluding I,O,U,Q,F).

    Returns:
        A string representing a valid CNPJ.
    """
    if alfa:
        base = [random.choice(_ALFA_CHARS) for _ in range(8)] + list("0001")
    else:
        base = [str(random.randint(0, 9)) for _ in range(8)] + list("0001")

    r1 = sum(_char_value(c) * w for c, w in zip(base, _WEIGHTS_DV1, strict=True)) % 11
    d1 = 0 if r1 < 2 else 11 - r1

    r2 = sum(_char_value(c) * w for c, w in zip([*base, str(d1)], _WEIGHTS_DV2, strict=True)) % 11
    d2 = 0 if r2 < 2 else 11 - r2

    raw = "".join(base) + str(d1) + str(d2)

    if formatted:
        return f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:12]}-{raw[12:]}"
    return raw
