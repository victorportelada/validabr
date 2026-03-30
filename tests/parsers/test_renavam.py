import pytest

from pybrdoc.generators.renavam import generate_renavam
from pybrdoc.parsers.renavam import format_renavam


class TestFormatRENAVAM:
    def test_formats_11_digit_raw(self) -> None:
        assert format_renavam("00123456789") == "0012345678-9"

    def test_formats_with_existing_hyphen(self) -> None:
        assert format_renavam("0012345678-9") == "0012345678-9"

    def test_pads_short_input_to_11(self) -> None:
        result = format_renavam("12345678")  # 8 digits → pad to 11
        assert len(result) == 12  # 10 digits + hyphen + 1
        assert result[10] == "-"

    def test_round_trip_with_generator(self) -> None:
        for _ in range(10):
            raw = generate_renavam()
            formatted = format_renavam(raw)
            assert formatted.count("-") == 1
            assert len(formatted) == 12

    def test_raises_on_too_short(self) -> None:
        with pytest.raises(ValueError, match=r"8-11 digits"):
            format_renavam("1234567")

    def test_raises_on_too_long(self) -> None:
        with pytest.raises(ValueError, match=r"8-11 digits"):
            format_renavam("123456789012")

    def test_raises_on_non_string(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_renavam(12345678901)  # type: ignore

    def test_raises_on_empty(self) -> None:
        with pytest.raises(ValueError, match=r"8-11 digits"):
            format_renavam("")

    def test_output_structure(self) -> None:
        result = format_renavam("00123456789")
        parts = result.split("-")
        assert len(parts) == 2
        assert len(parts[0]) == 10
        assert len(parts[1]) == 1
