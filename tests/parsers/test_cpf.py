import pytest

from pybrdoc.generators.cpf import generate_cpf
from pybrdoc.parsers.cpf import format_cpf


class TestFormatCPF:
    def test_formats_raw_digits(self) -> None:
        assert format_cpf("52998224725") == "529.982.247-25"

    def test_formats_already_formatted(self) -> None:
        assert format_cpf("529.982.247-25") == "529.982.247-25"

    def test_strips_extra_punctuation(self) -> None:
        assert format_cpf("529 982 247 25") == "529.982.247-25"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cpf()
            formatted = format_cpf(raw)
            assert formatted.count(".") == 2
            assert formatted.count("-") == 1
            assert len(formatted) == 14

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cpf("1234567890")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cpf("123456789012")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cpf(52998224725)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cpf("")

    def test_output_structure(self) -> None:
        result = format_cpf("11144477735")
        parts = result.split("-")
        assert len(parts) == 2
        assert len(parts[1]) == 2
        groups = parts[0].split(".")
        assert groups == ["111", "444", "777"]
