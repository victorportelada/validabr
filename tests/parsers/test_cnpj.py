import pytest

from validabr.generators.cnpj import generate_cnpj
from validabr.parsers.cnpj import CNPJData, format_cnpj, parse_cnpj


class TestFormatCNPJ:
    def test_formats_raw_digits(self) -> None:
        assert format_cnpj("11222333000181") == "11.222.333/0001-81"

    def test_formats_already_formatted(self) -> None:
        assert format_cnpj("11.222.333/0001-81") == "11.222.333/0001-81"

    def test_strips_extra_whitespace(self) -> None:
        assert format_cnpj("11 222 333 0001 81") == "11.222.333/0001-81"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cnpj()
            formatted = format_cnpj(raw)
            assert formatted.count(".") == 2
            assert formatted.count("/") == 1
            assert formatted.count("-") == 1
            assert len(formatted) == 18

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="14 characters"):
            format_cnpj("1234567890123")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="14 characters"):
            format_cnpj("123456789012345")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_cnpj(11222333000181)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="14 characters"):
            format_cnpj("")

    def test_output_structure(self) -> None:
        result = format_cnpj("11222333000181")
        slash_parts = result.split("/")
        assert len(slash_parts) == 2
        left = slash_parts[0].split(".")
        assert len(left) == 3
        right = slash_parts[1].split("-")
        assert len(right) == 2
        assert len(right[0]) == 4
        assert len(right[1]) == 2


class TestParseCNPJ:
    def test_returns_cnpj_data(self) -> None:
        result = parse_cnpj("11222333000181")
        assert isinstance(result, CNPJData)

    def test_fields_from_raw_digits(self) -> None:
        result = parse_cnpj("11222333000181")
        assert result.root == "11222333"
        assert result.branch == "0001"
        assert result.check_digits == "81"

    def test_accepts_formatted_input(self) -> None:
        result = parse_cnpj("11.222.333/0001-81")
        assert result.root == "11222333"
        assert result.branch == "0001"
        assert result.check_digits == "81"

    def test_is_matriz_true_for_0001(self) -> None:
        result = parse_cnpj("11222333000181")
        assert result.is_matriz is True

    def test_is_matriz_false_for_branch(self) -> None:
        # Generate a branch CNPJ by using branch "0002"
        result = parse_cnpj("11222333000271")
        assert result.is_matriz is False

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_cnpj()
            parsed = parse_cnpj(raw)
            assert len(parsed.root) == 8
            assert len(parsed.branch) == 4
            assert len(parsed.check_digits) == 2
            assert parsed.root + parsed.branch + parsed.check_digits == raw

    def test_is_immutable(self) -> None:
        result = parse_cnpj("11222333000181")
        with pytest.raises(AttributeError):
            result.root = "00000000"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        with pytest.raises(ValueError, match="14 characters"):
            parse_cnpj("1234567890123")

    def test_raises_on_long_input(self) -> None:
        with pytest.raises(ValueError, match="14 characters"):
            parse_cnpj("123456789012345")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_cnpj(11222333000181)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match="14 characters"):
            parse_cnpj("")


class TestCNPJAlfanumericoParser:
    VALID_ALFA = "12ABC34501DE35"
    VALID_ALFA_FORMATTED = "12.ABC.345/01DE-35"

    def test_parse_alfa_unformatted(self) -> None:
        result = parse_cnpj(self.VALID_ALFA)
        assert result.root == "12ABC345"
        assert result.branch == "01DE"
        assert result.check_digits == "35"

    def test_parse_alfa_formatted(self) -> None:
        result = parse_cnpj(self.VALID_ALFA_FORMATTED)
        assert result.root == "12ABC345"
        assert result.branch == "01DE"
        assert result.check_digits == "35"

    def test_format_alfa_unformatted(self) -> None:
        assert format_cnpj(self.VALID_ALFA) == self.VALID_ALFA_FORMATTED

    def test_format_alfa_already_formatted(self) -> None:
        assert format_cnpj(self.VALID_ALFA_FORMATTED) == self.VALID_ALFA_FORMATTED

    def test_format_alfa_lowercase_normalized(self) -> None:
        assert format_cnpj("12abc34501de35") == self.VALID_ALFA_FORMATTED

    def test_round_trip_generate_parse_alfa(self) -> None:
        from validabr.generators.cnpj import generate_cnpj

        for _ in range(10):
            raw = generate_cnpj(alfa=True)
            parsed = parse_cnpj(raw)
            assert len(parsed.root) == 8
            assert len(parsed.branch) == 4
            assert len(parsed.check_digits) == 2
            assert parsed.root + parsed.branch + parsed.check_digits == raw.upper()
