from brdocuments.generators.cns import generate_cns
from brdocuments.validators.cns import is_valid_cns


class TestCNSValidator:
    def test_valid_cns_formatted(self) -> None:
        raw = generate_cns()
        fmt = f"{raw[:3]} {raw[3:7]} {raw[7:11]} {raw[11:]}"
        assert is_valid_cns(fmt) is True

    def test_valid_cns_raw(self) -> None:
        raw = generate_cns()
        assert is_valid_cns(raw) is True

    def test_generated_is_valid(self) -> None:
        for _ in range(10):
            assert is_valid_cns(generate_cns()) is True

    def test_invalid_cns_wrong_check_digit(self) -> None:
        raw = generate_cns()
        wrong = raw[:-1] + ("0" if raw[-1] != "0" else "1")
        assert is_valid_cns(wrong) is False

    def test_invalid_cns_all_zeros(self) -> None:
        assert is_valid_cns("0" * 15) is False

    def test_invalid_cns_all_ones(self) -> None:
        assert is_valid_cns("1" * 15) is False

    def test_invalid_cns_wrong_length_short(self) -> None:
        assert is_valid_cns("1" * 14) is False

    def test_invalid_cns_wrong_length_long(self) -> None:
        assert is_valid_cns("1" * 16) is False

    def test_invalid_cns_letters(self) -> None:
        assert is_valid_cns("A" * 15) is False

    def test_invalid_cns_not_string(self) -> None:
        assert is_valid_cns(None) is False  # type: ignore
        assert is_valid_cns(111111111111111) is False  # type: ignore

    def test_empty_cns(self) -> None:
        assert is_valid_cns("") is False

    def test_definitive_card(self) -> None:
        cns = generate_cns()
        assert cns[0] in "12"
        assert is_valid_cns(cns) is True

    def test_temporary_card_valid(self) -> None:
        # Handcrafted valid temporary CNS (starts with 7)
        assert is_valid_cns("729141777631706") is True

    def test_temporary_card_invalid_check(self) -> None:
        # Tamper a digit used in the pis_sum (index 1, weight 14)
        base = "729141777631706"
        wrong = base[0] + ("0" if base[1] != "0" else "1") + base[2:]
        assert is_valid_cns(wrong) is False

    def test_invalid_first_digit_returns_false(self) -> None:
        # First digit 3 is not in (1, 2, 7, 8, 9) — hits the final return False
        # Must be non-uniform to bypass the all-same-digits check
        assert is_valid_cns("312345678901234") is False
        assert is_valid_cns("412345678901234") is False
