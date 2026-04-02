import logging

import pytest

from brdocs.secure import (
    BRDocFilter,
    mask_cep,
    mask_cnpj,
    mask_cns,
    mask_cpf,
    mask_pis,
    redact_text,
)


class TestRedactText:
    def test_redacts_valid_cpf(self) -> None:
        result = redact_text("Cliente CPF 529.982.247-25 pagou R$100")
        assert "529.982.247-25" not in result
        assert "*" in result

    def test_keeps_invalid_cpf(self) -> None:
        result = redact_text("bad cpf 000.000.000-00 here")
        assert "000.000.000-00" in result

    def test_redacts_valid_cnpj(self) -> None:
        result = redact_text("empresa 11.222.333/0001-81 fatura")
        assert "11.222.333/0001-81" not in result
        assert "*" in result

    def test_keeps_invalid_cnpj(self) -> None:
        result = redact_text("cnpj 00.000.000/0000-00 invalido")
        assert "00.000.000/0000-00" in result

    def test_redacts_multiple_in_one_string(self) -> None:
        text = "CPF 529.982.247-25 e CNPJ 11.222.333/0001-81"
        result = redact_text(text)
        assert "529.982.247-25" not in result
        assert "11.222.333/0001-81" not in result

    def test_types_filter_cpf_only(self) -> None:
        text = "CPF 529.982.247-25 CNPJ 11.222.333/0001-81"
        result = redact_text(text, types=["cpf"])
        assert "529.982.247-25" not in result
        assert "11.222.333/0001-81" in result

    def test_types_filter_cnpj_only(self) -> None:
        text = "CPF 529.982.247-25 CNPJ 11.222.333/0001-81"
        result = redact_text(text, types=["cnpj"])
        assert "529.982.247-25" in result
        assert "11.222.333/0001-81" not in result

    def test_no_pii_unchanged(self) -> None:
        text = "nothing sensitive here 12345"
        assert redact_text(text) == text

    def test_unsupported_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported type"):
            redact_text("text", types=["passport"])

    def test_non_string_raises(self) -> None:
        with pytest.raises(TypeError, match="must be str"):
            redact_text(12345)  # type: ignore[arg-type]

    def test_empty_string(self) -> None:
        assert redact_text("") == ""

    def test_raw_digits_cpf(self) -> None:
        result = redact_text("cpf: 52998224725 end")
        assert "52998224725" not in result

    def test_raw_digits_cnpj(self) -> None:
        result = redact_text("cnpj: 11222333000181 end")
        assert "11222333000181" not in result

    def test_returns_new_string(self) -> None:
        original = "CPF 529.982.247-25"
        result = redact_text(original)
        assert result is not original


class TestBRDocFilter:
    def _make_record(self, msg: str) -> logging.LogRecord:
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=msg,
            args=(),
            exc_info=None,
        )
        return record

    def test_filter_redacts_cpf_in_msg(self) -> None:
        f = BRDocFilter()
        record = self._make_record("user cpf 529.982.247-25 login")
        f.filter(record)
        assert "529.982.247-25" not in record.msg
        assert "*" in record.msg

    def test_filter_redacts_cnpj_in_msg(self) -> None:
        f = BRDocFilter()
        record = self._make_record("empresa 11.222.333/0001-81")
        f.filter(record)
        assert "11.222.333/0001-81" not in record.msg

    def test_filter_returns_true(self) -> None:
        f = BRDocFilter()
        record = self._make_record("some log")
        assert f.filter(record) is True

    def test_filter_custom_types(self) -> None:
        f = BRDocFilter(types=["cpf"])
        record = self._make_record("CPF 529.982.247-25 CNPJ 11.222.333/0001-81")
        f.filter(record)
        assert "529.982.247-25" not in record.msg
        assert "11.222.333/0001-81" in record.msg

    def test_filter_custom_fields(self) -> None:
        f = BRDocFilter(fields=["msg", "funcName"])
        record = self._make_record("clean")
        record.funcName = "fn:529.982.247-25"  # type: ignore[attr-defined]
        f.filter(record)
        assert "529.982.247-25" not in record.funcName  # type: ignore[attr-defined]

    def test_filter_non_string_field_skipped(self) -> None:
        f = BRDocFilter(fields=["lineno"])
        record = self._make_record("safe")
        result = f.filter(record)
        assert result is True
        assert record.lineno == 0

    def test_filter_attaches_to_handler(self) -> None:
        handler = logging.StreamHandler()
        handler.addFilter(BRDocFilter())
        logger = logging.getLogger("test_brdoc_filter_attach")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.info("user 529.982.247-25 action")
        logger.removeHandler(handler)


class TestMaskFunctions:
    def test_mask_cpf_formatted(self) -> None:
        assert mask_cpf("529.982.247-25") == "***.982.247-**"

    def test_mask_cpf_raw(self) -> None:
        assert mask_cpf("52998224725") == "***.982.247-**"

    def test_mask_cpf_fallback(self) -> None:
        result = mask_cpf("123")
        assert result == "***"

    def test_mask_cnpj_formatted(self) -> None:
        assert mask_cnpj("11.222.333/0001-81") == "**.222.333/****-**"

    def test_mask_cnpj_raw(self) -> None:
        assert mask_cnpj("11222333000181") == "**.222.333/****-**"

    def test_mask_cnpj_fallback(self) -> None:
        assert mask_cnpj("123") == "***"

    def test_mask_pis_formatted(self) -> None:
        result = mask_pis("123.45678.90-1")
        assert "**" in result

    def test_mask_pis_raw(self) -> None:
        result = mask_pis("12345678901")
        assert "**" in result

    def test_mask_pis_fallback(self) -> None:
        assert mask_pis("123") == "***"

    def test_mask_cep_formatted(self) -> None:
        assert mask_cep("01310-100") == "01310-***"

    def test_mask_cep_raw(self) -> None:
        assert mask_cep("01310100") == "01310-***"

    def test_mask_cep_fallback(self) -> None:
        assert mask_cep("123") == "***"

    def test_mask_cns_valid(self) -> None:
        result = mask_cns("167441640030005")
        assert result == "167 **** **** ****"

    def test_mask_cns_formatted(self) -> None:
        result = mask_cns("167 4416 4003 0005")
        assert result == "167 **** **** ****"

    def test_mask_cns_fallback(self) -> None:
        assert mask_cns("123") == "***"
