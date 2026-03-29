import random


def generate_cpf(formatted: bool = False) -> str:
    """
    Generates a valid random Brazilian CPF.

    Args:
        formatted: If True, returns in the NNN.NNN.NNN-NN format.

    Returns:
        A string representing a valid CPF.
    """
    while True:
        base = [random.randint(0, 9) for _ in range(9)]

        # Reject all-same-digit bases (would produce an invalid CPF)
        if len(set(base)) == 1:
            continue

        sum_1 = sum(d * (10 - i) for i, d in enumerate(base))
        d1 = (sum_1 * 10) % 11
        if d1 == 10:
            d1 = 0

        sum_2 = sum(d * (11 - i) for i, d in enumerate([*base, d1]))
        d2 = (sum_2 * 10) % 11
        if d2 == 10:
            d2 = 0

        digits = [*base, d1, d2]
        raw = "".join(str(d) for d in digits)

        if formatted:
            return f"{raw[:3]}.{raw[3:6]}.{raw[6:9]}-{raw[9:]}"
        return raw
