from validabr.validators.pix import PixKeyType, classify_pix


class TestClassifyPix:
    def test_valid_cpf(self) -> None:
        from validabr.generators.cpf import generate_cpf

        assert classify_pix(generate_cpf()) is PixKeyType.CPF

    def test_valid_cnpj(self) -> None:
        from validabr.generators.cnpj import generate_cnpj

        assert classify_pix(generate_cnpj()) is PixKeyType.CNPJ

    def test_valid_email(self) -> None:
        assert classify_pix("test@example.com") is PixKeyType.EMAIL
        assert classify_pix("user.name+tag@domain.co.uk") is PixKeyType.EMAIL

    def test_valid_phone_10_digits(self) -> None:
        assert classify_pix("+5511999999999") is PixKeyType.PHONE

    def test_valid_phone_11_digits(self) -> None:
        assert classify_pix("+5521988888888") is PixKeyType.PHONE

    def test_valid_evp_uuid(self) -> None:
        assert classify_pix("123e4567-e12b-42d3-a456-426614174000") is PixKeyType.EVP
        assert classify_pix("A987CFC9-1A23-4BDE-9AB4-1234567890AB") is PixKeyType.EVP

    def test_invalid_email_no_at(self) -> None:
        assert classify_pix("notanemail") is None

    def test_invalid_email_no_domain(self) -> None:
        assert classify_pix("user@") is None

    def test_invalid_phone_no_plus(self) -> None:
        assert classify_pix("5511999999999") is None

    def test_invalid_phone_wrong_country(self) -> None:
        assert classify_pix("+12125551234") is None

    def test_invalid_evp_wrong_format(self) -> None:
        assert classify_pix("12345678-1234-1234-1234-123456789012") is None
        assert classify_pix("not-a-uuid") is None

    def test_invalid_random_string(self) -> None:
        assert classify_pix("abcdefghijklmnop") is None

    def test_invalid_not_string(self) -> None:
        assert classify_pix(None) is None  # type: ignore
        assert classify_pix(12345678901) is None  # type: ignore

    def test_invalid_empty(self) -> None:
        assert classify_pix("") is None

    def test_email_with_uppercase(self) -> None:
        assert classify_pix("User@Domain.COM") is PixKeyType.EMAIL

    def test_email_subdomain(self) -> None:
        assert classify_pix("user@mail.domain.com") is PixKeyType.EMAIL

    def test_import_error_falls_back_to_none(self) -> None:
        import sys
        from unittest.mock import patch

        with patch.dict(sys.modules, {"validabr.validators": None}):
            # With validabr.validators unavailable, CPF/CNPJ lookup raises ImportError
            result = classify_pix("52998224725")
            assert result is None
