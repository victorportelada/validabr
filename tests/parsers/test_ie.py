import re

import pytest

from brdocuments.generators.ie import generate_ie
from brdocuments.parsers.ie import IEData, format_ie, parse_ie
from brdocuments.validators.ie import is_valid_ie

_ALL_STATES = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]


class TestFormatIeGuardClauses:
    def test_raises_on_non_string_ie(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_ie(123456789, "SP")  # type: ignore

    def test_raises_on_non_string_state(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            format_ie("123456789012", 42)  # type: ignore

    def test_raises_on_unknown_state(self) -> None:
        with pytest.raises(ValueError, match="Unknown state code"):
            format_ie("123456789012", "XX")

    def test_state_is_case_insensitive(self) -> None:
        raw = generate_ie("SP")
        assert format_ie(raw, "sp") == format_ie(raw, "SP")
        assert format_ie(raw, "Sp") == format_ie(raw, "SP")

    def test_raises_on_empty_ie(self) -> None:
        with pytest.raises(ValueError):
            format_ie("", "SP")

    def test_raises_on_empty_state(self) -> None:
        with pytest.raises(ValueError, match="Unknown state code"):
            format_ie("123456789012", "")


class TestFormatIeRoundTrip:
    @pytest.mark.parametrize("state", _ALL_STATES)
    def test_round_trip(self, state: str) -> None:
        for _ in range(3):
            raw = generate_ie(state)
            formatted = format_ie(raw, state)
            # formatted must contain only digits and allowed punctuation
            assert re.fullmatch(r"[\d.\-/ ]+", formatted), (
                f"{state}: unexpected char in '{formatted}'"
            )
            # strip back to digits and revalidate
            stripped = re.sub(r"\D", "", formatted)
            assert is_valid_ie(stripped, state), f"{state}: re-validation failed for '{stripped}'"
            # digit count is preserved
            assert stripped == raw

    @pytest.mark.parametrize("state", _ALL_STATES)
    def test_already_formatted_is_idempotent(self, state: str) -> None:
        raw = generate_ie(state)
        once = format_ie(raw, state)
        twice = format_ie(once, state)
        assert once == twice


class TestFormatIeWrongLength:
    @pytest.mark.parametrize(
        "state,bad_digits",
        [
            ("SP", "1" * 11),  # SP needs 12
            ("MG", "1" * 12),  # MG needs 13
            ("PR", "1" * 9),  # PR needs 10
            ("RS", "1" * 9),  # RS needs 10
            ("RJ", "1" * 9),  # RJ needs 8
            ("SC", "1" * 8),  # SC needs 9
            ("MT", "1" * 10),  # MT needs 11
            ("AC", "1" * 12),  # AC needs 13
        ],
    )
    def test_wrong_length_raises(self, state: str, bad_digits: str) -> None:
        with pytest.raises(ValueError, match="digits"):
            format_ie(bad_digits, state)

    @pytest.mark.parametrize(
        "state,bad_digits",
        [
            ("PE", "1" * 10),  # PE needs 9 or 14
            ("RN", "1" * 11),  # RN needs 9 or 10
            ("BA", "1" * 7),  # BA needs 8 or 9
            ("RO", "1" * 10),  # RO needs 9 or 14
        ],
    )
    def test_dual_length_wrong_raises(self, state: str, bad_digits: str) -> None:
        with pytest.raises(ValueError, match="or"):
            format_ie(bad_digits, state)


class TestFormatIeDualLength:
    def test_ba_9_succeeds(self) -> None:
        raw9 = generate_ie("BA")
        assert len(raw9) == 9
        fmt9 = format_ie(raw9, "BA")
        assert "-" in fmt9
        assert len(fmt9) == 10  # XXXXXXX-XX

    def test_ba_8_succeeds(self) -> None:
        # BA 8-digit: XXXXXX-XX → len 9
        raw8 = "12345678"
        fmt = format_ie(raw8, "BA")
        assert fmt == "123456-78"
        assert len(fmt) == 9

    def test_pe_9_succeeds(self) -> None:
        raw9 = generate_ie("PE")
        assert len(raw9) == 9
        fmt9 = format_ie(raw9, "PE")
        assert "-" in fmt9

    def test_pe_14_succeeds(self) -> None:
        # PE 14-digit: XX.X.XXX.XXXXXXX-X
        raw14 = "12345678901234"
        fmt = format_ie(raw14, "PE")
        assert fmt == "12.3.456.7890123-4"
        assert fmt.count(".") == 3
        assert fmt.count("-") == 1

    def test_rn_9_succeeds(self) -> None:
        raw = generate_ie("RN")
        assert len(raw) == 9
        fmt = format_ie(raw, "RN")
        assert "-" in fmt

    def test_rn_10_succeeds(self) -> None:
        # RN 10-digit: XX.XXX.XXX.X-X
        raw10 = "1234567890"
        fmt = format_ie(raw10, "RN")
        assert fmt == "12.345.678.9-0"
        assert fmt.count(".") == 3
        assert "-" in fmt

    def test_ro_succeeds(self) -> None:
        raw = generate_ie("RO")
        fmt = format_ie(raw, "RO")
        assert isinstance(fmt, str)
        assert len(fmt) >= 9


class TestFormatIeKnownStructure:
    def test_sp_four_dot_separated_groups_of_three(self) -> None:
        raw = generate_ie("SP")
        fmt = format_ie(raw, "SP")
        groups = fmt.split(".")
        assert len(groups) == 4
        assert all(len(g) == 3 for g in groups)

    def test_rs_slash_after_three_digits(self) -> None:
        raw = generate_ie("RS")
        fmt = format_ie(raw, "RS")
        assert fmt[3] == "/"
        assert len(fmt) == 11  # XXX/XXXXXXX

    def test_mg_slash_after_nine_digits(self) -> None:
        raw = generate_ie("MG")
        fmt = format_ie(raw, "MG")
        assert "/" in fmt
        left, right = fmt.split("/")
        assert len(re.sub(r"\D", "", left)) == 9
        assert len(right) == 4

    def test_pr_dot_then_hyphen(self) -> None:
        raw = generate_ie("PR")
        fmt = format_ie(raw, "PR")
        assert fmt[3] == "."
        assert "-" in fmt
        assert len(fmt) == 12  # XXX.XXXXX-XX

    def test_rj_two_dots_and_hyphen(self) -> None:
        raw = generate_ie("RJ")
        fmt = format_ie(raw, "RJ")
        assert fmt.count(".") == 2
        assert fmt.count("-") == 1
        assert len(fmt) == 11  # XX.XXX.XX-X

    def test_pa_two_hyphens(self) -> None:
        raw = generate_ie("PA")
        fmt = format_ie(raw, "PA")
        assert fmt.count("-") == 2
        assert len(fmt) == 11  # XX-XXXXXX-X

    def test_sc_three_dot_separated_groups(self) -> None:
        raw = generate_ie("SC")
        fmt = format_ie(raw, "SC")
        groups = fmt.split(".")
        assert len(groups) == 3

    def test_ac_slash_and_hyphen(self) -> None:
        raw = generate_ie("AC")
        fmt = format_ie(raw, "AC")
        assert "/" in fmt
        assert "-" in fmt
        assert len(fmt) == 17  # XXX.XXX.XXX/XXX-XX


class TestParseIE:
    def test_returns_ie_data(self) -> None:
        raw = generate_ie("SP")
        result = parse_ie(raw, "SP")
        assert isinstance(result, IEData)

    def test_digits_normalized(self) -> None:
        raw = generate_ie("SP")
        result = parse_ie(raw, "SP")
        assert result.digits == raw

    def test_state_normalized_to_uppercase(self) -> None:
        raw = generate_ie("SP")
        result = parse_ie(raw, "sp")
        assert result.state == "SP"

    def test_accepts_formatted_input(self) -> None:
        raw = generate_ie("SP")
        formatted = format_ie(raw, "SP")
        result = parse_ie(formatted, "SP")
        assert result.digits == raw
        assert result.state == "SP"

    @pytest.mark.parametrize("state", _ALL_STATES)
    def test_round_trip_all_states(self, state: str) -> None:
        raw = generate_ie(state)
        parsed = parse_ie(raw, state)
        assert parsed.digits == raw
        assert parsed.state == state

    def test_is_immutable(self) -> None:
        raw = generate_ie("SP")
        result = parse_ie(raw, "SP")
        with pytest.raises(AttributeError):
            result.digits = "000000000000"  # type: ignore

    def test_raises_on_non_string_ie(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_ie(123456789012, "SP")  # type: ignore

    def test_raises_on_non_string_state(self) -> None:
        with pytest.raises(ValueError, match="Expected str"):
            parse_ie("123456789012", 42)  # type: ignore

    def test_raises_on_unknown_state(self) -> None:
        with pytest.raises(ValueError, match="Unknown state code"):
            parse_ie("123456789012", "XX")

    def test_raises_on_wrong_length(self) -> None:
        with pytest.raises(ValueError, match="digits"):
            parse_ie("1" * 11, "SP")  # SP needs 12

    def test_raises_on_dual_length_wrong(self) -> None:
        with pytest.raises(ValueError, match="or"):
            parse_ie("1" * 10, "PE")  # PE needs 9 or 14
