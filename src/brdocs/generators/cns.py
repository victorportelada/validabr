import random


def generate_cns(formatted: bool = False) -> str:
    """
    Generates a valid random Brazilian CNS (Cartão Nacional de Saúde).

    Generates definitive cards (starting with 1 or 2) by generating
    15 random digits and computing the final digit to satisfy the
    Modulo 11 constraint.

    Args:
        formatted: If True, returns in the XXX XXXX XXXX XXXX format.

    Returns:
        A 15-digit string representing a valid CNS.
    """
    while True:
        prefix = random.choice([1, 2])
        digits = [prefix] + [random.randint(0, 9) for _ in range(14)]
        total = sum(digits[i] * (15 - i) for i in range(15))
        if total % 11 == 0:
            raw = "".join(str(d) for d in digits)
            if formatted:
                return f"{raw[:3]} {raw[3:7]} {raw[7:11]} {raw[11:]}"
            return raw
