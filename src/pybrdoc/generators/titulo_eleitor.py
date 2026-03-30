import random

_WEIGHTS_SEQ = [2, 3, 4, 5, 6, 7, 8, 9]
_SP_MG_STATES = {1, 2}
_VALID_STATE_CODES = list(range(1, 29))


def generate_titulo_eleitor(state_code: int | None = None) -> str:
    """
    Generates a valid random Brazilian Título de Eleitor (12 digits).

    Args:
        state_code: TSE state code (1-28). Randomly chosen if not provided.

    Returns:
        A valid 12-digit Título de Eleitor string.
    """
    if state_code is None:
        state_code = random.choice(_VALID_STATE_CODES)

    if state_code not in range(1, 29):
        raise ValueError(f"Invalid state_code {state_code}: must be 1-28")

    while True:
        seq = [random.randint(0, 9) for _ in range(8)]
        r1 = sum(d * w for d, w in zip(seq, _WEIGHTS_SEQ, strict=False)) % 11

        if state_code in _SP_MG_STATES:
            if r1 == 0:
                v1 = 0
            elif r1 == 1:
                continue  # no valid check digit — regenerate
            else:
                v1 = 11 - r1
        else:
            v1 = 0 if r1 < 2 else 11 - r1

        e1, e2 = state_code // 10, state_code % 10
        r2 = (e1 * 7 + e2 * 8 + v1 * 9) % 11

        if state_code in _SP_MG_STATES:
            v2 = 1 if r2 == 0 else 11 - r2
        else:
            v2 = 0 if r2 < 2 else 11 - r2

        if v2 >= 10:
            continue  # edge case — regenerate

        seq_str = "".join(str(d) for d in seq)
        return f"{seq_str}{state_code:02d}{v1}{v2}"
