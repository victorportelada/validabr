import pytest

from brdocs.generators.cnj import generate_cnj
from brdocs.parsers.cnj import format_cnj


class TestFormatCNJ:
    def test_formats_raw_digits(self) -> None:
        result = format_cnj("00010034120238260000")
        assert result == "0001003-41.2023.8.26.0000"

    def test_formats_already_formatted(self) -> None:
        assert format_cnj("0001003-41.2023.8.26.0000") == "0001003-41.2023.8.26.0000"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cnj()
            formatted = format_cnj(raw)
            assert formatted.count("-") == 1
            assert formatted.count(".") == 4
            assert len(formatted) == 25

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="20 digits"):
            format_cnj("1234567890123456789")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="20 digits"):
            format_cnj("123456789012345678901")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cnj(12345678901234567890)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="20 digits"):
            format_cnj("")

    def test_output_structure(self) -> None:
        result = format_cnj("00010034120238260000")
        parts = result.split("-")
        assert len(parts[0]) == 7
        # after the hyphen: DD.AAAA.J.TT.OOOO → 5 dot-separated parts
        rest = parts[1].split(".")
        assert len(rest) == 5
        assert len(rest[0]) == 2  # DD
        assert len(rest[1]) == 4  # AAAA
        assert len(rest[2]) == 1  # J
        assert len(rest[3]) == 2  # TT
        assert len(rest[4]) == 4  # OOOO
