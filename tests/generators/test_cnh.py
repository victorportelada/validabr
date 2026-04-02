from validabr.generators.cnh import generate_cnh
from validabr.validators.cnh import is_valid_cnh


class TestGenerateCNH:
    def test_returns_string(self) -> None:
        assert isinstance(generate_cnh(), str)

    def test_is_11_digits(self) -> None:
        cnh = generate_cnh()
        assert len(cnh) == 11
        assert cnh.isdigit()

    def test_generated_is_valid(self) -> None:
        for _ in range(20):
            assert is_valid_cnh(generate_cnh()) is True

    def test_generates_different_values(self) -> None:
        results = {generate_cnh() for _ in range(30)}
        assert len(results) > 1

    def test_never_all_same_digits(self) -> None:
        for _ in range(20):
            cnh = generate_cnh()
            assert len(set(cnh)) > 1


class TestGenerateCNHBranches:
    def test_all_same_digits_loop_rejection(self) -> None:
        from unittest.mock import patch

        call_count = 0

        def _side_effect(a: int, b: int) -> int:
            nonlocal call_count
            call_count += 1
            if call_count <= 9:
                return 5  # all-same base → triggers continue
            return call_count % 7  # varied

        with patch("validabr.generators.cnh.random.randint", side_effect=_side_effect):
            cnh = generate_cnh()

        assert isinstance(cnh, str)
        assert len(cnh) == 11
