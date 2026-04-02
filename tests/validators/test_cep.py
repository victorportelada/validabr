from validabr.validators.cep import is_valid_cep


class TestCEPValidator:
    def test_valid_cep_formatted(self) -> None:
        assert is_valid_cep("01310-000") is True

    def test_valid_cep_raw(self) -> None:
        assert is_valid_cep("01310000") is True

    def test_valid_cep_with_spaces(self) -> None:
        assert is_valid_cep("013 10 000") is True

    def test_invalid_cep_all_zeros(self) -> None:
        assert is_valid_cep("00000000") is False

    def test_invalid_cep_all_ones(self) -> None:
        assert is_valid_cep("11111111") is False

    def test_invalid_cep_wrong_length_short(self) -> None:
        assert is_valid_cep("0131000") is False

    def test_invalid_cep_wrong_length_long(self) -> None:
        assert is_valid_cep("013100000") is False

    def test_invalid_cep_letters(self) -> None:
        assert is_valid_cep("ABCDEFGH") is False

    def test_invalid_cep_not_string(self) -> None:
        assert is_valid_cep(None) is False  # type: ignore
        assert is_valid_cep(1310000) is False  # type: ignore

    def test_empty_cep(self) -> None:
        assert is_valid_cep("") is False

    def test_idempotent_format(self) -> None:
        assert is_valid_cep("01310-000") is True
