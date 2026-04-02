import pytest

from brdocs.generators.cpf import generate_cpf
from brdocs.validators.cpf import is_valid_cpf


class TestCPFValidator:
    def test_valid_cpf_without_punctuation(self) -> None:
        assert is_valid_cpf("52998224725") is True

    def test_valid_cpf_with_punctuation(self) -> None:
        assert is_valid_cpf("529.982.247-25") is True

    def test_valid_cpf_other_known_values(self) -> None:
        # Additional known-valid CPFs
        assert is_valid_cpf("11144477735") is True
        assert is_valid_cpf("111.444.777-35") is True

    def test_invalid_cpf_wrong_first_check(self) -> None:
        # Flip the first check digit (position 9)
        assert is_valid_cpf("52998224625") is False

    def test_invalid_cpf_wrong_second_check(self) -> None:
        # Flip the second check digit (position 10)
        assert is_valid_cpf("52998224726") is False

    def test_invalid_cpf_all_same_digits(self) -> None:
        for d in "0123456789":
            assert is_valid_cpf(d * 11) is False

    def test_invalid_cpf_wrong_length_short(self) -> None:
        assert is_valid_cpf("123456789") is False
        assert is_valid_cpf("1234567890") is False

    def test_invalid_cpf_wrong_length_long(self) -> None:
        assert is_valid_cpf("123456789012") is False

    def test_invalid_cpf_letters(self) -> None:
        assert is_valid_cpf("abc.def.ghi-jk") is False

    def test_empty_cpf(self) -> None:
        assert is_valid_cpf("") is False

    def test_invalid_cpf_none(self) -> None:
        assert is_valid_cpf(None) is False  # type: ignore

    def test_invalid_cpf_int(self) -> None:
        assert is_valid_cpf(52998224725) is False  # type: ignore

    @pytest.mark.parametrize("_", range(10))
    def test_round_trip_generate_validate(self, _: int) -> None:
        cpf = generate_cpf()
        assert is_valid_cpf(cpf) is True

    def test_formatted_cpf_validates(self) -> None:
        for _ in range(5):
            assert is_valid_cpf(generate_cpf(formatted=True)) is True
