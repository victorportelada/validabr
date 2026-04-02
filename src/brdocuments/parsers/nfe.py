import re
from typing import NamedTuple


class NFEData(NamedTuple):
    uf_code: str
    year_month: str
    cnpj: str
    model: str
    series: str
    number: str
    emission_type: str
    random_code: str
    check_digit: str


def parse_nfe(key: str) -> NFEData:
    """
    Decomposes a 44-digit NFe/CTe/MDFe access key into its semantic parts.

    Layout (44 digits):
        [0:2]   - UF code (2 digits)
        [2:6]   - Year and month (YYMM, 4 digits)
        [6:20]  - CNPJ (14 digits)
        [20:22] - Model (2 digits: 55=NFe, 57=CTe, 58=MDFe)
        [22:25] - Series (3 digits)
        [25:34] - Number (9 digits)
        [34:35] - Emission type (1 digit)
        [35:43] - Random code (8 digits)
        [43:44] - Check digit (1 digit)

    Raises:
        ValueError: if input is not a str or does not contain exactly 44 digits.
    """
    if not isinstance(key, str):
        raise ValueError(f"Expected str, got {type(key).__name__}")

    digits = re.sub(r"\D", "", key)

    if len(digits) != 44:
        raise ValueError(f"NFe key must have 44 digits, got {len(digits)}")

    return NFEData(
        uf_code=digits[0:2],
        year_month=digits[2:6],
        cnpj=digits[6:20],
        model=digits[20:22],
        series=digits[22:25],
        number=digits[25:34],
        emission_type=digits[34:35],
        random_code=digits[35:43],
        check_digit=digits[43:44],
    )


def format_nfe(key: str) -> str:
    """
    Formats a NFe/CTe/MDFe access key to its canonical grouped format.

    Format: XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXX
            (8 groups of 5 + 1 group of 4)

    Raises:
        ValueError: if the input does not contain exactly 44 digits.
    """
    if not isinstance(key, str):
        raise ValueError(f"Expected str, got {type(key).__name__}")

    digits = re.sub(r"\D", "", key)

    if len(digits) != 44:
        raise ValueError(f"NFe key must have 44 digits, got {len(digits)}")

    groups = [digits[i * 5 : (i + 1) * 5] for i in range(8)]
    groups.append(digits[40:44])
    return " ".join(groups)
