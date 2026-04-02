import re

import pytest


def _calculate_nfe_check(key: str) -> int:
    digits = key[:43]
    weights = []
    for i in range(42, -1, -1):
        weights.append([2, 3, 4, 5, 6, 7, 8, 9][i % 8])
    total = sum(int(digits[i]) * weights[i] for i in range(43))
    remainder = total % 11
    if remainder <= 1:
        return 1
    return 11 - remainder


def _generate_nfe() -> str:
    import random

    while True:
        uf = f"{random.randint(11, 99):02d}"
        year = f"{random.randint(0, 9)}{random.randint(0, 9)}"
        month = f"{random.randint(1, 9)}{random.randint(0, 9)}"
        cnpj = "".join(str(random.randint(0, 9)) for _ in range(14))
        model = random.choice(["55", "57", "58"])
        series = f"{random.randint(1, 9):03d}"
        number = "".join(str(random.randint(0, 9)) for _ in range(9))
        emission = str(random.randint(1, 9))
        random_code = "".join(str(random.randint(0, 9)) for _ in range(8))
        base = uf + year + month + cnpj + model + series + number + emission + random_code
        check = _calculate_nfe_check(base)
        full = base + str(check)
        digits = re.sub(r"\D", "", full)
        if digits == digits[0] * 44:
            continue
        return digits


class TestParseNFE:
    def test_returns_nfe_data(self) -> None:
        from validabr.parsers.nfe import NFEData, parse_nfe

        result = parse_nfe(_generate_nfe())
        assert isinstance(result, NFEData)

    def test_fields_from_valid_key(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        key = _generate_nfe()
        result = parse_nfe(key)
        assert len(result.uf_code) == 2
        assert len(result.year_month) == 4
        assert len(result.cnpj) == 14
        assert len(result.model) == 2
        assert len(result.series) == 3
        assert len(result.number) == 9
        assert len(result.emission_type) == 1
        assert len(result.random_code) == 8
        assert len(result.check_digit) == 1

    def test_accepts_formatted_input(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        raw = _generate_nfe()
        formatted = " ".join([raw[i * 5 : (i + 1) * 5] for i in range(8)] + [raw[40:44]])
        result = parse_nfe(formatted)
        assert result.uf_code == raw[:2]
        assert result.check_digit == raw[43]

    def test_round_trip(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        key = _generate_nfe()
        result = parse_nfe(key)
        reconstructed = (
            result.uf_code
            + result.year_month
            + result.cnpj
            + result.model
            + result.series
            + result.number
            + result.emission_type
            + result.random_code
            + result.check_digit
        )
        assert reconstructed == key

    def test_is_immutable(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        result = parse_nfe(_generate_nfe())
        with pytest.raises(AttributeError):
            result.uf_code = "00"  # type: ignore

    def test_raises_on_short_input(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        with pytest.raises(ValueError, match="44 digits"):
            parse_nfe("1" * 43)

    def test_raises_on_long_input(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        with pytest.raises(ValueError, match="44 digits"):
            parse_nfe("1" * 45)

    def test_raises_on_non_string(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        with pytest.raises(ValueError, match="Expected str"):
            parse_nfe(1111111111111111111111111111111111111111111111)  # type: ignore

    def test_raises_on_empty(self) -> None:
        from validabr.parsers.nfe import parse_nfe

        with pytest.raises(ValueError, match="44 digits"):
            parse_nfe("")


class TestFormatNFE:
    def test_formats_raw_digits(self) -> None:
        from validabr.parsers.nfe import format_nfe

        raw = _generate_nfe()
        fmt = format_nfe(raw)
        assert fmt.count(" ") == 8
        assert len(fmt) == 52

    def test_formats_already_formatted(self) -> None:
        from validabr.parsers.nfe import format_nfe

        raw = _generate_nfe()
        fmt1 = format_nfe(raw)
        fmt2 = format_nfe(fmt1)
        assert fmt1 == fmt2

    def test_raises_on_short_input(self) -> None:
        from validabr.parsers.nfe import format_nfe

        with pytest.raises(ValueError, match="44 digits"):
            format_nfe("1" * 43)

    def test_raises_on_non_string(self) -> None:
        from validabr.parsers.nfe import format_nfe

        with pytest.raises(ValueError, match="Expected str"):
            format_nfe(1111111111111111111111111111111111111111111111)  # type: ignore
