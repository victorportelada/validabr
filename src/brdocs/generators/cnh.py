import random


def generate_cnh() -> str:
    """
    Generates a valid random Brazilian CNH (Carteira Nacional de Habilitação).

    Returns:
        An 11-digit string representing a valid CNH (raw digits, no separators).
    """
    while True:
        base = [random.randint(0, 9) for _ in range(9)]

        if len(set(base)) == 1:
            continue

        # First pass — descending weights [9, 8, 7, 6, 5, 4, 3, 2, 1]
        sum1 = sum(base[i] * (9 - i) for i in range(9))
        remainder1 = sum1 % 11
        if remainder1 >= 10:
            first_digit = 0
            dsc = 2
        else:
            first_digit = remainder1
            dsc = 0

        # Second pass — ascending weights [1, 2, 3, 4, 5, 6, 7, 8, 9] + DSC
        sum2 = dsc + sum(base[i] * (i + 1) for i in range(9))
        remainder2 = sum2 % 11
        second_digit = 0 if remainder2 >= 10 else remainder2

        return "".join(str(d) for d in [*base, first_digit, second_digit])
