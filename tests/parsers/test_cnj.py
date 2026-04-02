import pytest

from brdocuments.generators.cnj import generate_cnj
from brdocuments.parsers.cnj import CNJData, format_cnj, parse_cnj


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


class TestParseCNJ:
    # CNJ: NNNNNNN-DD.AAAA.J.TT.OOOO → 20 digits
    # digits[0:7]   = sequence
    # digits[7:9]   = check_digits (DD)
    # digits[9:13]  = year
    # digits[13:14] = justice_segment
    # digits[14:16] = tribunal
    # digits[16:20] = origin_unit
    _RAW = "00010034120238260000"

    def test_returns_cnj_data(self) -> None:
        result = parse_cnj(self._RAW)
        assert isinstance(result, CNJData)

    def test_fields_from_raw_digits(self) -> None:
        result = parse_cnj(self._RAW)
        assert result.sequence == "0001003"
        assert result.check_digits == "41"
        assert result.year == "2023"
        assert result.justice_segment == "8"
        assert result.tribunal == "26"
        assert result.origin_unit == "0000"

    def test_accepts_formatted_input(self) -> None:
        result = parse_cnj("0001003-41.2023.8.26.0000")
        assert result.sequence == "0001003"
        assert result.year == "2023"

    def test_round_trip_with_generator(self) -> None:
        import re

        for _ in range(10):
            raw = generate_cnj()
            parsed = parse_cnj(raw)
            assert len(parsed.sequence) == 7
            assert len(parsed.check_digits) == 2
            assert len(parsed.year) == 4
            assert len(parsed.justice_segment) == 1
            assert len(parsed.tribunal) == 2
            assert len(parsed.origin_unit) == 4
            reconstructed = (
                parsed.sequence
                + parsed.check_digits
                + parsed.year
                + parsed.justice_segment
                + parsed.tribunal
                + parsed.origin_unit
            )
            assert reconstructed == re.sub(r"\D", "", raw)

    def test_is_immutable(self) -> None:
        result = parse_cnj(self._RAW)
        with pytest.raises(AttributeError):
            result.sequence = "0000000"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="20 digits"):
            parse_cnj("1234567890123456789")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="20 digits"):
            parse_cnj("123456789012345678901")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_cnj(12345678901234567890)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="20 digits"):
            parse_cnj("")
