from brdocs.generators.pis import generate_pis
from brdocs.validators.pis import is_valid_pis


class TestPISGenerator:
    def test_generate_raw_returns_11_digits(self) -> None:
        raw = generate_pis()
        assert len(raw) == 11
        assert raw.isdigit()

    def test_generate_formatted_returns_14_chars(self) -> None:
        fmt = generate_pis(formatted=True)
        assert len(fmt) == 14
        assert fmt.count(".") == 2
        assert fmt.count("-") == 1

    def test_generated_is_valid(self) -> None:
        for _ in range(10):
            assert is_valid_pis(generate_pis()) is True

    def test_formatted_round_trip(self) -> None:
        for _ in range(10):
            fmt = generate_pis(formatted=True)
            assert is_valid_pis(fmt) is True

    def test_generates_different_values(self) -> None:
        values = {generate_pis() for _ in range(100)}
        assert len(values) > 90


class TestPISGeneratorBranches:
    def test_all_same_digits_loop_rejection(self) -> None:
        from unittest.mock import patch

        call_count = 0

        def _side_effect(a: int, b: int) -> int:
            nonlocal call_count
            call_count += 1
            if call_count <= 10:
                return 5  # all-same → triggers continue
            return call_count % 7  # varied

        with patch("brdocs.generators.pis.random.randint", side_effect=_side_effect):
            pis = generate_pis()

        assert isinstance(pis, str)
        assert len(pis) == 11
