import pytest

from validabr.generators.cnh import generate_cnh
from validabr.parsers.cnh import CNHData, format_cnh, parse_cnh


class TestFormatCNH:
    def test_returns_raw_digits(self) -> None:
        cnh = generate_cnh()
        assert format_cnh(cnh) == cnh

    def test_strips_non_digits(self) -> None:
        cnh = generate_cnh()
        spaced = f"{cnh[:3]} {cnh[3:6]} {cnh[6:]}"
        assert format_cnh(spaced) == cnh

    def test_idempotent(self) -> None:
        cnh = generate_cnh()
        assert format_cnh(format_cnh(cnh)) == format_cnh(cnh)

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cnh()
            assert format_cnh(raw) == raw
            assert len(format_cnh(raw)) == 11

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cnh("1234567890")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cnh("123456789012")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cnh(12345678901)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cnh("")


class TestParseCNH:
    def test_returns_cnh_data(self) -> None:
        result = parse_cnh(generate_cnh())
        assert isinstance(result, CNHData)

    def test_fields_correct(self) -> None:
        cnh = generate_cnh()
        result = parse_cnh(cnh)
        assert result.registration == cnh[:9]
        assert result.check_digits == cnh[9:]

    def test_registration_length(self) -> None:
        result = parse_cnh(generate_cnh())
        assert len(result.registration) == 9

    def test_check_digits_length(self) -> None:
        result = parse_cnh(generate_cnh())
        assert len(result.check_digits) == 2

    def test_accepts_with_non_digits(self) -> None:
        cnh = generate_cnh()
        spaced = f"{cnh[:3]} {cnh[3:]}"
        result = parse_cnh(spaced)
        assert result.registration == cnh[:9]

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cnh()
            parsed = parse_cnh(raw)
            assert parsed.registration + parsed.check_digits == raw

    def test_is_immutable(self) -> None:
        result = parse_cnh(generate_cnh())
        with pytest.raises(AttributeError):
            result.registration = "000000000"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_cnh("1234567890")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_cnh("123456789012")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_cnh(12345678901)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_cnh("")
