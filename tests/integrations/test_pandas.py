"""Tests for brdocs Pandas Series accessor integration."""

import pytest

pandas = pytest.importorskip("pandas")

import brdocs  # noqa: E402
import brdocs.integrations.pandas  # noqa: E402 - registers accessor


class TestIsValidAccessor:
    def test_is_valid_cpf_true(self) -> None:
        s = pandas.Series(["529.982.247-25"])
        result = s.brdocs.is_valid_cpf()
        assert isinstance(result, pandas.Series)
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_cpf_false(self) -> None:
        s = pandas.Series(["000.000.000-00"])
        result = s.brdocs.is_valid_cpf()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_cpf_mixed(self) -> None:
        s = pandas.Series(["529.982.247-25", "000.000.000-00", "123.456.789-00"])
        result = s.brdocs.is_valid_cpf()
        assert result.tolist() == [True, False, False]

    def test_is_valid_cnpj_true(self) -> None:
        s = pandas.Series(["11.222.333/0001-81"])
        result = s.brdocs.is_valid_cnpj()
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_cnpj_false(self) -> None:
        s = pandas.Series(["00.000.000/0001-00"])
        result = s.brdocs.is_valid_cnpj()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_ie_true(self) -> None:
        ie = brdocs.generate_ie("SP")
        s = pandas.Series([ie])
        result = s.brdocs.is_valid_ie("SP")
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_ie_false(self) -> None:
        s = pandas.Series(["123"])
        result = s.brdocs.is_valid_ie("SP")
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_cep_true(self) -> None:
        s = pandas.Series(["01310-100"])
        result = s.brdocs.is_valid_cep()
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_cep_false(self) -> None:
        s = pandas.Series(["00000-000"])
        result = s.brdocs.is_valid_cep()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_cnh_true(self) -> None:
        cnh = brdocs.generate_cnh()
        s = pandas.Series([cnh])
        result = s.brdocs.is_valid_cnh()
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_cnh_false(self) -> None:
        s = pandas.Series(["00000000000"])
        result = s.brdocs.is_valid_cnh()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_pis_true(self) -> None:
        pis = brdocs.generate_pis()
        s = pandas.Series([pis])
        result = s.brdocs.is_valid_pis()
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_pis_false(self) -> None:
        s = pandas.Series(["000.00000.00-0"])
        result = s.brdocs.is_valid_pis()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_renavam_true(self) -> None:
        raw = brdocs.generate_renavam()
        s = pandas.Series([raw])
        result = s.brdocs.is_valid_renavam()
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_renavam_false(self) -> None:
        s = pandas.Series(["00000000000"])
        result = s.brdocs.is_valid_renavam()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_titulo_eleitor_true(self) -> None:
        raw = brdocs.generate_titulo_eleitor()
        s = pandas.Series([raw])
        result = s.brdocs.is_valid_titulo_eleitor()
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_titulo_eleitor_false(self) -> None:
        s = pandas.Series(["000000000000"])
        result = s.brdocs.is_valid_titulo_eleitor()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_cnj_true(self) -> None:
        raw = brdocs.generate_cnj()
        s = pandas.Series([raw])
        result = s.brdocs.is_valid_cnj()
        assert result.iloc[0] == True  # noqa: E712

    def test_is_valid_cnj_false(self) -> None:
        s = pandas.Series(["0000000-00.0000.0.00.0000"])
        result = s.brdocs.is_valid_cnj()
        assert result.iloc[0] == False  # noqa: E712

    def test_is_valid_nfe_false(self) -> None:
        s = pandas.Series(["0" * 44])
        result = s.brdocs.is_valid_nfe()
        assert result.iloc[0] == False  # noqa: E712

    def test_classify_pix_cpf(self) -> None:
        s = pandas.Series(["529.982.247-25"])
        result = s.brdocs.classify_pix()
        assert result.iloc[0] == "CPF"

    def test_classify_pix_cnpj(self) -> None:
        s = pandas.Series(["11.222.333/0001-81"])
        result = s.brdocs.classify_pix()
        assert result.iloc[0] == "CNPJ"

    def test_classify_pix_email(self) -> None:
        s = pandas.Series(["email@example.com"])
        result = s.brdocs.classify_pix()
        assert result.iloc[0] == "EMAIL"

    def test_classify_pix_phone(self) -> None:
        s = pandas.Series(["+55 11 99999-9999"])
        result = s.brdocs.classify_pix()
        assert result.iloc[0] == "PHONE"

    def test_classify_pix_evp(self) -> None:
        s = pandas.Series(["123e4567-e12b-42d3-a456-426614174000"])
        result = s.brdocs.classify_pix()
        assert result.iloc[0] == "EVP"

    def test_classify_pix_unknown(self) -> None:
        s = pandas.Series(["chave_aleatoria"])
        result = s.brdocs.classify_pix()
        assert result.iloc[0] == ""


