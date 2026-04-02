from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import NamedTuple


class CNPJEnrichment(NamedTuple):
    cnpj: str
    razao_social: str | None
    nome_fantasia: str | None
    cnae_code: str | None
    cnae_description: str | None
    status: str | None
    endereco: str | None
    error: str | None


class CEPEnrichment(NamedTuple):
    cep: str
    logradouro: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None
    error: str | None


def enrich_cnpj(cnpj: str, timeout: int = 10) -> CNPJEnrichment:
    digits = re.sub(r"\D", "", cnpj)
    if len(digits) != 14:
        return CNPJEnrichment(
            cnpj=cnpj,
            razao_social=None,
            nome_fantasia=None,
            cnae_code=None,
            cnae_description=None,
            status=None,
            endereco=None,
            error="invalid input",
        )

    url = f"https://brasilapi.com.br/api/cnpj/v1/{digits}"

    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            msg = "not found"
        elif e.code >= 500:
            msg = "server error"
        else:
            msg = f"http {e.code}"
        return CNPJEnrichment(
            cnpj=digits,
            razao_social=None,
            nome_fantasia=None,
            cnae_code=None,
            cnae_description=None,
            status=None,
            endereco=None,
            error=msg,
        )
    except urllib.error.URLError:
        return CNPJEnrichment(
            cnpj=digits,
            razao_social=None,
            nome_fantasia=None,
            cnae_code=None,
            cnae_description=None,
            status=None,
            endereco=None,
            error="timeout",
        )
    except (json.JSONDecodeError, ValueError):
        return CNPJEnrichment(
            cnpj=digits,
            razao_social=None,
            nome_fantasia=None,
            cnae_code=None,
            cnae_description=None,
            status=None,
            endereco=None,
            error="invalid response",
        )

    razao_social = data.get("razao_social")
    nome_fantasia = data.get("nome_fantasia")
    cnae_code = data.get("cnae_codigo")
    cnae_description = data.get("cnae_descricao")
    status = data.get("descricao_situacao_cadastral")
    logradouro = data.get("logradouro")
    numero = data.get("numero")
    bairro = data.get("bairro")
    cidade = data.get("municipio")
    estado = data.get("uf")

    if logradouro or cidade or estado:
        parts = []
        if logradouro:
            parts.append(logradouro)
        if numero and numero != "S/N":
            parts.append(f"N{numero}")
        if bairro:
            parts.append(bairro)
        if cidade:
            parts.append(cidade)
        if estado:
            parts.append(estado)
        endereco = ", ".join(parts)
    else:
        endereco = None

    return CNPJEnrichment(
        cnpj=digits,
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        cnae_code=cnae_code,
        cnae_description=cnae_description,
        status=status,
        endereco=endereco,
        error=None,
    )


def enrich_cep(cep: str, timeout: int = 10) -> CEPEnrichment:
    digits = re.sub(r"\D", "", cep)
    if len(digits) != 8:
        return CEPEnrichment(
            cep=cep,
            logradouro=None,
            bairro=None,
            cidade=None,
            estado=None,
            error="invalid input",
        )

    url = f"https://brasilapi.com.br/api/cep/v2/{digits}"

    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            msg = "not found"
        elif e.code >= 500:
            msg = "server error"
        else:
            msg = f"http {e.code}"
        return CEPEnrichment(
            cep=digits,
            logradouro=None,
            bairro=None,
            cidade=None,
            estado=None,
            error=msg,
        )
    except urllib.error.URLError:
        return CEPEnrichment(
            cep=digits,
            logradouro=None,
            bairro=None,
            cidade=None,
            estado=None,
            error="timeout",
        )
    except (json.JSONDecodeError, ValueError):
        return CEPEnrichment(
            cep=digits,
            logradouro=None,
            bairro=None,
            cidade=None,
            estado=None,
            error="invalid response",
        )

    return CEPEnrichment(
        cep=digits,
        logradouro=data.get("street"),
        bairro=data.get("neighborhood"),
        cidade=data.get("city"),
        estado=data.get("state"),
        error=None,
    )
