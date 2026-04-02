from brdocs.generators.titulo_eleitor import generate_titulo_eleitor
from brdocs.validators.titulo_eleitor import is_valid_titulo_eleitor


class TestGenerateTituloEleitor:
    def test_returns_string(self) -> None:
        assert isinstance(generate_titulo_eleitor(), str)

    def test_is_12_digits(self) -> None:
        t = generate_titulo_eleitor()
        assert len(t) == 12
        assert t.isdigit()

    def test_generated_is_valid(self) -> None:
        for _ in range(50):
            assert is_valid_titulo_eleitor(generate_titulo_eleitor()) is True

    def test_specific_state_code_sp(self) -> None:
        for _ in range(20):
            t = generate_titulo_eleitor(state_code=1)
            assert t[8:10] == "01"
            assert is_valid_titulo_eleitor(t) is True

    def test_specific_state_code_mg(self) -> None:
        for _ in range(20):
            t = generate_titulo_eleitor(state_code=2)
            assert t[8:10] == "02"
            assert is_valid_titulo_eleitor(t) is True

    def test_all_state_codes_produce_valid_titles(self) -> None:
        for sc in range(1, 29):
            for _ in range(5):
                assert is_valid_titulo_eleitor(generate_titulo_eleitor(state_code=sc))

    def test_invalid_state_code_raises(self) -> None:
        import pytest

        with pytest.raises(ValueError):
            generate_titulo_eleitor(state_code=0)
        with pytest.raises(ValueError):
            generate_titulo_eleitor(state_code=29)

    def test_generates_different_values(self) -> None:
        results = {generate_titulo_eleitor() for _ in range(30)}
        assert len(results) > 1
