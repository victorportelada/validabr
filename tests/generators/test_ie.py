import pytest

from validabr.generators.ie import _VALID_STATES, generate_ie
from validabr.validators.ie import is_valid_ie


class TestGenerateIeErrors:
    def test_unknown_state_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown state code"):
            generate_ie("XX")

    def test_empty_state_raises(self) -> None:
        with pytest.raises(ValueError):
            generate_ie("")

    def test_lowercase_state_works(self) -> None:
        ie = generate_ie("sp")
        assert ie.isdigit()
        assert is_valid_ie(ie, "SP") is True


class TestGenerateIeOutput:
    @pytest.mark.parametrize("state", sorted(_VALID_STATES))
    def test_returns_string(self, state: str) -> None:
        assert isinstance(generate_ie(state), str)

    @pytest.mark.parametrize("state", sorted(_VALID_STATES))
    def test_returns_digits_only(self, state: str) -> None:
        ie = generate_ie(state)
        assert ie.isdigit(), f"{state!r} generator returned non-digits: {ie!r}"

    @pytest.mark.parametrize("state", sorted(_VALID_STATES))
    def test_generates_valid_ie(self, state: str) -> None:
        for _ in range(10):
            ie = generate_ie(state)
            assert is_valid_ie(ie, state), (
                f"Generated IE {ie!r} failed validation for state {state!r}"
            )

    @pytest.mark.parametrize("state", sorted(_VALID_STATES))
    def test_generates_different_values(self, state: str) -> None:
        # Should not always produce the same IE (randomness check)
        results = {generate_ie(state) for _ in range(20)}
        assert len(results) > 1, f"Generator for {state!r} always returns the same value"


# ─── Branch-coverage tests for generator internal paths ──────────────────────


class TestGenApRangeBranches:
    """Ensure _gen_ap produces valid output for all three numeric ranges."""

    def test_gen_ap_yields_valid_in_any_range(self) -> None:
        # Run many times to probabilistically hit all three branches
        from validabr.generators.ie import _gen_ap
        from validabr.validators.ie import is_valid_ie

        for _ in range(50):
            ie = _gen_ap()
            assert is_valid_ie(ie, "AP"), f"Generated AP IE {ie!r} failed validation"

    def test_gen_ap_else_branch_via_mock(self) -> None:
        """Force the else branch (n < 3_000_001) by mocking _rand to return zeros."""
        from unittest.mock import patch

        from validabr.generators import ie as ie_gen
        from validabr.validators.ie import is_valid_ie

        # Patching _rand to return [0,0,0,0,0,0] makes base = [0,3,0,0,0,0,0,0]
        # → n = 03000000 = 3,000,000 which is < 3_000_001 → else: p=9, d_extra=0
        with patch.object(ie_gen, "_rand", return_value=[0, 0, 0, 0, 0, 0]):
            ie = ie_gen._gen_ap()
        assert is_valid_ie(ie, "AP"), f"AP else-branch IE {ie!r} failed validation"


class TestGenAmTotalBranch:
    """Ensure _gen_am handles the total < 11 path (produces valid output)."""

    def test_gen_am_always_valid(self) -> None:
        from validabr.generators.ie import _gen_am
        from validabr.validators.ie import is_valid_ie

        for _ in range(30):
            ie = _gen_am()
            assert is_valid_ie(ie, "AM"), f"Generated AM IE {ie!r} failed validation"

    def test_gen_am_total_less_than_11_via_mock(self) -> None:
        """Force total < 11 in _gen_am by mocking _rand to return all zeros."""
        from unittest.mock import patch

        from validabr.generators import ie as ie_gen
        from validabr.validators.ie import is_valid_ie

        # all zeros → total=0 < 11 → check = 11 - 0 = 11, which is >9, loops again
        # Use [0,0,0,0,0,0,0,1] → total = 1*2 = 2 < 11 → check = 9
        with patch.object(ie_gen, "_rand", return_value=[0, 0, 0, 0, 0, 0, 0, 1]):
            ie = ie_gen._gen_am()
        assert is_valid_ie(ie, "AM"), f"AM total<11 IE {ie!r} failed validation"


class TestGenBaBranches:
    """Cover all _gen_ba branches: 8-digit, 9-digit, and invalid guard."""

    def test_gen_ba_8_digits(self) -> None:
        from validabr.generators.ie import _gen_ba
        from validabr.validators.ie import is_valid_ie

        ie = _gen_ba(digits=8)
        assert len(ie) == 8
        assert is_valid_ie(ie, "BA") is True

    def test_gen_ba_9_digits(self) -> None:
        from validabr.generators.ie import _gen_ba
        from validabr.validators.ie import is_valid_ie

        ie = _gen_ba(digits=9)
        assert len(ie) == 9
        assert is_valid_ie(ie, "BA") is True

    def test_gen_ba_invalid_digits_defaults_to_9(self) -> None:
        # digits not in {8, 9} → defaults to 9
        from validabr.generators.ie import _gen_ba
        from validabr.validators.ie import is_valid_ie

        ie = _gen_ba(digits=7)
        assert len(ie) == 9
        assert is_valid_ie(ie, "BA") is True


class TestGenPeFormats:
    """Cover both _gen_pe(new_format=False) and _gen_pe(new_format=True)."""

    def test_gen_pe_old_format(self) -> None:
        from validabr.generators.ie import _gen_pe
        from validabr.validators.ie import is_valid_ie

        ie = _gen_pe(new_format=False)
        assert len(ie) == 9
        assert is_valid_ie(ie, "PE") is True

    def test_gen_pe_new_format(self) -> None:
        from validabr.generators.ie import _gen_pe
        from validabr.validators.ie import is_valid_ie

        ie = _gen_pe(new_format=True)
        assert len(ie) == 14
        assert is_valid_ie(ie, "PE") is True


class TestGenRnFormats:
    """Cover _gen_rn(long=False) and _gen_rn(long=True)."""

    def test_gen_rn_short(self) -> None:
        from validabr.generators.ie import _gen_rn
        from validabr.validators.ie import is_valid_ie

        ie = _gen_rn(long=False)
        assert len(ie) == 9
        assert is_valid_ie(ie, "RN") is True

    def test_gen_rn_long(self) -> None:
        from validabr.generators.ie import _gen_rn
        from validabr.validators.ie import is_valid_ie

        ie = _gen_rn(long=True)
        assert len(ie) == 10
        assert is_valid_ie(ie, "RN") is True


class TestGenRoFormats:
    """Cover _gen_ro(long=True) and _gen_ro(long=False)."""

    def test_gen_ro_long(self) -> None:
        from validabr.generators.ie import _gen_ro
        from validabr.validators.ie import is_valid_ie

        ie = _gen_ro(long=True)
        assert len(ie) == 14
        assert is_valid_ie(ie, "RO") is True

    def test_gen_ro_short(self) -> None:
        from validabr.generators.ie import _gen_ro
        from validabr.validators.ie import is_valid_ie

        ie = _gen_ro(long=False)
        assert len(ie) == 9
        assert is_valid_ie(ie, "RO") is True
