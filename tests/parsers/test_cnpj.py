import pytest

from pybrdoc.generators.cnpj import generate_cnpj
from pybrdoc.parsers.cnpj import format_cnpj


class TestFormatCNPJ:
    def test_formats_raw_digits(self) -> None:
        assert format_cnpj("11222333000181") == "11.222.333/0001-81"

    def test_formats_already_formatted(self) -> None:
        assert format_cnpj("11.222.333/0001-81") == "11.222.333/0001-81"

    def test_strips_extra_whitespace(self) -> None:
        assert format_cnpj("11 222 333 0001 81") == "11.222.333/0001-81"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cnpj()
            formatted = format_cnpj(raw)
            assert formatted.count(".") == 2
            assert formatted.count("/") == 1
            assert formatted.count("-") == 1
            assert len(formatted) == 18

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="14 digits"):
            format_cnpj("1234567890123")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="14 digits"):
            format_cnpj("123456789012345")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cnpj(11222333000181)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="14 digits"):
            format_cnpj("")

    def test_output_structure(self) -> None:
        result = format_cnpj("11222333000181")
        slash_parts = result.split("/")
        assert len(slash_parts) == 2
        left = slash_parts[0].split(".")
        assert len(left) == 3
        right = slash_parts[1].split("-")
        assert len(right) == 2
        assert len(right[0]) == 4
        assert len(right[1]) == 2
