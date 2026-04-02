from brdocuments.generators.cep import generate_cep
from brdocuments.validators.cep import is_valid_cep


class TestCEPGenerator:
    def test_generate_raw_returns_8_digits(self) -> None:
        raw = generate_cep()
        assert len(raw) == 8
        assert raw.isdigit()

    def test_generate_formatted_returns_9_chars(self) -> None:
        fmt = generate_cep(formatted=True)
        assert len(fmt) == 9
        assert fmt.count("-") == 1

    def test_generated_is_valid(self) -> None:
        for _ in range(10):
            assert is_valid_cep(generate_cep()) is True

    def test_formatted_round_trip(self) -> None:
        for _ in range(10):
            fmt = generate_cep(formatted=True)
            assert is_valid_cep(fmt) is True

    def test_generates_different_values(self) -> None:
        values = {generate_cep() for _ in range(100)}
        assert len(values) > 90


class TestCEPGeneratorBranches:
    def test_all_same_digits_loop_rejection(self) -> None:
        from unittest.mock import patch

        call_count = 0

        def _side_effect(a: int, b: int) -> int:
            nonlocal call_count
            call_count += 1
            if call_count <= 8:
                return 5  # all-same → triggers continue
            return call_count % 7  # varied

        with patch("brdocuments.generators.cep.random.randint", side_effect=_side_effect):
            cep = generate_cep()

        assert isinstance(cep, str)
        assert len(cep) == 8
