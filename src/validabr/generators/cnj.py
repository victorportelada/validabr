import random

# Justice segments: 1=STF, 2=CNJ, 3=STJ, 4=Justiça Federal, 5=TRT,
# 6=TRE, 7=TRM, 8=TJSP-style (state courts), 9=CSJT
_JUSTICE_SEGMENTS = list(range(1, 10))


def generate_cnj(formatted: bool = True) -> str:
    """
    Generates a valid random Brazilian Processo CNJ number.

    Args:
        formatted: If True, returns in NNNNNNN-DD.AAAA.J.TT.OOOO format.
                   If False, returns 20 contiguous digits.

    Returns:
        A valid Processo CNJ string.
    """
    nnnnnnn = str(random.randint(1, 9999999)).zfill(7)
    aaaa = str(random.randint(2000, 2030))
    j = str(random.choice(_JUSTICE_SEGMENTS))
    tt = str(random.randint(1, 99)).zfill(2)
    oooo = str(random.randint(0, 9999)).zfill(4)

    base = nnnnnnn + "00" + aaaa + j + tt + oooo
    remainder = int(base) % 97
    dd = str(98 - remainder).zfill(2)

    if formatted:
        return f"{nnnnnnn}-{dd}.{aaaa}.{j}.{tt}.{oooo}"
    return nnnnnnn + dd + aaaa + j + tt + oooo
