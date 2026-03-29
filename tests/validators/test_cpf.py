from pybrdoc.validators.cpf import is_valid_cpf

class TestCPFValidator:
    def test_valid_cpf_without_punctuation(self) -> None:
        # Known valid, randomly generated CPF
        assert is_valid_cpf("52998224725") is True

    def test_valid_cpf_with_punctuation(self) -> None:
        assert is_valid_cpf("529.982.247-25") is True

    def test_invalid_cpf_wrong_digits(self) -> None:
        # Changed the last verifier digit
        assert is_valid_cpf("52998224726") is False

    def test_invalid_cpf_all_same_digits(self) -> None:
        # A common edge case in CPF calculation
        assert is_valid_cpf("11111111111") is False
        assert is_valid_cpf("00000000000") is False

    def test_invalid_cpf_wrong_length(self) -> None:
        assert is_valid_cpf("123456789") is False
        assert is_valid_cpf("123456789012") is False

    def test_invalid_cpf_letters(self) -> None:
        assert is_valid_cpf("abc.def.ghi-jk") is False
        
    def test_empty_cpf(self) -> None:
        assert is_valid_cpf("") is False
        assert is_valid_cpf(None) is False  # type: ignore
