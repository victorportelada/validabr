import pytest

from brdocuments.generators.cpf import generate_cpf
from brdocuments.parsers.cpf import CPFData, format_cpf, parse_cpf


class TestFormatCPF:
    def test_formats_raw_digits(self) -> None:
        assert format_cpf("52998224725") == "529.982.247-25"

    def test_formats_already_formatted(self) -> None:
        assert format_cpf("529.982.247-25") == "529.982.247-25"

    def test_strips_extra_punctuation(self) -> None:
        assert format_cpf("529 982 247 25") == "529.982.247-25"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cpf()
            formatted = format_cpf(raw)
            assert formatted.count(".") == 2
            assert formatted.count("-") == 1
            assert len(formatted) == 14

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cpf("1234567890")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cpf("123456789012")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cpf(52998224725)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            format_cpf("")

    def test_output_structure(self) -> None:
        result = format_cpf("11144477735")
        parts = result.split("-")
        assert len(parts) == 2
        assert len(parts[1]) == 2
        groups = parts[0].split(".")
        assert groups == ["111", "444", "777"]


class TestParseCPF:
    def test_returns_cpf_data(self) -> None:
        result = parse_cpf("52998224725")
        assert isinstance(result, CPFData)

    def test_fields_from_raw_digits(self) -> None:
        result = parse_cpf("52998224725")
        assert result.root == "529982247"
        assert result.region_digit == "7"
        assert result.check_digits == "25"

    def test_accepts_formatted_input(self) -> None:
        result = parse_cpf("529.982.247-25")
        assert result.root == "529982247"
        assert result.check_digits == "25"

    def test_region_digit_is_ninth_digit(self) -> None:
        result = parse_cpf("52998224725")
        # region_digit is digits[8] — the 9th digit of the raw string
        assert result.region_digit == "52998224725"[8]

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cpf()
            parsed = parse_cpf(raw)
            assert len(parsed.root) == 9
            assert len(parsed.check_digits) == 2
            assert parsed.root + parsed.check_digits == raw

    def test_is_immutable(self) -> None:
        result = parse_cpf("52998224725")
        with pytest.raises(AttributeError):
            result.root = "000000000"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_cpf("1234567890")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_cpf("123456789012")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_cpf(52998224725)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="11 digits"):
            parse_cpf("")
