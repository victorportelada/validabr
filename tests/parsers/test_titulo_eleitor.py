import pytest

from pybrdoc.generators.titulo_eleitor import generate_titulo_eleitor
from pybrdoc.parsers.titulo_eleitor import format_titulo_eleitor


class TestFormatTituloEleitor:
    def test_formats_raw_digits(self) -> None:
        assert format_titulo_eleitor("000000000119") == "0000 0000 0119"

    def test_formats_with_spaces(self) -> None:
        assert format_titulo_eleitor("0000 0000 0119") == "0000 0000 0119"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_titulo_eleitor()
            formatted = format_titulo_eleitor(raw)
            assert formatted.count(" ") == 2
            assert len(formatted) == 14

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="12 digits"):
            format_titulo_eleitor("12345678901")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="12 digits"):
            format_titulo_eleitor("1234567890123")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_titulo_eleitor(123456789012)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="12 digits"):
            format_titulo_eleitor("")

    def test_output_structure(self) -> None:
        result = format_titulo_eleitor("000000000119")
        groups = result.split(" ")
        assert len(groups) == 3
        assert all(len(g) == 4 for g in groups)
