from brdocs.generators.cpf import generate_cpf
from brdocs.validators.cpf import is_valid_cpf


class TestGenerateCpf:
    def test_returns_string(self) -> None:
        assert isinstance(generate_cpf(), str)

    def test_unformatted_is_11_digits(self) -> None:
        cpf = generate_cpf()
        assert len(cpf) == 11
        assert cpf.isdigit()

    def test_formatted_has_correct_pattern(self) -> None:
        cpf = generate_cpf(formatted=True)
        parts = cpf.split(".")
        assert len(parts) == 3
        assert len(parts[0]) == 3
        assert "-" in parts[2]

    def test_generated_cpf_is_valid(self) -> None:
        for _ in range(20):
            assert is_valid_cpf(generate_cpf()) is True

    def test_formatted_cpf_is_valid(self) -> None:
        for _ in range(10):
            assert is_valid_cpf(generate_cpf(formatted=True)) is True

    def test_generates_different_values(self) -> None:
        results = {generate_cpf() for _ in range(30)}
        assert len(results) > 1

    def test_never_all_same_digits(self) -> None:
        for _ in range(20):
            cpf = generate_cpf()
            assert len(set(cpf)) > 1, f"All-same-digit CPF generated: {cpf}"


class TestGenerateCpfBranches:
    """Cover internal loop branches via mocking."""

    def test_all_same_digits_loop_rejection(self) -> None:
        """Force the all-same-digit rejection (line 19) to execute."""
        from unittest.mock import patch

        _call_count = 0

        def _side_effect(a: int, b: int) -> int:
            nonlocal _call_count
            _call_count += 1
            # First 9 calls: return 5 (all-same base -> triggers continue)
            # Next calls: return varied values (valid base)
            if _call_count <= 9:
                return 5
            return _call_count % 7  # varied, not all-same

        with patch("brdocs.generators.cpf.random.randint", side_effect=_side_effect):
            cpf = generate_cpf()

        assert isinstance(cpf, str)
        assert len(cpf) == 11
