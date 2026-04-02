"""Tests for brdocuments Polars DataFrame extension integration."""

import pytest

polars = pytest.importorskip("polars")

import brdocuments  # noqa: E402
import brdocuments.integrations.polars  # noqa: E402 - registers extension


class TestIsValidExpr:
    def test_is_valid_cpf_true(self) -> None:
        df = polars.DataFrame({"cpf": ["529.982.247-25"]})
        result = df.select(polars.col("cpf").brdocuments.is_valid_cpf())
        assert result[0, 0] is True

    def test_is_valid_cpf_false(self) -> None:
        df = polars.DataFrame({"cpf": ["000.000.000-00"]})
        result = df.select(polars.col("cpf").brdocuments.is_valid_cpf())
        assert result[0, 0] is False

    def test_is_valid_cpf_mixed(self) -> None:
        df = polars.DataFrame({"cpf": ["529.982.247-25", "000.000.000-00", "123.456.789-00"]})
        result = df.select(polars.col("cpf").brdocuments.is_valid_cpf())
        assert result.to_series().to_list() == [True, False, False]

    def test_is_valid_cnpj_true(self) -> None:
        df = polars.DataFrame({"cnpj": ["11.222.333/0001-81"]})
        result = df.select(polars.col("cnpj").brdocuments.is_valid_cnpj())
        assert result[0, 0] is True

    def test_is_valid_cnpj_false(self) -> None:
        df = polars.DataFrame({"cnpj": ["00.000.000/0001-00"]})
        result = df.select(polars.col("cnpj").brdocuments.is_valid_cnpj())
        assert result[0, 0] is False

    def test_is_valid_ie_true(self) -> None:
        ie = brdocuments.generate_ie("SP")
        df = polars.DataFrame({"ie": [ie]})
        result = df.select(polars.col("ie").brdocuments.is_valid_ie("SP"))
        assert result[0, 0] is True

    def test_is_valid_ie_false(self) -> None:
        df = polars.DataFrame({"ie": ["123"]})
        result = df.select(polars.col("ie").brdocuments.is_valid_ie("SP"))
        assert result[0, 0] is False

    def test_is_valid_cep_true(self) -> None:
        df = polars.DataFrame({"cep": ["01310-100"]})
        result = df.select(polars.col("cep").brdocuments.is_valid_cep())
        assert result[0, 0] is True

    def test_is_valid_cep_false(self) -> None:
        df = polars.DataFrame({"cep": ["00000-000"]})
        result = df.select(polars.col("cep").brdocuments.is_valid_cep())
        assert result[0, 0] is False

    def test_is_valid_cnh_true(self) -> None:
        cnh = brdocuments.generate_cnh()
        df = polars.DataFrame({"cnh": [cnh]})
        result = df.select(polars.col("cnh").brdocuments.is_valid_cnh())
        assert result[0, 0] is True

    def test_is_valid_cnh_false(self) -> None:
        df = polars.DataFrame({"cnh": ["00000000000"]})
        result = df.select(polars.col("cnh").brdocuments.is_valid_cnh())
        assert result[0, 0] is False

    def test_is_valid_pis_true(self) -> None:
        pis = brdocuments.generate_pis()
        df = polars.DataFrame({"pis": [pis]})
        result = df.select(polars.col("pis").brdocuments.is_valid_pis())
        assert result[0, 0] is True

    def test_is_valid_pis_false(self) -> None:
        df = polars.DataFrame({"pis": ["000.00000.00-0"]})
        result = df.select(polars.col("pis").brdocuments.is_valid_pis())
        assert result[0, 0] is False

    def test_is_valid_renavam_true(self) -> None:
        raw = brdocuments.generate_renavam()
        df = polars.DataFrame({"renavam": [raw]})
        result = df.select(polars.col("renavam").brdocuments.is_valid_renavam())
        assert result[0, 0] is True

    def test_is_valid_renavam_false(self) -> None:
        df = polars.DataFrame({"renavam": ["00000000000"]})
        result = df.select(polars.col("renavam").brdocuments.is_valid_renavam())
        assert result[0, 0] is False

    def test_is_valid_titulo_eleitor_true(self) -> None:
        raw = brdocuments.generate_titulo_eleitor()
        df = polars.DataFrame({"titulo": [raw]})
        result = df.select(polars.col("titulo").brdocuments.is_valid_titulo_eleitor())
        assert result[0, 0] is True

    def test_is_valid_titulo_eleitor_false(self) -> None:
        df = polars.DataFrame({"titulo": ["000000000000"]})
        result = df.select(polars.col("titulo").brdocuments.is_valid_titulo_eleitor())
        assert result[0, 0] is False

    def test_is_valid_cnj_true(self) -> None:
        raw = brdocuments.generate_cnj()
        df = polars.DataFrame({"cnj": [raw]})
        result = df.select(polars.col("cnj").brdocuments.is_valid_cnj())
        assert result[0, 0] is True

    def test_is_valid_cnj_false(self) -> None:
        df = polars.DataFrame({"cnj": ["0000000-00.0000.0.00.0000"]})
        result = df.select(polars.col("cnj").brdocuments.is_valid_cnj())
        assert result[0, 0] is False

    def test_is_valid_nfe_false(self) -> None:
        df = polars.DataFrame({"nfe": ["0" * 44]})
        result = df.select(polars.col("nfe").brdocuments.is_valid_nfe())
        assert result[0, 0] is False

    def test_classify_pix_cpf(self) -> None:
        df = polars.DataFrame({"pix": ["529.982.247-25"]})
        result = df.select(polars.col("pix").brdocuments.classify_pix())
        assert result[0, 0] == "CPF"

    def test_classify_pix_cnpj(self) -> None:
        df = polars.DataFrame({"pix": ["11.222.333/0001-81"]})
        result = df.select(polars.col("pix").brdocuments.classify_pix())
        assert result[0, 0] == "CNPJ"

    def test_classify_pix_email(self) -> None:
        df = polars.DataFrame({"pix": ["email@example.com"]})
        result = df.select(polars.col("pix").brdocuments.classify_pix())
        assert result[0, 0] == "EMAIL"

    def test_classify_pix_phone(self) -> None:
        df = polars.DataFrame({"pix": ["+55 11 99999-9999"]})
        result = df.select(polars.col("pix").brdocuments.classify_pix())
        assert result[0, 0] == "PHONE"

    def test_classify_pix_evp(self) -> None:
        df = polars.DataFrame({"pix": ["chave_aleatoria"]})
        result = df.select(polars.col("pix").brdocuments.classify_pix())
        assert result[0, 0] == ""


