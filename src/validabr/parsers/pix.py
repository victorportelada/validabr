import re
from typing import NamedTuple

from validabr.parsers.cnpj import CNPJData
from validabr.parsers.cnpj import format_cnpj as _format_cnpj
from validabr.parsers.cnpj import parse_cnpj as _parse_cnpj
from validabr.parsers.cpf import CPFData
from validabr.parsers.cpf import format_cpf as _format_cpf
from validabr.parsers.cpf import parse_cpf as _parse_cpf
from validabr.validators.pix import PixKeyType, classify_pix


class PixPhoneData(NamedTuple):
    country_code: str
    area_code: str
    number: str
    raw: str


class PixEmailData(NamedTuple):
    local: str
    domain: str
    normalized: str


class PixEVPData(NamedTuple):
    uuid: str


def format_pix(key: str) -> str:
    """
    Formats a PIX key to its canonical representation.

    Uses classify_pix internally to determine the key type, then formats
    according to PIX standards:
        CPF     → NNN.NNN.NNN-NN
        CNPJ    → NN.NNN.NNN/NNNN-NN
        PHONE   → +55 (DD) NNNNN-NNNN or +55 (DD) NNNN-NNNN
        EMAIL   → lowercase email (unchanged)
        EVP     → lowercase UUID with hyphens

    Raises:
        ValueError: if the key is not a valid PIX key.
    """
    key_type = classify_pix(key)
    if key_type is None:
        raise ValueError(f"Invalid PIX key: {key!r}")

    if key_type == PixKeyType.CPF:
        digits = re.sub(r"\D", "", key)
        return _format_cpf(digits)

    if key_type == PixKeyType.CNPJ:
        cleaned = re.sub(r"[\s.\/-]", "", key).upper()
        return _format_cnpj(cleaned)

    if key_type == PixKeyType.PHONE:
        digits = re.sub(r"\D", "", key)
        area_code = digits[2:4]
        number = digits[4:]
        if len(number) == 9:
            return f"+55 ({area_code}) {number[:5]}-{number[5:]}"
        return f"+55 ({area_code}) {number[:4]}-{number[4:]}"

    if key_type == PixKeyType.EMAIL:
        return key.strip().lower()

    if key_type == PixKeyType.EVP:
        return key.strip().lower()

    raise ValueError(f"Invalid PIX key: {key!r}")


def parse_pix(key: str) -> CPFData | CNPJData | PixPhoneData | PixEmailData | PixEVPData:
    """
    Parses a PIX key into its typed semantic representation.

    Uses classify_pix internally to determine the key type, then dispatches
    to the appropriate parser:
        CPF    → strips non-digits, calls parse_cpf, returns CPFData
        CNPJ   → strips formatting, calls parse_cnpj, returns CNPJData
        PHONE  → extracts country_code="55", area_code (first 2 after +55),
                 number (remaining 8 or 9 digits), returns PixPhoneData
        EMAIL  → splits on @, returns PixEmailData with normalized lowercase
        EVP    → returns PixEVPData(uuid=key.strip().lower())

    Raises:
        ValueError: if the key is not a valid PIX key.
    """
    key_type = classify_pix(key)
    if key_type is None:
        raise ValueError(f"Invalid PIX key: {key!r}")

    if key_type == PixKeyType.CPF:
        digits = re.sub(r"\D", "", key)
        return _parse_cpf(digits)

    if key_type == PixKeyType.CNPJ:
        cleaned = re.sub(r"[\s.\/-]", "", key).upper()
        return _parse_cnpj(cleaned)

    if key_type == PixKeyType.PHONE:
        digits = re.sub(r"\D", "", key)
        country_code = digits[:2]
        area_code = digits[2:4]
        number = digits[4:]
        raw = f"+{digits}"
        return PixPhoneData(
            country_code=country_code,
            area_code=area_code,
            number=number,
            raw=raw,
        )

    if key_type == PixKeyType.EMAIL:
        local, domain = key.strip().lower().split("@", 1)
        return PixEmailData(
            local=local,
            domain=domain,
            normalized=f"{local}@{domain}",
        )

    if key_type == PixKeyType.EVP:
        return PixEVPData(uuid=key.strip().lower())

    raise ValueError(f"Invalid PIX key: {key!r}")
