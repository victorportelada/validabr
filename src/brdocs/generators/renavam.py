import random

_WEIGHTS = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def generate_renavam(formatted: bool = False) -> str:
    """
    Generates a valid random Brazilian RENAVAM (11 digits).

    Args:
        formatted: If True, returns with a hyphen before the check digit
                   (e.g. "0012345678-9").

    Returns:
        A valid RENAVAM string.
    """
    while True:
        base = [random.randint(0, 9) for _ in range(10)]
        total = sum(d * w for d, w in zip(base, _WEIGHTS, strict=False))
        remainder = total % 11

        if remainder == 1:
            # No valid check digit for this base — regenerate
            continue

        check = 0 if remainder == 0 else 11 - remainder
        digits = "".join(str(d) for d in base) + str(check)

        if formatted:
            return f"{digits[:10]}-{digits[10]}"
        return digits
