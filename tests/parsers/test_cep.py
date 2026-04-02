import pytest

from brdocuments.generators.cep import generate_cep
from brdocuments.parsers.cep import CEPData, format_cep, parse_cep


class TestFormatCEP:
    def test_formats_raw_digits(self) -> None:
        assert format_cep("01310000") == "01310-000"

    def test_formats_already_formatted(self) -> None:
        assert format_cep("01310-000") == "01310-000"

    def test_strips_extra_punctuation(self) -> None:
        assert format_cep("013 10 000") == "01310-000"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cep()
            formatted = format_cep(raw)
            assert formatted.count("-") == 1
            assert len(formatted) == 9

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="8 digits"):
            format_cep("0131000")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="8 digits"):
            format_cep("013100000")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cep(1310000)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="8 digits"):
            format_cep("")

    def test_output_structure(self) -> None:
        result = format_cep("01310000")
        parts = result.split("-")
        assert len(parts) == 2
        assert len(parts[0]) == 5
        assert len(parts[1]) == 3


class TestParseCEP:
    def test_returns_cep_data(self) -> None:
        result = parse_cep("01310000")
        assert isinstance(result, CEPData)

    def test_fields_from_raw_digits(self) -> None:
        result = parse_cep("01310000")
        assert result.region == "01310"
        assert result.suffix == "000"

    def test_accepts_formatted_input(self) -> None:
        result = parse_cep("01310-000")
        assert result.region == "01310"
        assert result.suffix == "000"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cep()
            parsed = parse_cep(raw)
            assert len(parsed.region) == 5
            assert len(parsed.suffix) == 3
            assert parsed.region + parsed.suffix == raw

    def test_is_immutable(self) -> None:
        result = parse_cep("01310000")
        with pytest.raises(AttributeError):
            result.region = "00000"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="8 digits"):
            parse_cep("0131000")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="8 digits"):
            parse_cep("013100000")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_cep(1310000)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="8 digits"):
            parse_cep("")
