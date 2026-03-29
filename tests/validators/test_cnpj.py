import pytest

from pybrdoc.generators.cnpj import generate_cnpj
from pybrdoc.validators.cnpj import is_valid_cnpj


class TestCNPJValidator:
    def test_valid_cnpj_unformatted(self) -> None:
        assert is_valid_cnpj("11222333000181") is True
        assert is_valid_cnpj("00000000000191") is True  # Banco do Brasil
        assert is_valid_cnpj("60746948000112") is True  # Banco Bradesco

    def test_valid_cnpj_formatted(self) -> None:
        assert is_valid_cnpj("11.222.333/0001-81") is True
        assert is_valid_cnpj("00.000.000/0001-91") is True
        assert is_valid_cnpj("01.900.000/0001-00") is True

    def test_invalid_cnpj_wrong_first_check(self) -> None:
        # Change digit at position 12
        assert is_valid_cnpj("11222333000191") is False

    def test_invalid_cnpj_wrong_second_check(self) -> None:
        # Change digit at position 13
        assert is_valid_cnpj("11222333000182") is False

    def test_invalid_cnpj_type(self) -> None:
        assert is_valid_cnpj(42) is False  # type: ignore
        assert is_valid_cnpj(None) is False  # type: ignore

    def test_invalid_cnpj_bad_length(self) -> None:
        assert is_valid_cnpj("1122233300018") is False  # 13 digits
        assert is_valid_cnpj("11.222.333/0001-8") is False
        assert is_valid_cnpj("112223330001819") is False  # 15 digits

    def test_invalid_cnpj_identical_digits(self) -> None:
        for d in "0123456789":
            assert is_valid_cnpj(d * 14) is False

    def test_invalid_cnpj_invalid_characters(self) -> None:
        assert is_valid_cnpj("11A222333000181") is False
        assert is_valid_cnpj("!@#$%¨&*()_+{}") is False

    def test_empty_cnpj(self) -> None:
        assert is_valid_cnpj("") is False

    @pytest.mark.parametrize("_", range(10))
    def test_round_trip_generate_validate(self, _: int) -> None:
        cnpj = generate_cnpj()
        assert is_valid_cnpj(cnpj) is True

    def test_formatted_cnpj_validates(self) -> None:
        for _ in range(5):
            assert is_valid_cnpj(generate_cnpj(formatted=True)) is True
