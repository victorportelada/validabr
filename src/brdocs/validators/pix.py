import re
from enum import Enum


class PixKeyType(Enum):
    CPF = "CPF"
    CNPJ = "CNPJ"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    EVP = "EVP"


def classify_pix(key: str) -> PixKeyType | None:
    """
    Classifies a Pix key according to Banco Central do Brasil patterns.

    Supported types:
        CPF: 11 digits matching CPF algorithm
        CNPJ: 14 digits matching CNPJ algorithm
        EMAIL: RFC-compatible email address
        PHONE: +55 followed by 10 or 11 digits (DDD + number)
        EVP: UUID v4 format (xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx)

    Returns:
        PixKeyType if the key matches a known pattern, None otherwise.
    """
    if not isinstance(key, str):
        return None

    cleaned = key.strip()

    if _is_valid_evp(cleaned):
        return PixKeyType.EVP

    if _is_valid_phone(cleaned):
        return PixKeyType.PHONE

    if _is_valid_email(cleaned):
        return PixKeyType.EMAIL

    try:
        from brdocs.validators import is_valid_cnpj, is_valid_cpf
    except ImportError:
        return None

    digits = re.sub(r"\D", "", cleaned)

    if len(digits) == 11 and is_valid_cpf(digits):
        return PixKeyType.CPF

    if len(digits) == 14 and is_valid_cnpj(digits):
        return PixKeyType.CNPJ

    return None


def _is_valid_evp(value: str) -> bool:
    pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    return bool(re.match(pattern, value, re.IGNORECASE))


def _is_valid_phone(value: str) -> bool:
    if not value.startswith("+55"):
        return False
    digits = re.sub(r"\D", "", value)
    return len(digits) == 12 or len(digits) == 13


def _is_valid_email(value: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, value))
