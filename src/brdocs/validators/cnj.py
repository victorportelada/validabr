import re


def is_valid_cnj(cnj: str) -> bool:
    """
    Validates a Brazilian Processo CNJ number (Resolução CNJ nº 65/2008).

    Accepts formatted (NNNNNNN-DD.AAAA.J.TT.OOOO) and unformatted
    (20 contiguous digits) strings.

    The check uses ISO 7064 mod 97: with DD replaced by '00', the resulting
    20-digit integer mod 97 gives a remainder R, and DD must equal 98 - R.
    """
    if not isinstance(cnj, str):
        return False

    digits = re.sub(r"\D", "", cnj)

    if len(digits) != 20:
        return False

    nnnnnnn = digits[0:7]
    dd = digits[7:9]
    aaaa = digits[9:13]
    j = digits[13:14]
    tt = digits[14:16]
    oooo = digits[16:20]

    base = nnnnnnn + "00" + aaaa + j + tt + oooo
    remainder = int(base) % 97
    expected_dd = 98 - remainder

    return int(dd) == expected_dd
