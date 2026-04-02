"""Tests for validabr Pydantic v2 integration."""

import pytest

pydantic = pytest.importorskip("pydantic")

from pydantic import BaseModel, ValidationError  # noqa: E402

import validabr  # noqa: E402
from validabr.integrations.pydantic import (  # noqa: E402
    CNJ,
    CNPJ,
    CPF,
    Renavam,
    TituloEleitor,
)

# ---------------------------------------------------------------------------
# CPF
# ---------------------------------------------------------------------------


class TestCPFType:
    def test_accepts_valid_formatted(self) -> None:
        class M(BaseModel):
            cpf: CPF

        m = M(cpf="529.982.247-25")
        assert m.cpf == "529.982.247-25"

    def test_accepts_valid_unformatted(self) -> None:
        class M(BaseModel):
            cpf: CPF

        m = M(cpf="52998224725")
        # normalised to formatted form
        assert m.cpf == "529.982.247-25"

    def test_rejects_invalid_cpf(self) -> None:
        class M(BaseModel):
            cpf: CPF

        with pytest.raises(ValidationError):
            M(cpf="000.000.000-00")

    def test_rejects_wrong_length(self) -> None:
        class M(BaseModel):
            cpf: CPF

        with pytest.raises(ValidationError):
            M(cpf="123")

    def test_rejects_non_string(self) -> None:
        class M(BaseModel):
            cpf: CPF

        with pytest.raises(ValidationError):
            M(cpf=12345678901)  # type: ignore[arg-type]

    def test_json_schema_has_title(self) -> None:
        class M(BaseModel):
            cpf: CPF

        schema = M.model_json_schema()
        assert schema["properties"]["cpf"]["title"] == "CPF"

    def test_is_string_subclass(self) -> None:
        assert issubclass(CPF, str)

    def test_round_trip_with_generator(self) -> None:
        class M(BaseModel):
            cpf: CPF

        raw = validabr.generate_cpf()
        m = M(cpf=raw)
        assert validabr.is_valid_cpf(m.cpf)


# ---------------------------------------------------------------------------
# CNPJ
# ---------------------------------------------------------------------------


class TestCNPJType:
    def test_accepts_valid_formatted(self) -> None:
        class M(BaseModel):
            cnpj: CNPJ

        m = M(cnpj="11.222.333/0001-81")
        assert m.cnpj == "11.222.333/0001-81"

    def test_accepts_valid_unformatted(self) -> None:
        class M(BaseModel):
            cnpj: CNPJ

        m = M(cnpj="11222333000181")
        assert m.cnpj == "11.222.333/0001-81"

    def test_rejects_invalid_cnpj(self) -> None:
        class M(BaseModel):
            cnpj: CNPJ

        with pytest.raises(ValidationError):
            M(cnpj="00.000.000/0000-00")

    def test_rejects_non_string(self) -> None:
        class M(BaseModel):
            cnpj: CNPJ

        with pytest.raises(ValidationError):
            M(cnpj=12345678000195)  # type: ignore[arg-type]

    def test_json_schema_has_title(self) -> None:
        class M(BaseModel):
            cnpj: CNPJ

        schema = M.model_json_schema()
        assert schema["properties"]["cnpj"]["title"] == "CNPJ"

    def test_round_trip_with_generator(self) -> None:
        class M(BaseModel):
            cnpj: CNPJ

        raw = validabr.generate_cnpj()
        m = M(cnpj=raw)
        assert validabr.is_valid_cnpj(m.cnpj)


# ---------------------------------------------------------------------------
# CNJ
# ---------------------------------------------------------------------------


