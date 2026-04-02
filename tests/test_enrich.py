import json
import urllib.error
from unittest.mock import MagicMock, patch

from brdocuments.enrich import CEPEnrichment, CNPJEnrichment, enrich_cep, enrich_cnpj

_URLOPEN = "urllib.request.urlopen"


def _mock_urlopen(data: bytes) -> MagicMock:
    """Return a mock that acts as a context manager yielding a response with .read()."""
    response = MagicMock()
    response.read.return_value = data
    cm = MagicMock()
    cm.__enter__.return_value = response
    cm.__exit__.return_value = False
    return cm


def _mock_json(payload: dict) -> MagicMock:  # type: ignore[type-arg]
    return _mock_urlopen(json.dumps(payload).encode())


class TestEnrichCNPJ:
    def test_happy_path(self) -> None:
        payload = {
            "razao_social": "ACME LTDA",
            "nome_fantasia": "Acme",
            "cnae_codigo": "1234567",
            "cnae_descricao": " Comercio varejista",
            "descricao_situacao_cadastral": "ATIVA",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "municipio": "Sao Paulo",
            "uf": "SP",
        }
        with patch(_URLOPEN, return_value=_mock_json(payload)):
            result = enrich_cnpj("11222333000181")

        assert isinstance(result, CNPJEnrichment)
        assert result.cnpj == "11222333000181"
        assert result.razao_social == "ACME LTDA"
        assert result.nome_fantasia == "Acme"
        assert result.cnae_code == "1234567"
        assert result.cnae_description == " Comercio varejista"
        assert result.status == "ATIVA"
        assert result.endereco == "Rua das Flores, N123, Centro, Sao Paulo, SP"
        assert result.error is None

    def test_strips_formatting(self) -> None:
        payload = {
            "razao_social": "ACME LTDA",
            "nome_fantasia": None,
            "cnae_codigo": None,
            "cnae_descricao": None,
            "descricao_situacao_cadastral": None,
            "logradouro": None,
            "numero": None,
            "bairro": None,
            "municipio": None,
            "uf": None,
        }
        with patch(_URLOPEN, return_value=_mock_json(payload)):
            result = enrich_cnpj("11.222.333/0001-81")

        assert result.cnpj == "11222333000181"
        assert result.razao_social == "ACME LTDA"

    def test_http_404(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.HTTPError(
                url="",
                code=404,
                msg="",
                hdrs={},
                fp=None,  # type: ignore[arg-type]
            )
            result = enrich_cnpj("11222333000181")

        assert result.cnpj == "11222333000181"
        assert result.error == "not found"
        assert result.razao_social is None

    def test_http_500(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.HTTPError(
                url="",
                code=500,
                msg="",
                hdrs={},
                fp=None,  # type: ignore[arg-type]
            )
            result = enrich_cnpj("11222333000181")

        assert result.error == "server error"

    def test_http_other(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.HTTPError(
                url="",
                code=403,
                msg="",
                hdrs={},
                fp=None,  # type: ignore[arg-type]
            )
            result = enrich_cnpj("11222333000181")

        assert result.error == "http 403"

    def test_timeout(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.URLError("timed out")
            result = enrich_cnpj("11222333000181")

        assert result.cnpj == "11222333000181"
        assert result.error == "timeout"

    def test_invalid_json(self) -> None:
        with patch(_URLOPEN, return_value=_mock_urlopen(b"not json")):
            result = enrich_cnpj("11222333000181")

        assert result.cnpj == "11222333000181"
        assert result.error == "invalid response"

    def test_invalid_input_wrong_digit_count(self) -> None:
        result = enrich_cnpj("123")
        assert result.cnpj == "123"
        assert result.error == "invalid input"
        assert result.razao_social is None

    def test_endereco_none_when_no_location_fields(self) -> None:
        payload = {
            "razao_social": "ACME",
            "nome_fantasia": None,
            "cnae_codigo": None,
            "cnae_descricao": None,
            "descricao_situacao_cadastral": None,
            "logradouro": None,
            "numero": None,
            "bairro": None,
            "municipio": None,
            "uf": None,
        }
        with patch(_URLOPEN, return_value=_mock_json(payload)):
            result = enrich_cnpj("11222333000181")

        assert result.endereco is None

    def test_numero_sem_numero(self) -> None:
        payload = {
            "razao_social": "ACME",
            "nome_fantasia": None,
            "cnae_codigo": None,
            "cnae_descricao": None,
            "descricao_situacao_cadastral": None,
            "logradouro": "Rua X",
            "numero": "S/N",
            "bairro": None,
            "municipio": "SP",
            "uf": "SP",
        }
        with patch(_URLOPEN, return_value=_mock_json(payload)):
            result = enrich_cnpj("11222333000181")

        assert result.endereco is not None
        assert "S/N" not in (result.endereco or "")


class TestEnrichCEP:
    def test_happy_path(self) -> None:
        payload = {
            "cep": "01001000",
            "state": "SP",
            "city": "Sao Paulo",
            "street": "Praca da Se",
            "neighborhood": "Se",
        }
        with patch(_URLOPEN, return_value=_mock_json(payload)):
            result = enrich_cep("01001000")

        assert isinstance(result, CEPEnrichment)
        assert result.cep == "01001000"
        assert result.logradouro == "Praca da Se"
        assert result.bairro == "Se"
        assert result.cidade == "Sao Paulo"
        assert result.estado == "SP"
        assert result.error is None

    def test_strips_formatting(self) -> None:
        payload = {
            "cep": "01001000",
            "state": "SP",
            "city": "Sao Paulo",
            "street": "Praca da Se",
            "neighborhood": "Se",
        }
        with patch(_URLOPEN, return_value=_mock_json(payload)):
            result = enrich_cep("01001-000")

        assert result.cep == "01001000"
        assert result.cidade == "Sao Paulo"

    def test_http_404(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.HTTPError(
                url="",
                code=404,
                msg="",
                hdrs={},
                fp=None,  # type: ignore[arg-type]
            )
            result = enrich_cep("01001000")

        assert result.cep == "01001000"
        assert result.error == "not found"
        assert result.cidade is None

    def test_http_500(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.HTTPError(
                url="",
                code=500,
                msg="",
                hdrs={},
                fp=None,  # type: ignore[arg-type]
            )
            result = enrich_cep("01001000")

        assert result.error == "server error"

    def test_http_other(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.HTTPError(
                url="",
                code=429,
                msg="",
                hdrs={},
                fp=None,  # type: ignore[arg-type]
            )
            result = enrich_cep("01001000")

        assert result.error == "http 429"

    def test_timeout(self) -> None:
        with patch(_URLOPEN) as m:
            m.side_effect = urllib.error.URLError("timed out")
            result = enrich_cep("01001000")

        assert result.cep == "01001000"
        assert result.error == "timeout"

    def test_invalid_json(self) -> None:
        with patch(_URLOPEN, return_value=_mock_urlopen(b"not json")):
            result = enrich_cep("01001000")

        assert result.cep == "01001000"
        assert result.error == "invalid response"

    def test_invalid_input_wrong_digit_count(self) -> None:
        result = enrich_cep("12345")
        assert result.cep == "12345"
        assert result.error == "invalid input"
        assert result.cidade is None
