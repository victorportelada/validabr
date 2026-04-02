import random
import re

_VALID_CUF = frozenset(
    {
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        31,
        32,
        33,
        35,
        41,
        42,
        43,
        50,
        51,
        52,
        53,
    }
)
_VALID_MOD = frozenset({55, 57, 58, 65})


def _compute_check_digit(digits: str) -> int:
    total = sum(int(digits[i]) * [2, 3, 4, 5, 6, 7, 8, 9][(42 - i) % 8] for i in range(43))
    remainder = total % 11
    return 1 if remainder <= 1 else 11 - remainder


def generate_nfe(
    cuf: int,
    cnpj: str,
    aamm: str,
    serie: int = 1,
    nnf: int = 1,
    mod: int = 55,
    tp_emis: int = 1,
    formatted: bool = False,
) -> str:
    """
    Generates a valid 44-digit NFe/CTe/NFC-e/MDF-e access key (chave de acesso).

    Args:
        cuf: IBGE state code. Must be in the valid set. Raises ValueError otherwise.
        cnpj: Emitter CNPJ as a 14-digit string (formatted or raw).
              Raises ValueError if not 14 digits after stripping.
        aamm: 4-character "YYMM" string (e.g. "2404"). Must match r"^\\d{4}$".
              Raises ValueError otherwise.
        serie: Invoice series, 0-999. Defaults to 1.
        nnf: Invoice number, 1-999_999_999. Defaults to 1.
        mod: Document model. Must be in {55, 57, 58, 65}.
             55=NF-e, 65=NFC-e, 57=CT-e, 58=MDF-e. Defaults to 55.
        tp_emis: Emission type, 1-9. Defaults to 1 (normal).
        formatted: If True, returns in grouped format
                   "XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXX"
                   (8 groups of 5 + 1 group of 4).

    Returns:
        A 44-character string representing a valid access key.

    Raises:
        ValueError: if cUF, mod, aamm, or CNPJ are invalid.
    """
    if cuf not in _VALID_CUF:
        raise ValueError(f"cUF must be one of {_VALID_CUF}, got {cuf}")

    if not isinstance(aamm, str) or not re.fullmatch(r"\d{4}", aamm):
        raise ValueError(f"aamm must be a 4-digit string like '2404', got {aamm!r}")

    cnpj_digits = re.sub(r"\D", "", cnpj)
    if len(cnpj_digits) != 14:
        raise ValueError(f"CNPJ must have 14 digits, got {len(cnpj_digits)}")

    if mod not in _VALID_MOD:
        raise ValueError(f"mod must be one of {_VALID_MOD}, got {mod}")

    if not (0 <= serie <= 999):
        raise ValueError(f"serie must be 0-999, got {serie}")

    if not (1 <= nnf <= 999_999_999):
        raise ValueError(f"nnf must be 1-999_999_999, got {nnf}")

    if not (1 <= tp_emis <= 9):
        raise ValueError(f"tp_emis must be 1-9, got {tp_emis}")

    cnf = random.randint(1, 99_999_999)

    key = f"{cuf:02d}{aamm}{cnpj_digits}{mod:02d}{serie:03d}{nnf:09d}{tp_emis}{cnf:08d}"

    cdv = _compute_check_digit(key)
    raw = f"{key}{cdv}"

    if formatted:
        groups = [raw[i * 5 : (i + 1) * 5] for i in range(8)]
        groups.append(raw[40:44])
        return " ".join(groups)

    return raw
