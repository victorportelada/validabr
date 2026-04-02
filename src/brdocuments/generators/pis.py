import random


def generate_pis(formatted: bool = False) -> str:
    """
    Generates a valid random Brazilian PIS/PASEP/NIT.

    Args:
        formatted: If True, returns in the XXX.XXXXX.XX-X format.

    Returns:
        A string representing a valid PIS.
    """
    while True:
        base = [random.randint(0, 9) for _ in range(10)]

        if len(set(base)) == 1:
            continue

        weights = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_ = sum(d * weights[i] for i, d in enumerate(base))

        remainder = sum_ % 11
        check_digit = 0 if remainder < 2 else 11 - remainder

        digits = [*base, check_digit]
        raw = "".join(str(d) for d in digits)

        if formatted:
            return f"{raw[:3]}.{raw[3:8]}.{raw[8:10]}-{raw[10]}"
        return raw
