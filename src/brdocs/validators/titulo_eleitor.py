import re

_WEIGHTS_SEQ = [2, 3, 4, 5, 6, 7, 8, 9]
_SP_MG_STATES = {1, 2}


def is_valid_titulo_eleitor(titulo: str) -> bool:
    """
    Validates a Brazilian Título de Eleitor (voter registration number).

    The 12-digit number is structured as:
      SSSSSSSS EE V1 V2
      - SSSSSSSS: 8-digit sequential number
      - EE: 2-digit state code (01-28)
      - V1, V2: two check digits (mod 11)

    SP (01) and MG (02) use a different rule for V2: when the remainder is 0,
    V2 = 1 instead of 0.
    """
    if not isinstance(titulo, str):
        return False

    digits = re.sub(r"\D", "", titulo)

    if len(digits) != 12:
        return False

    seq = [int(d) for d in digits[:8]]
    state_code = int(digits[8:10])
    v1 = int(digits[10])
    v2 = int(digits[11])

    if state_code == 0 or state_code > 28:
        return False

    # First check digit
    r1 = sum(d * w for d, w in zip(seq, _WEIGHTS_SEQ, strict=False)) % 11

    if state_code in _SP_MG_STATES:
        if r1 == 0:
            expected_v1 = 0
        elif r1 == 1:
            return False  # no valid title can have this sequential for SP/MG
        else:
            expected_v1 = 11 - r1
    else:
        expected_v1 = 0 if r1 < 2 else 11 - r1

    if v1 != expected_v1:
        return False

    # Second check digit
    e1, e2 = state_code // 10, state_code % 10
    r2 = (e1 * 7 + e2 * 8 + v1 * 9) % 11

    if state_code in _SP_MG_STATES:
        expected_v2 = 1 if r2 == 0 else 11 - r2
    else:
        expected_v2 = 0 if r2 < 2 else 11 - r2

    return v2 == expected_v2
