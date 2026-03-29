from pybrdoc.validators.cnpj import is_valid_cnpj


def test_valid_cnpj_unformatted() -> None:
    assert is_valid_cnpj("11222333000181") is True
    # Known real-world CNPJs (public corporate entities in Brazil)
    assert is_valid_cnpj("00000000000191") is True  # Banco do Brasil
    assert is_valid_cnpj("60746948000112") is True  # Banco Bradesco


def test_valid_cnpj_formatted() -> None:
    assert is_valid_cnpj("11.222.333/0001-81") is True
    assert is_valid_cnpj("00.000.000/0001-91") is True
    assert is_valid_cnpj("01.900.000/0001-00") is True


def test_invalid_cnpj_type() -> None:
    assert is_valid_cnpj(42) is False  # type: ignore
    assert is_valid_cnpj(None) is False  # type: ignore


def test_invalid_cnpj_bad_length() -> None:
    assert is_valid_cnpj("1122233300018") is False  # 13 digits
    assert is_valid_cnpj("11.222.333/0001-8") is False
    assert is_valid_cnpj("112223330001819") is False  # 15 digits


def test_invalid_cnpj_identical_digits() -> None:
    assert is_valid_cnpj("00000000000000") is False
    assert is_valid_cnpj("11111111111111") is False
    assert is_valid_cnpj("99999999999999") is False


def test_invalid_cnpj_math_error() -> None:
    # Changed last digit from 1 to 2 to intentionally break modulo 11
    assert is_valid_cnpj("11222333000182") is False


def test_cnpj_with_invalid_characters() -> None:
    assert is_valid_cnpj("11A222333000181") is False
    assert is_valid_cnpj("!@#$%¨&*()_+{}") is False
