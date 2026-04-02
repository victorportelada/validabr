import pytest

from brdocuments.generators.titulo_eleitor import generate_titulo_eleitor
from brdocuments.parsers.titulo_eleitor import (
    TituloData,
    format_titulo_eleitor,
    parse_titulo_eleitor,
)


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


class TestParseTituloEleitor:
    # Título: SSSSSSSS EE V1 V2 → 12 digits
    # sequential = digits[:8], state_code = digits[8:10], check_digits = digits[10:]
    _RAW = "000000000119"

    def test_returns_titulo_data(self) -> None:
        result = parse_titulo_eleitor(self._RAW)
        assert isinstance(result, TituloData)

    def test_fields_from_raw_digits(self) -> None:
        result = parse_titulo_eleitor(self._RAW)
        assert result.sequential == "00000000"
        assert result.state_code == "01"
        assert result.check_digits == "19"

    def test_accepts_formatted_input(self) -> None:
        result = parse_titulo_eleitor("0000 0000 0119")
        assert result.sequential == "00000000"
        assert result.state_code == "01"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_titulo_eleitor()
            parsed = parse_titulo_eleitor(raw)
            assert len(parsed.sequential) == 8
            assert len(parsed.state_code) == 2
            assert len(parsed.check_digits) == 2
            assert parsed.sequential + parsed.state_code + parsed.check_digits == raw

    def test_is_immutable(self) -> None:
        result = parse_titulo_eleitor(self._RAW)
        with pytest.raises(AttributeError):
            result.sequential = "00000000"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="12 digits"):
            parse_titulo_eleitor("12345678901")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="12 digits"):
            parse_titulo_eleitor("1234567890123")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_titulo_eleitor(123456789012)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="12 digits"):
            parse_titulo_eleitor("")
