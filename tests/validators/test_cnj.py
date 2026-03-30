from brdocs.validators.cnj import is_valid_cnj


class TestCNJValidator:
    def test_valid_cnj_formatted(self) -> None:
        assert is_valid_cnj("0000001-38.2024.8.26.0001") is True

    def test_valid_cnj_second_example(self) -> None:
        assert is_valid_cnj("0023456-74.2023.5.01.0050") is True

    def test_valid_cnj_unformatted(self) -> None:
        # Same as first example, no separators
        assert is_valid_cnj("00000013820248260001") is True

    def test_invalid_cnj_wrong_check_digits(self) -> None:
        assert is_valid_cnj("0000001-00.2024.8.26.0001") is False
        assert is_valid_cnj("0000001-99.2024.8.26.0001") is False

    def test_invalid_cnj_wrong_length(self) -> None:
        assert is_valid_cnj("000000138202482600") is False
        assert is_valid_cnj("000000138202482600011") is False

    def test_invalid_cnj_letters(self) -> None:
        assert is_valid_cnj("AAAAAAAA-BB.CCCC.D.EE.FFFF") is False

    def test_invalid_cnj_not_string(self) -> None:
        assert is_valid_cnj(None) is False  # type: ignore
        assert is_valid_cnj(12345) is False  # type: ignore

    def test_empty_cnj(self) -> None:
        assert is_valid_cnj("") is False
