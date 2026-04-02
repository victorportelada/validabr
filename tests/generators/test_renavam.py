from brdocuments.generators.renavam import generate_renavam
from brdocuments.validators.renavam import is_valid_renavam


class TestGenerateRenavam:
    def test_returns_string(self) -> None:
        assert isinstance(generate_renavam(), str)

    def test_unformatted_is_11_digits(self) -> None:
        r = generate_renavam()
        assert len(r) == 11
        assert r.isdigit()

    def test_formatted_has_hyphen(self) -> None:
        r = generate_renavam(formatted=True)
        assert r[-2] == "-"
        digits = r.replace("-", "")
        assert len(digits) == 11
        assert digits.isdigit()

    def test_generated_renavam_is_valid(self) -> None:
        for _ in range(20):
            assert is_valid_renavam(generate_renavam()) is True

    def test_formatted_renavam_is_valid(self) -> None:
        for _ in range(10):
            assert is_valid_renavam(generate_renavam(formatted=True)) is True

    def test_generates_different_values(self) -> None:
        results = {generate_renavam() for _ in range(30)}
        assert len(results) > 1

    def test_never_all_zeros(self) -> None:
        for _ in range(20):
            r = generate_renavam()
            assert r != "0" * 11
