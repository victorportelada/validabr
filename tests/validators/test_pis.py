from brdocuments.generators.pis import generate_pis
from brdocuments.validators.pis import is_valid_pis


class TestPISValidator:
    def test_valid_pis_formatted(self) -> None:
        raw = generate_pis()
        fmt = f"{raw[:3]}.{raw[3:8]}.{raw[8:10]}-{raw[10]}"
        assert is_valid_pis(fmt) is True

    def test_valid_pis_raw(self) -> None:
        raw = generate_pis()
        assert is_valid_pis(raw) is True

    def test_valid_pis_with_spaces(self) -> None:
        raw = generate_pis()
        spaced = f"{raw[:3]} {raw[3:8]} {raw[8:10]} {raw[10]}"
        assert is_valid_pis(spaced) is True

    def test_generated_is_valid(self) -> None:
        for _ in range(10):
            assert is_valid_pis(generate_pis()) is True

    def test_invalid_pis_wrong_check_digit(self) -> None:
        raw = generate_pis()
        wrong = raw[:-1] + ("0" if raw[-1] != "0" else "1")
        assert is_valid_pis(wrong) is False

    def test_invalid_pis_all_zeros(self) -> None:
        assert is_valid_pis("00000000000") is False

    def test_invalid_pis_all_ones(self) -> None:
        assert is_valid_pis("11111111111") is False

    def test_invalid_pis_wrong_length_short(self) -> None:
        assert is_valid_pis("1201256889") is False

    def test_invalid_pis_wrong_length_long(self) -> None:
        assert is_valid_pis("120125688944") is False

    def test_invalid_pis_letters(self) -> None:
        assert is_valid_pis("ABCDEFGHIJK") is False

    def test_invalid_pis_not_string(self) -> None:
        assert is_valid_pis(None) is False  # type: ignore
        assert is_valid_pis(12012568894) is False  # type: ignore

    def test_empty_pis(self) -> None:
        assert is_valid_pis("") is False

    def test_idempotent_format(self) -> None:
        raw = generate_pis()
        fmt = f"{raw[:3]}.{raw[3:8]}.{raw[8:10]}-{raw[10]}"
        assert is_valid_pis(fmt) is True