class TestFormatExpr:
    def test_format_cpf(self) -> None:
        df = polars.DataFrame({"cpf": ["52998224725"]})
        result = df.select(polars.col("cpf").brdocuments.format_cpf())
        assert result[0, 0] == "529.982.247-25"

    def test_format_cpf_already_formatted(self) -> None:
        df = polars.DataFrame({"cpf": ["529.982.247-25"]})
        result = df.select(polars.col("cpf").brdocuments.format_cpf())
        assert result[0, 0] == "529.982.247-25"

    def test_format_cnpj(self) -> None:
        df = polars.DataFrame({"cnpj": ["11222333000181"]})
        result = df.select(polars.col("cnpj").brdocuments.format_cnpj())
        assert result[0, 0] == "11.222.333/0001-81"

    def test_format_cnpj_already_formatted(self) -> None:
        df = polars.DataFrame({"cnpj": ["11.222.333/0001-81"]})
        result = df.select(polars.col("cnpj").brdocuments.format_cnpj())
        assert result[0, 0] == "11.222.333/0001-81"

    def test_format_ie(self) -> None:
        df = polars.DataFrame({"ie": ["110042490114"]})
        result = df.select(polars.col("ie").brdocuments.format_ie("SP"))
        assert result[0, 0] == "110.042.490.114"

    def test_format_cep(self) -> None:
        df = polars.DataFrame({"cep": ["01310100"]})
        result = df.select(polars.col("cep").brdocuments.format_cep())
        assert result[0, 0] == "01310-100"

    def test_format_cnh(self) -> None:
        df = polars.DataFrame({"cnh": ["26459568096"]})
        result = df.select(polars.col("cnh").brdocuments.format_cnh())
        assert result[0, 0] == "26459568096"

    def test_format_pis(self) -> None:
        df = polars.DataFrame({"pis": ["17052505100"]})
        result = df.select(polars.col("pis").brdocuments.format_pis())
        assert result[0, 0] == "170.52505.10-0"

    def test_format_renavam(self) -> None:
        raw = brdocuments.generate_renavam()
        df = polars.DataFrame({"renavam": [raw]})
        result = df.select(polars.col("renavam").brdocuments.format_renavam())
        assert len(result[0, 0]) == 12
        assert "-" in result[0, 0]

    def test_format_titulo_eleitor(self) -> None:
        raw = brdocuments.generate_titulo_eleitor()
        df = polars.DataFrame({"titulo": [raw]})
        result = df.select(polars.col("titulo").brdocuments.format_titulo_eleitor())
        assert len(result[0, 0]) == 14
        assert " " in result[0, 0]

    def test_format_cnj(self) -> None:
        raw = brdocuments.generate_cnj()
        df = polars.DataFrame({"cnj": [raw]})
        result = df.select(polars.col("cnj").brdocuments.format_cnj())
        assert "-" in result[0, 0]
        assert "." in result[0, 0]

    def test_format_nfe(self) -> None:
        nfe44 = "53182010854130138184456324624839712561807001"
        df = polars.DataFrame({"nfe": [nfe44]})
        result = df.select(polars.col("nfe").brdocuments.format_nfe())
        assert len(result[0, 0]) == 52


class TestMaskExpr:
    def test_mask_cpf(self) -> None:
        df = polars.DataFrame({"cpf": ["529.982.247-25"]})
        result = df.select(polars.col("cpf").brdocuments.mask_cpf())
        assert result[0, 0] == "***.982.247-**"

    def test_mask_cpf_unformatted(self) -> None:
        df = polars.DataFrame({"cpf": ["52998224725"]})
        result = df.select(polars.col("cpf").brdocuments.mask_cpf())
        assert result[0, 0] == "***.982.247-**"

    def test_mask_cnpj(self) -> None:
        df = polars.DataFrame({"cnpj": ["11.222.333/0001-81"]})
        result = df.select(polars.col("cnpj").brdocuments.mask_cnpj())
        assert result[0, 0] == "**.222.333/****-**"

    def test_mask_cnpj_unformatted(self) -> None:
        df = polars.DataFrame({"cnpj": ["11222333000181"]})
        result = df.select(polars.col("cnpj").brdocuments.mask_cnpj())
        assert result[0, 0] == "**.222.333/****-**"


class TestChainedExpressions:
    def test_chain_is_valid_and_format(self) -> None:
        df = polars.DataFrame({"cpf": ["52998224725", "00000000000"]})
        result = df.select(
            polars.col("cpf").brdocuments.is_valid_cpf().alias("valid"),
        )
        assert result.to_series().to_list() == [True, False]

    def test_filter_valid_cpf(self) -> None:
        df = polars.DataFrame({"cpf": ["529.982.247-25", "000.000.000-00", "123"]})
        valid = df.filter(polars.col("cpf").brdocuments.is_valid_cpf())
        assert len(valid) == 1
        assert valid[0, 0] == "529.982.247-25"
