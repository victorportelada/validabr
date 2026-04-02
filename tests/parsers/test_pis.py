import pytest

from validabr.generators.pis import generate_pis
from validabr.parsers.pis import PISData, format_pis, parse_pis


class TestFormatPIS:
    def test_formats_raw_digits(self) -> None:
        raw = generate_pis()
        fmt = format_pis(raw)
        assert fmt.count(".") == 2
        assert fmt.count("-") == 1

    def test_formats_already_formatted(self) -> None:
        raw = generate_pis()
        fmt1 = format_pis(raw)
        fmt2 = format_pis(fmt1)
        assert fmt1 == fmt2

    def test_strips_extra_punctuation(self) -> None:
        raw = generate_pis()
        digits = raw[:3] + " " + raw[3:8] + "  " + raw[8:10] + " - " + raw[10]
        result = format_pis(digits)
        assert result.count(".") == 2
        assert result.count("-") == 1

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_pis()
            formatted = format_pis(raw)
            assert formatted.count(".") == 2
            assert formatted.count("-") == 1
            assert len(formatted) == 14

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_pis("1201256889")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_pis("120125688944")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_pis(12012568894)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_pis("")

    def test_output_structure(self) -> None:
        raw = generate_pis()
        result = format_pis(raw)
        assert len(result) == 14
        assert result[3] == "."
        assert result[9] == "."
        assert result[12] == "-"
        assert result[:3] == raw[:3]
        assert result[4:9] == raw[3:8]
        assert result[10:12] == raw[8:10]
        assert result[13] == raw[10]


class TestParsePIS:
    def test_returns_pis_data(self) -> None:
        result = parse_pis(generate_pis())
        assert isinstance(result, PISData)

    def test_fields_from_raw_digits(self) -> None:
        raw = "56875023741"
        result = parse_pis(raw)
        assert result.base == "5687502374"
        assert result.check_digit == "1"

    def test_accepts_formatted_input(self) -> None:
        raw = "568.75023.74-1"
        result = parse_pis(raw)
        assert result.base == "5687502374"
        assert result.check_digit == "1"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_pis()
            parsed = parse_pis(raw)
            assert len(parsed.base) == 10
            assert len(parsed.check_digit) == 1
            assert parsed.base + parsed.check_digit == raw

    def test_is_immutable(self) -> None:
        result = parse_pis(generate_pis())
        with pytest.raises(AttributeError):
            result.base = "0000000000"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_pis("1201256889")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_pis("120125688944")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_pis(12012568894)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_pis("")
