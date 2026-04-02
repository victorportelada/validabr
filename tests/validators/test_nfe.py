import re


def _calculate_nfe_check(key: str) -> int:
    digits = key[:43]
    weights = []
    for i in range(42, -1, -1):
        weights.append([2, 3, 4, 5, 6, 7, 8, 9][i % 8])
    total = sum(int(digits[i]) * weights[i] for i in range(43))
    remainder = total % 11
    if remainder <= 1:
        return 1
    return 11 - remainder


def _generate_nfe_base() -> str:
    import random

    while True:
        uf = f"{random.randint(11, 99):02d}"
        year = f"{random.randint(0, 9)}{random.randint(0, 9)}"
        month = f"{random.randint(1, 9)}{random.randint(0, 9)}"
        cnpj = "".join(str(random.randint(0, 9)) for _ in range(14))
        model = random.choice(["55", "57", "58"])
        series = f"{random.randint(1, 9):03d}"
        number = "".join(str(random.randint(0, 9)) for _ in range(9))
        emission = str(random.randint(1, 9))
        random_code = "".join(str(random.randint(0, 9)) for _ in range(8))
        base = uf + year + month + cnpj + model + series + number + emission + random_code
        check = _calculate_nfe_check(base)
        full = base + str(check)
        digits = re.sub(r"\D", "", full)
        if digits == digits[0] * 44:
            continue
        return digits


class TestNFEValidator:
    def test_valid_nfe_raw(self) -> None:
        key = _generate_nfe_base()
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe(key) is True

    def test_valid_nfe_formatted(self) -> None:
        key = _generate_nfe_base()
        formatted = " ".join([key[i * 5 : (i + 1) * 5] for i in range(8)] + [key[40:44]])
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe(formatted) is True

    def test_invalid_nfe_wrong_check_digit(self) -> None:
        key = _generate_nfe_base()
        wrong = key[:-1] + ("0" if key[-1] != "0" else "1")
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe(wrong) is False

    def test_invalid_nfe_all_zeros(self) -> None:
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe("0" * 44) is False

    def test_invalid_nfe_wrong_length_short(self) -> None:
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe("1" * 43) is False

    def test_invalid_nfe_wrong_length_long(self) -> None:
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe("1" * 45) is False

    def test_invalid_nfe_letters(self) -> None:
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe("A" * 44) is False

    def test_invalid_nfe_not_string(self) -> None:
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe(None) is False  # type: ignore
        assert is_valid_nfe(1111111111111111111111111111111111111111) is False  # type: ignore

    def test_empty_nfe(self) -> None:
        from brdocuments.validators.nfe import is_valid_nfe

        assert is_valid_nfe("") is False
