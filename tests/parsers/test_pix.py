import pytest

from validabr.parsers.pix import (
    PixEmailData,
    PixEVPData,
    PixPhoneData,
    format_pix,
    parse_pix,
)


class TestFormatPix:
    def test_format_cpf(self) -> None:
        assert format_pix("52998224725") == "529.982.247-25"

    def test_format_cpf_formatted_input(self) -> None:
        assert format_pix("529.982.247-25") == "529.982.247-25"

    def test_format_cnpj(self) -> None:
        assert format_pix("00000000000191") == "00.000.000/0001-91"

    def test_format_cnpj_formatted_input(self) -> None:
        assert format_pix("00.000.000/0001-91") == "00.000.000/0001-91"

    def test_format_phone_9_digits(self) -> None:
        assert format_pix("+5511999999999") == "+55 (11) 99999-9999"

    def test_format_phone_8_digits(self) -> None:
        assert format_pix("+551132165432") == "+55 (11) 3216-5432"

    def test_format_phone_without_plus(self) -> None:
        assert format_pix("+5511999999999") == "+55 (11) 99999-9999"

    def test_format_email(self) -> None:
        assert format_pix("Test@EXAMPLE.COM") == "test@example.com"

    def test_format_email_unchanged_lowercase(self) -> None:
        assert format_pix("lowercase@example.com") == "lowercase@example.com"

    def test_format_evp(self) -> None:
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        assert format_pix(uuid) == uuid.lower()

    def test_format_evp_uppercase(self) -> None:
        uuid = "550E8400-E29B-41D4-A716-446655440000"
        assert format_pix(uuid) == uuid.lower()

    def test_format_raises_on_invalid_key(self) -> None:
        with pytest.raises(ValueError, match="Invalid PIX key"):
            format_pix("not-a-valid-key")

    def test_format_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="Invalid PIX key"):
            format_pix("")

    def test_format_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Invalid PIX key"):
            format_pix(12345678901)  # type: ignore


class TestParsePix:
    def test_parse_cpf_returns_cpf_data(self) -> None:
        result = parse_pix("52998224725")
        assert isinstance(result.root, str)
        assert isinstance(result.region_digit, str)
        assert isinstance(result.check_digits, str)

    def test_parse_cpf_fields(self) -> None:
        result = parse_pix("52998224725")
        assert result.root == "529982247"
        assert result.region_digit == "7"
        assert result.check_digits == "25"

    def test_parse_cpf_accepts_formatted(self) -> None:
        result = parse_pix("529.982.247-25")
        assert result.root == "529982247"
        assert result.check_digits == "25"

    def test_parse_cnpj_returns_cnpj_data(self) -> None:
        result = parse_pix("00000000000191")
        assert isinstance(result.root, str)
        assert isinstance(result.branch, str)
        assert isinstance(result.check_digits, str)

    def test_parse_cnpj_fields(self) -> None:
        result = parse_pix("00000000000191")
        assert result.root == "00000000"
        assert result.branch == "0001"
        assert result.check_digits == "91"
        assert result.is_matriz is True

    def test_parse_cnpj_accepts_formatted(self) -> None:
        result = parse_pix("00.000.000/0001-91")
        assert result.root == "00000000"
        assert result.branch == "0001"

    def test_parse_phone_9_digits(self) -> None:
        result = parse_pix("+5511999999999")
        assert isinstance(result, PixPhoneData)
        assert result.country_code == "55"
        assert result.area_code == "11"
        assert result.number == "999999999"
        assert result.raw == "+5511999999999"

    def test_parse_phone_8_digits(self) -> None:
        result = parse_pix("+551132165432")
        assert isinstance(result, PixPhoneData)
        assert result.country_code == "55"
        assert result.area_code == "11"
        assert result.number == "32165432"
        assert result.raw == "+551132165432"

    def test_parse_email(self) -> None:
        result = parse_pix("Test@EXAMPLE.COM")
        assert isinstance(result, PixEmailData)
        assert result.local == "test"
        assert result.domain == "example.com"
        assert result.normalized == "test@example.com"

    def test_parse_email_lowercase_unchanged(self) -> None:
        result = parse_pix("lowercase@example.com")
        assert result.local == "lowercase"
        assert result.domain == "example.com"
        assert result.normalized == "lowercase@example.com"

    def test_parse_evp(self) -> None:
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        result = parse_pix(uuid)
        assert isinstance(result, PixEVPData)
        assert result.uuid == uuid.lower()

    def test_parse_evp_uppercase(self) -> None:
        uuid = "550E8400-E29B-41D4-A716-446655440000"
        result = parse_pix(uuid)
        assert isinstance(result, PixEVPData)
        assert result.uuid == uuid.lower()

    def test_parse_raises_on_invalid_key(self) -> None:
        with pytest.raises(ValueError, match="Invalid PIX key"):
            parse_pix("not-a-valid-key")

    def test_parse_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="Invalid PIX key"):
            parse_pix("")

    def test_parse_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Invalid PIX key"):
            parse_pix(12345678901)  # type: ignore

    def test_round_trip_cpf(self) -> None:
        raw = "52998224725"
        formatted = format_pix(raw)
        parsed = parse_pix(formatted)
        assert parsed.root + parsed.check_digits == raw

    def test_round_trip_cnpj(self) -> None:
        raw = "00000000000191"
        formatted = format_pix(raw)
        parsed = parse_pix(formatted)
        assert parsed.root + parsed.branch + parsed.check_digits == raw

    def test_round_trip_phone(self) -> None:
        raw = "+5511999999999"
        formatted = format_pix(raw)
        parsed = parse_pix(formatted)
        assert parsed.raw == raw

    def test_round_trip_email(self) -> None:
        raw = "Test@EXAMPLE.COM"
        formatted = format_pix(raw)
        parsed = parse_pix(formatted)
        assert parsed.normalized == formatted

    def test_round_trip_evp(self) -> None:
        raw = "550e8400-e29b-41d4-a716-446655440000"
        formatted = format_pix(raw)
        parsed = parse_pix(formatted)
        assert parsed.uuid == formatted
