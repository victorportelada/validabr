import random
from collections.abc import Callable


def _mod11_check(digits: list[int], weights: list[int]) -> int:
    remainder = sum(d * w for d, w in zip(digits, weights, strict=False)) % 11
    return 0 if remainder < 2 else 11 - remainder


def _rand(n: int) -> list[int]:
    return [random.randint(0, 9) for _ in range(n)]


# ─── Per-state generators ─────────────────────────────────────────────────────


def _gen_ac() -> str:
    base = [0, 1, *_rand(9)]
    c1 = _mod11_check(base, [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    c2 = _mod11_check([*base, c1], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c1, c2])


def _gen_al() -> str:
    base = [2, 4, *_rand(6)]
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_ap() -> str:
    while True:
        base = [0, 3, *_rand(6)]
        n = int("".join(str(x) for x in base))
        if 3_000_001 <= n <= 3_017_000:
            p, d_extra = 5, 0
        elif 3_017_001 <= n <= 5_014_026:
            p, d_extra = 6, 1
        else:
            p, d_extra = 9, 0
        total = sum(x * w for x, w in zip(base, [9, 8, 7, 6, 5, 4, 3, 2], strict=False)) + p
        remainder = total % 11
        check = 11 - remainder
        if check == 10:
            check = 0
        elif check == 11:
            check = d_extra
        return "".join(str(d) for d in [*base, check])


def _gen_am() -> str:
    while True:
        base = _rand(8)
        total = sum(x * w for x, w in zip(base, [9, 8, 7, 6, 5, 4, 3, 2], strict=False))
        if total < 11:
            check = 11 - total
        else:
            remainder = total % 11
            check = 0 if remainder <= 1 else 11 - remainder
        if 0 <= check <= 9:
            return "".join(str(d) for d in [*base, check])


def _gen_ba(digits: int = 9) -> str:
    if digits not in {8, 9}:
        digits = 9
    # First digit determines mod-10 (0,1,2,3,4,5,8) or mod-11 (6,7,9)
    all_first = [0, 1, 2, 3, 4, 5, 8, 6, 7, 9]
    d0 = random.choice(all_first)
    mod_10 = d0 in {0, 1, 2, 3, 4, 5, 8}
    base = [d0, *_rand(digits - 3)]

    def compute_check(subset: list[int], weights: list[int]) -> int:
        total = sum(x * w for x, w in zip(subset, weights, strict=False))
        if mod_10:
            r = total % 10
            return 0 if r == 0 else 10 - r
        r = total % 11
        return 0 if r < 2 else 11 - r

    if digits == 8:
        w_c2, w_c1 = [7, 6, 5, 4, 3, 2], [8, 7, 6, 5, 4, 3, 2]
    else:
        w_c2, w_c1 = [8, 7, 6, 5, 4, 3, 2], [9, 8, 7, 6, 5, 4, 3, 2]

    c2 = compute_check(base, w_c2)
    c1 = compute_check([*base, c2], w_c1)
    return "".join(str(d) for d in [*base, c2, c1])


def _gen_ce() -> str:
    base = _rand(8)
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_df() -> str:
    base = [0, 7, *_rand(9)]
    c1 = _mod11_check(base, [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    c2 = _mod11_check([*base, c1], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c1, c2])


def _gen_es() -> str:
    base = _rand(8)
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_go() -> str:
    prefix = random.choice([10, 11, 15])
    base = [prefix // 10, prefix % 10, *_rand(6)]
    total = sum(x * w for x, w in zip(base, [9, 8, 7, 6, 5, 4, 3, 2], strict=False))
    remainder = total % 11
    check = 0 if remainder == 0 else (1 if remainder == 1 else 11 - remainder)
    return "".join(str(d) for d in [*base, check])


def _gen_ma() -> str:
    base = [1, 2, *_rand(6)]
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_mt() -> str:
    base = _rand(10)
    c = _mod11_check(base, [3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_ms() -> str:
    base = [2, 8, *_rand(6)]
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_mg() -> str:
    base = _rand(11)
    # First check: Luhn-style on 12-digit intermediate
    intermediate = [*base[:3], 0, *base[3:]]
    total = 0
    for x, w in zip(intermediate, [1, 2] * 6, strict=False):
        prod = x * w
        total += prod // 10 + prod % 10
    c1 = (10 - total % 10) % 10
    # Second check: mod-11 with extended weights
    weights2 = [3, 2, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    total2 = sum(x * w for x, w in zip([*base, c1], weights2, strict=False))
    remainder = total2 % 11
    c2 = 0 if remainder < 2 else 11 - remainder
    return "".join(str(d) for d in [*base, c1, c2])


def _gen_pa() -> str:
    base = [1, 5, *_rand(6)]
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_pb() -> str:
    base = _rand(8)
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_pr() -> str:
    base = _rand(8)
    c1 = sum(x * w for x, w in zip(base, [3, 7, 1, 3, 7, 1, 3, 7], strict=False)) % 10
    c2 = sum(x * w for x, w in zip([*base, c1], [7, 1, 3, 7, 1, 3, 7, 1, 3], strict=False)) % 10
    return "".join(str(d) for d in [*base, c1, c2])


def _gen_pe(new_format: bool = False) -> str:
    if new_format:
        base = _rand(12)
        w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        r1 = sum(x * w for x, w in zip(base, w1, strict=False)) % 11
        c1 = 0 if r1 < 2 else 11 - r1
        w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        r2 = sum(x * w for x, w in zip([*base, c1], w2, strict=False)) % 11
        c2 = 0 if r2 < 2 else 11 - r2
        return "".join(str(d) for d in [*base, c1, c2])
    base = _rand(7)
    r1 = sum(x * w for x, w in zip(base, [8, 7, 6, 5, 4, 3, 2], strict=False)) % 11
    c1 = 0 if r1 < 2 else 11 - r1
    r2 = sum(x * w for x, w in zip([*base, c1], [9, 8, 7, 6, 5, 4, 3, 2], strict=False)) % 11
    c2 = 0 if r2 < 2 else 11 - r2
    return "".join(str(d) for d in [*base, c1, c2])


def _gen_pi() -> str:
    base = _rand(8)
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_rj() -> str:
    base = _rand(7)
    total = sum(x * w for x, w in zip(base, [2, 7, 6, 5, 4, 3, 2], strict=False))
    remainder = total % 11
    check = 0 if remainder < 2 else 11 - remainder
    return "".join(str(d) for d in [*base, check])


def _gen_rn(long: bool = False) -> str:
    base = [2, 0, *_rand(6 if not long else 7)]
    if not long:
        c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    else:
        c = _mod11_check(base, [10, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_rs() -> str:
    base = _rand(9)
    c = _mod11_check(base, [2, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_ro(long: bool = True) -> str:
    if long:
        base = _rand(13)
        weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total = sum(x * w for x, w in zip(base, weights, strict=False))
        remainder = total % 11
        check = 0 if remainder < 2 else 11 - remainder
        return "".join(str(d) for d in [*base, check])
    base = _rand(8)
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_rr() -> str:
    base = [2, 4, *_rand(6)]
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_sc() -> str:
    base = _rand(8)
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_sp() -> str:
    while True:
        base = _rand(8)
        c1 = sum(x * w for x, w in zip(base, [1, 3, 2, 9, 7, 13, 4, 5], strict=False)) % 11
        if c1 > 9:
            continue  # discard; no single-digit representation
        middle = _rand(2)
        w2 = [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        total2 = sum(x * w for x, w in zip([*base, c1, *middle], w2, strict=False))
        r2 = total2 % 11
        c2 = 0 if r2 < 2 else 11 - r2
        return "".join(str(d) for d in [*base, c1, *middle, c2])


def _gen_se() -> str:
    base = _rand(8)
    c = _mod11_check(base, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in [*base, c])


def _gen_to() -> str:
    # Positions 2 and 3 are a year indicator (can be anything 0-99)
    prefix = _rand(2)
    year = _rand(2)
    suffix = _rand(6)
    base_for_check = prefix + suffix  # skip year digits in check computation
    c = _mod11_check(base_for_check, [9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(d) for d in prefix + year + suffix + [c])


# ─── Dispatch table ───────────────────────────────────────────────────────────

_GENERATORS: dict[str, Callable[[], str]] = {
    "AC": _gen_ac,
    "AL": _gen_al,
    "AP": _gen_ap,
    "AM": _gen_am,
    "BA": _gen_ba,
    "CE": _gen_ce,
    "DF": _gen_df,
    "ES": _gen_es,
    "GO": _gen_go,
    "MA": _gen_ma,
    "MT": _gen_mt,
    "MS": _gen_ms,
    "MG": _gen_mg,
    "PA": _gen_pa,
    "PB": _gen_pb,
    "PR": _gen_pr,
    "PE": _gen_pe,
    "PI": _gen_pi,
    "RJ": _gen_rj,
    "RN": _gen_rn,
    "RS": _gen_rs,
    "RO": _gen_ro,
    "RR": _gen_rr,
    "SC": _gen_sc,
    "SP": _gen_sp,
    "SE": _gen_se,
    "TO": _gen_to,
}

_VALID_STATES = frozenset(_GENERATORS)


# ─── Public API ───────────────────────────────────────────────────────────────


def generate_ie(state: str) -> str:
    """
    Generates a valid random Inscrição Estadual for the given state.

    Args:
        state: Two-letter state code (e.g. "SP", "MG", "RJ").

    Returns:
        A string of digits representing a valid IE for that state.

    Raises:
        ValueError: If the state code is not recognized.
    """
    state = state.upper().strip()
    if state not in _VALID_STATES:
        raise ValueError(f"Unknown state code: {state!r}")
    return _GENERATORS[state]()
