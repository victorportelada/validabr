from brdocs.generators.cns import generate_cns


class TestCNSGenerator:
    def test_generate_raw_returns_15_digits(self) -> None:
        raw = generate_cns()
        assert len(raw) == 15
        assert raw.isdigit()

    def test_generate_formatted_returns_18_chars(self) -> None:
        fmt = generate_cns(formatted=True)
        assert len(fmt) == 18
        assert fmt.count(" ") == 3

    def test_generated_is_valid(self) -> None:
        from brdocs.validators.cns import is_valid_cns

        for _ in range(10):
            assert is_valid_cns(generate_cns()) is True

    def test_formatted_round_trip(self) -> None:
        from brdocs.validators.cns import is_valid_cns

        for _ in range(10):
            fmt = generate_cns(formatted=True)
            assert is_valid_cns(fmt) is True

    def test_generates_different_values(self) -> None:
        values = {generate_cns() for _ in range(100)}
        assert len(values) > 90

    def test_all_same_digits_loop_rejection(self) -> None:
        from unittest.mock import patch

        call_count = 0

        def _side_effect(a: int, b: int) -> int:
            nonlocal call_count
            call_count += 1
            if call_count <= 15:
                return 1
            return call_count % 10

        with patch("brdocs.generators.cns.random.randint", side_effect=_side_effect):
            cns = generate_cns()

        assert isinstance(cns, str)
        assert len(cns) == 15
