import pytest

from validabr.generators.cns import generate_cns
from validabr.parsers.cns import CNSData, format_cns, parse_cns


class TestFormatCNS:
    def test_formats_raw_digits(self) -> None:
        raw = generate_cns()
        fmt = format_cns(raw)
        assert fmt.count(" ") == 3

    def test_formats_already_formatted(self) -> None:
        raw = generate_cns()
        fmt1 = format_cns(raw)
        fmt2 = format_cns(fmt1)
        assert fmt1 == fmt2

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cns()
            formatted = format_cns(raw)
            assert formatted.count(" ") == 3
            assert len(formatted) == 18

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="15 digits"):
            format_cns("1" * 14)

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="15 digits"):
            format_cns("1" * 16)

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cns(111111111111111)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="15 digits"):
            format_cns("")


class TestParseCNS:
    def test_returns_cns_data(self) -> None:
        result = parse_cns(generate_cns())
        assert isinstance(result, CNSData)

    def test_fields_from_raw_digits(self) -> None:
        raw = "167441640030005"
        result = parse_cns(raw)
        assert result.digits == raw
        assert result.card_type == "definitive"

    def test_accepts_formatted_input(self) -> None:
        raw = "167 4416 4003 0005"
        result = parse_cns(raw)
        assert result.digits == "167441640030005"

    def test_definitive_card_type(self) -> None:
        raw = generate_cns()
        result = parse_cns(raw)
        assert result.card_type == "definitive"

    def test_is_immutable(self) -> None:
        result = parse_cns(generate_cns())
        with pytest.raises(AttributeError):
            result.digits = "0" * 15

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="15 digits"):
            parse_cns("1" * 14)

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="15 digits"):
            parse_cns("1" * 16)

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_cns(111111111111111)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="15 digits"):
            parse_cns("")

    def test_temporary_card_type(self) -> None:
        result = parse_cns("729141777631706")
        assert result.card_type == "temporary"

    def test_unknown_first_digit_falls_back_to_definitive(self) -> None:
        # First digit 3 is not in (1,2) or (7,8,9) — hits the else fallback
        result = parse_cns("3" * 15)
        assert result.card_type == "definitive"