class TestFormatAccessor:
    def test_format_cpf(self) -> None:
        s = pandas.Series(["52998224725"])
        result = s.brdocs.format_cpf()
        assert result.iloc[0] == "529.982.247-25"

    def test_format_cpf_already_formatted(self) -> None:
        s = pandas.Series(["529.982.247-25"])
        result = s.brdocs.format_cpf()
        assert result.iloc[0] == "529.982.247-25"

    def test_format_cnpj(self) -> None:
        s = pandas.Series(["11222333000181"])
        result = s.brdocs.format_cnpj()
        assert result.iloc[0] == "11.222.333/0001-81"

    def test_format_cnpj_already_formatted(self) -> None:
        s = pandas.Series(["11.222.333/0001-81"])
        result = s.brdocs.format_cnpj()
        assert result.iloc[0] == "11.222.333/0001-81"

    def test_format_ie(self) -> None:
        s = pandas.Series(["110042490114"])
        result = s.brdocs.format_ie("SP")
        assert result.iloc[0] == "110.042.490.114"

    def test_format_cep(self) -> None:
        s = pandas.Series(["01310100"])
        result = s.brdocs.format_cep()
        assert result.iloc[0] == "01310-100"

    def test_format_cnh(self) -> None:
        s = pandas.Series(["26459568096"])
        result = s.brdocs.format_cnh()
        assert result.iloc[0] == "26459568096"

    def test_format_pis(self) -> None:
        s = pandas.Series(["17052505100"])
        result = s.brdocs.format_pis()
        assert result.iloc[0] == "170.52505.10-0"

    def test_format_renavam(self) -> None:
        raw = brdocs.generate_renavam()
        result = pandas.Series([raw]).brdocs.format_renavam()
        assert len(result.iloc[0]) == 12
        assert "-" in result.iloc[0]

    def test_format_titulo_eleitor(self) -> None:
        raw = brdocs.generate_titulo_eleitor()
        result = pandas.Series([raw]).brdocs.format_titulo_eleitor()
        assert len(result.iloc[0]) == 14
        assert " " in result.iloc[0]

    def test_format_cnj(self) -> None:
        raw = brdocs.generate_cnj()
        result = pandas.Series([raw]).brdocs.format_cnj()
        assert "-" in result.iloc[0]
        assert "." in result.iloc[0]

    def test_format_nfe(self) -> None:
        nfe44 = "53182010854130138184456324624839712561807001"
        result = pandas.Series([nfe44]).brdocs.format_nfe()
        assert len(result.iloc[0]) == 52


class TestMaskAccessor:
    def test_mask_cpf(self) -> None:
        s = pandas.Series(["529.982.247-25"])
        result = s.brdocs.mask_cpf()
        assert result.iloc[0] == "***.982.247-**"

    def test_mask_cpf_unformatted(self) -> None:
        s = pandas.Series(["52998224725"])
        result = s.brdocs.mask_cpf()
        assert result.iloc[0] == "***.982.247-**"

    def test_mask_cnpj(self) -> None:
        s = pandas.Series(["11.222.333/0001-81"])
        result = s.brdocs.mask_cnpj()
        assert result.iloc[0] == "**.222.333/****-**"

    def test_mask_cnpj_unformatted(self) -> None:
        s = pandas.Series(["11222333000181"])
        result = s.brdocs.mask_cnpj()
        assert result.iloc[0] == "**.222.333/****-**"


class TestIntegerInput:
    def test_is_valid_cpf_with_int(self) -> None:
        s = pandas.Series([52998224725])  # type: ignore[list-item]
        result = s.brdocs.is_valid_cpf()
        assert result.iloc[0] == True  # noqa: E712

    def test_format_cpf_with_int(self) -> None:
        s = pandas.Series([52998224725])  # type: ignore[list-item]
        result = s.brdocs.format_cpf()
        assert result.iloc[0] == "529.982.247-25"
