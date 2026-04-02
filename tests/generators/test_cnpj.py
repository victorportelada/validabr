from validabr.generators.cnpj import generate_cnpj
from validabr.validators.cnpj import is_valid_cnpj


class TestGenerateCnpj:
    def test_returns_string(self) -> None:
        assert isinstance(generate_cnpj(), str)

    def test_unformatted_is_14_digits(self) -> None:
        cnpj = generate_cnpj()
        assert len(cnpj) == 14
        assert cnpj.isdigit()

    def test_formatted_has_correct_separators(self) -> None:
        cnpj = generate_cnpj(formatted=True)
        assert "." in cnpj
        assert "/" in cnpj
        assert "-" in cnpj
        # Strip formatting and check 14 digits
        digits = cnpj.replace(".", "").replace("/", "").replace("-", "")
        assert len(digits) == 14
        assert digits.isdigit()

    def test_generated_cnpj_is_valid(self) -> None:
        for _ in range(20):
            assert is_valid_cnpj(generate_cnpj()) is True

    def test_formatted_cnpj_is_valid(self) -> None:
        for _ in range(10):
            assert is_valid_cnpj(generate_cnpj(formatted=True)) is True

    def test_generates_different_values(self) -> None:
        results = {generate_cnpj() for _ in range(30)}
        assert len(results) > 1

    def test_branch_code_is_0001(self) -> None:
        # Generator always produces headquarters branch (0001)
        for _ in range(10):
            cnpj = generate_cnpj()
            assert cnpj[8:12] == "0001"


class TestGenerateCnpjAlfa:
    def test_returns_string(self) -> None:

        cnpj = generate_cnpj(alfa=True)
        assert isinstance(cnpj, str)
        assert len(cnpj) == 14

    def test_may_contain_letters(self) -> None:
        results = [generate_cnpj(alfa=True) for _ in range(50)]
        assert any(not r.isdigit() for r in results)

    def test_branch_still_0001(self) -> None:
        for _ in range(10):
            cnpj = generate_cnpj(alfa=True)
            assert cnpj[8:12] == "0001"

    def test_dv_always_digits(self) -> None:
        for _ in range(10):
            cnpj = generate_cnpj(alfa=True)
            assert cnpj[12:].isdigit()

    def test_formatted_alfa_structure(self) -> None:
        cnpj = generate_cnpj(formatted=True, alfa=True)
        assert cnpj[2] == "."
        assert cnpj[6] == "."
        assert "/" in cnpj
        assert "-" in cnpj

    def test_generated_alfa_is_valid(self) -> None:
        from validabr.validators.cnpj import is_valid_cnpj

        for _ in range(20):
            assert is_valid_cnpj(generate_cnpj(alfa=True)) is True

    def test_no_excluded_letters(self) -> None:
        excluded = set("IOUQF")
        for _ in range(50):
            cnpj = generate_cnpj(alfa=True)
            assert not (excluded & set(cnpj[:12]))


class TestGenerateCnpjBranches:
    """Cover internal loop branches via mocking."""

    def test_all_same_digits_loop_rejection(self) -> None:
        """Force the all-same-digit rejection (line 20) to execute."""
        from unittest.mock import patch

        _call_count = 0

        def _side_effect(a: int, b: int) -> int:
            nonlocal _call_count
            _call_count += 1
            # First 8 calls: return 3 (all-same base of 8 digits -> continue)
            # Next calls: return varied values starting from 0
            if _call_count <= 8:
                return 3
            return _call_count % 7

        with patch("validabr.generators.cnpj.random.randint", side_effect=_side_effect):
            cnpj = generate_cnpj()

        assert isinstance(cnpj, str)
        assert len(cnpj) == 14