class TestCNJType:
    def test_accepts_valid_cnj(self) -> None:
        class M(BaseModel):
            cnj: CNJ

        raw = validabr.generate_cnj()
        m = M(cnj=raw)
        assert validabr.is_valid_cnj(m.cnj)

    def test_rejects_invalid_cnj(self) -> None:
        class M(BaseModel):
            cnj: CNJ

        with pytest.raises(ValidationError):
            M(cnj="0000000-00.0000.0.00.0000")

    def test_json_schema_has_title(self) -> None:
        class M(BaseModel):
            cnj: CNJ

        schema = M.model_json_schema()
        assert schema["properties"]["cnj"]["title"] == "CNJ"


# ---------------------------------------------------------------------------
# Renavam
# ---------------------------------------------------------------------------


class TestRenavamType:
    def test_accepts_valid_renavam(self) -> None:
        class M(BaseModel):
            renavam: Renavam

        raw = validabr.generate_renavam()
        m = M(renavam=raw)
        assert validabr.is_valid_renavam(m.renavam)

    def test_rejects_invalid_renavam(self) -> None:
        class M(BaseModel):
            renavam: Renavam

        with pytest.raises(ValidationError):
            M(renavam="00000000000")

    def test_json_schema_has_title(self) -> None:
        class M(BaseModel):
            renavam: Renavam

        schema = M.model_json_schema()
        assert schema["properties"]["renavam"]["title"] == "Renavam"


# ---------------------------------------------------------------------------
# TituloEleitor
# ---------------------------------------------------------------------------


class TestTituloEleitorType:
    def test_accepts_valid_titulo(self) -> None:
        class M(BaseModel):
            titulo: TituloEleitor

        raw = validabr.generate_titulo_eleitor()
        m = M(titulo=raw)
        assert validabr.is_valid_titulo_eleitor(m.titulo)

    def test_rejects_invalid_titulo(self) -> None:
        class M(BaseModel):
            titulo: TituloEleitor

        with pytest.raises(ValidationError):
            M(titulo="000000000000")

    def test_json_schema_has_title(self) -> None:
        class M(BaseModel):
            titulo: TituloEleitor

        schema = M.model_json_schema()
        assert schema["properties"]["titulo"]["title"] == "TituloEleitor"


# ---------------------------------------------------------------------------
# IE  (requires state)
# ---------------------------------------------------------------------------


class TestIEType:
    def test_accepts_valid_ie_with_state(self) -> None:
        from validabr.integrations.pydantic import ie_field

        SP_IE = ie_field("SP")

        class M(BaseModel):
            ie: SP_IE

        raw = validabr.generate_ie("SP")
        m = M(ie=raw)
        assert validabr.is_valid_ie(m.ie, "SP")

    def test_rejects_invalid_ie(self) -> None:
        from validabr.integrations.pydantic import ie_field

        SP_IE = ie_field("SP")

        class M(BaseModel):
            ie: SP_IE

        with pytest.raises(ValidationError):
            M(ie="000000000")

    def test_json_schema_has_title(self) -> None:
        from validabr.integrations.pydantic import ie_field

        SP_IE = ie_field("SP")

        class M(BaseModel):
            ie: SP_IE

        schema = M.model_json_schema()
        assert schema["properties"]["ie"]["title"] == "IE (SP)"


# ---------------------------------------------------------------------------
# Multiple fields in one model
# ---------------------------------------------------------------------------


class TestCompositeModel:
    def test_model_with_cpf_and_cnpj(self) -> None:
        class Client(BaseModel):
            cpf: CPF
            cnpj: CNPJ

        cpf = validabr.generate_cpf(formatted=True)
        cnpj = validabr.generate_cnpj(formatted=True)
        client = Client(cpf=cpf, cnpj=cnpj)
        assert validabr.is_valid_cpf(client.cpf)
        assert validabr.is_valid_cnpj(client.cnpj)

    def test_serialization_roundtrip(self) -> None:
        class M(BaseModel):
            cpf: CPF

        raw = validabr.generate_cpf()
        m = M(cpf=raw)
        dumped = m.model_dump()
        m2 = M(**dumped)
        assert m2.cpf == m.cpf
