import re
from collections.abc import Callable

_VALID_STATES = frozenset(
    [
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    ]
)


def _clean(ie: str) -> str:
    return re.sub(r"\D", "", ie)


def _mod11(digits: list[int], weights: list[int]) -> int:
    """Compute mod-11 check digit; maps remainder 0 or 1 to 0."""
    remainder = sum(d * w for d, w in zip(digits, weights, strict=False)) % 11
    return 0 if remainder < 2 else 11 - remainder


# ─── Per-state validators ─────────────────────────────────────────────────────


def _ac(d: list[int]) -> bool:
    if len(d) != 13 or d[0] != 0 or d[1] != 1:
        return False
    c1 = _mod11(d[:11], [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    c2 = _mod11(d[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return d[11] == c1 and d[12] == c2


def _al(d: list[int]) -> bool:
    if len(d) != 9 or d[0] != 2 or d[1] != 4:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _ap(d: list[int]) -> bool:
    if len(d) != 9 or d[0] != 0 or d[1] != 3:
        return False
    n = int("".join(str(x) for x in d[:8]))
    if 3_000_001 <= n <= 3_017_000:
        p, d_extra = 5, 0
    elif 3_017_001 <= n <= 5_014_026:
        p, d_extra = 6, 1
    else:
        p, d_extra = 9, 0
    total = sum(x * w for x, w in zip(d[:8], [9, 8, 7, 6, 5, 4, 3, 2], strict=False)) + p
    remainder = total % 11
    check = 11 - remainder
    if check == 10:
        check = 0
    elif check == 11:
        check = d_extra
    return d[8] == check


def _am(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    total = sum(x * w for x, w in zip(d[:8], [9, 8, 7, 6, 5, 4, 3, 2], strict=False))
    if total < 11:
        check = 11 - total
    else:
        remainder = total % 11
        check = 0 if remainder <= 1 else 11 - remainder
    return d[8] == check


def _ba(d: list[int]) -> bool:
    if len(d) == 8:
        w_c2, w_c1 = [7, 6, 5, 4, 3, 2], [8, 7, 6, 5, 4, 3, 2]
        base_len = 6
    elif len(d) == 9:
        w_c2, w_c1 = [8, 7, 6, 5, 4, 3, 2], [9, 8, 7, 6, 5, 4, 3, 2]
        base_len = 7
    else:
        return False

    mod_10 = d[0] in {0, 1, 2, 3, 4, 5, 8}

    def _check(digits: list[int], weights: list[int]) -> int:
        total = sum(x * w for x, w in zip(digits, weights, strict=False))
        if mod_10:
            remainder = total % 10
            return 0 if remainder == 0 else 10 - remainder
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    c2 = _check(d[:base_len], w_c2)
    c1 = _check(d[: base_len + 1], w_c1)
    return d[-2] == c2 and d[-1] == c1


def _ce(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _df(d: list[int]) -> bool:
    if len(d) != 13 or d[0] != 0 or d[1] != 7:
        return False
    c1 = _mod11(d[:11], [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    c2 = _mod11(d[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return d[11] == c1 and d[12] == c2


def _es(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _go(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    prefix = d[0] * 10 + d[1]
    if prefix not in {10, 11, 15}:
        return False
    total = sum(x * w for x, w in zip(d[:8], [9, 8, 7, 6, 5, 4, 3, 2], strict=False))
    remainder = total % 11
    # GO: remainder 1 maps to check digit 1 (not 0 like other states)
    if remainder == 0:
        check = 0
    elif remainder == 1:
        check = 1
    else:
        check = 11 - remainder
    return d[8] == check


def _ma(d: list[int]) -> bool:
    if len(d) != 9 or d[0] != 1 or d[1] != 2:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _mt(d: list[int]) -> bool:
    if len(d) != 11:
        return False
    return d[10] == _mod11(d[:10], [3, 2, 9, 8, 7, 6, 5, 4, 3, 2])


def _ms(d: list[int]) -> bool:
    if len(d) != 9 or d[0] != 2 or d[1] != 8:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _mg(d: list[int]) -> bool:
    if len(d) != 13:
        return False
    # First check (d[11]): Luhn-style on 12-digit intermediate
    base = d[:11]
    intermediate = [*base[:3], 0, *base[3:]]  # insert 0 at position 3
    total = 0
    for x, w in zip(intermediate, [1, 2] * 6, strict=False):
        prod = x * w
        total += prod // 10 + prod % 10
    c1 = (10 - total % 10) % 10
    if d[11] != c1:
        return False
    # Second check (d[12]): standard mod-11 with extended weights
    weights2 = [3, 2, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    total2 = sum(x * w for x, w in zip(d[:12], weights2, strict=False))
    remainder = total2 % 11
    c2 = 0 if remainder < 2 else 11 - remainder
    return d[12] == c2


def _pa(d: list[int]) -> bool:
    if len(d) != 9 or d[0] != 1 or d[1] != 5:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _pb(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _pr(d: list[int]) -> bool:
    if len(d) != 10:
        return False
    c1 = sum(x * w for x, w in zip(d[:8], [3, 7, 1, 3, 7, 1, 3, 7], strict=False)) % 10
    c2 = sum(x * w for x, w in zip(d[:9], [7, 1, 3, 7, 1, 3, 7, 1, 3], strict=False)) % 10
    return d[8] == c1 and d[9] == c2


def _pe(d: list[int]) -> bool:
    if len(d) == 9:
        # Old format: two check digits at positions 7 and 8
        r1 = sum(x * w for x, w in zip(d[:7], [8, 7, 6, 5, 4, 3, 2], strict=False)) % 11
        c1 = 0 if r1 < 2 else 11 - r1
        if d[7] != c1:
            return False
        r2 = sum(x * w for x, w in zip(d[:8], [9, 8, 7, 6, 5, 4, 3, 2], strict=False)) % 11
        c2 = 0 if r2 < 2 else 11 - r2
        return d[8] == c2
    if len(d) == 14:
        # New format: CNPJ-style check digits
        w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        r1 = sum(x * w for x, w in zip(d[:12], w1, strict=False)) % 11
        c1 = 0 if r1 < 2 else 11 - r1
        if d[12] != c1:
            return False
        w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        r2 = sum(x * w for x, w in zip(d[:13], w2, strict=False)) % 11
        c2 = 0 if r2 < 2 else 11 - r2
        return d[13] == c2
    return False


def _pi(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _rj(d: list[int]) -> bool:
    if len(d) != 8:
        return False
    total = sum(x * w for x, w in zip(d[:7], [2, 7, 6, 5, 4, 3, 2], strict=False))
    remainder = total % 11
    check = 0 if remainder < 2 else 11 - remainder
    return d[7] == check


def _rn(d: list[int]) -> bool:
    if d[0] != 2 or d[1] != 0:
        return False
    if len(d) == 9:
        return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])
    if len(d) == 10:
        return d[9] == _mod11(d[:9], [10, 9, 8, 7, 6, 5, 4, 3, 2])
    return False


def _rs(d: list[int]) -> bool:
    if len(d) != 10:
        return False
    return d[9] == _mod11(d[:9], [2, 9, 8, 7, 6, 5, 4, 3, 2])


def _ro(d: list[int]) -> bool:
    if len(d) == 14:
        weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total = sum(x * w for x, w in zip(d[:13], weights, strict=False))
        remainder = total % 11
        check = 0 if remainder < 2 else 11 - remainder
        return d[13] == check
    if len(d) == 9:
        # Old format uses last 5 digits + 2-digit municipality code
        total = sum(x * w for x, w in zip(d[:8], [9, 8, 7, 6, 5, 4, 3, 2], strict=False))
        remainder = total % 11
        check = 0 if remainder < 2 else 11 - remainder
        return d[8] == check
    return False


def _rr(d: list[int]) -> bool:
    if len(d) != 9 or d[0] != 2 or d[1] != 4:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _sc(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _sp(d: list[int]) -> bool:
    if len(d) != 12:
        return False
    # First check (d[8]): remainder mod 11 is used directly
    c1 = sum(x * w for x, w in zip(d[:8], [1, 3, 2, 9, 7, 13, 4, 5], strict=False)) % 11
    if d[8] != c1:
        return False
    # Second check (d[11]): mod-11 with extended weights
    total2 = sum(x * w for x, w in zip(d[:11], [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2], strict=False))
    remainder2 = total2 % 11
    c2 = 0 if remainder2 < 2 else 11 - remainder2
    return d[11] == c2


def _se(d: list[int]) -> bool:
    if len(d) != 9:
        return False
    return d[8] == _mod11(d[:8], [9, 8, 7, 6, 5, 4, 3, 2])


def _to(d: list[int]) -> bool:
    if len(d) != 11:
        return False
    # Positions 2 and 3 (year indicator) are skipped in the check calculation
    base = d[:2] + d[4:10]  # 8 digits
    return d[10] == _mod11(base, [9, 8, 7, 6, 5, 4, 3, 2])


# ─── Dispatch table ───────────────────────────────────────────────────────────

_VALIDATORS: dict[str, Callable[[list[int]], bool]] = {
    "AC": _ac,
    "AL": _al,
    "AP": _ap,
    "AM": _am,
    "BA": _ba,
    "CE": _ce,
    "DF": _df,
    "ES": _es,
    "GO": _go,
    "MA": _ma,
    "MT": _mt,
    "MS": _ms,
    "MG": _mg,
    "PA": _pa,
    "PB": _pb,
    "PR": _pr,
    "PE": _pe,
    "PI": _pi,
    "RJ": _rj,
    "RN": _rn,
    "RS": _rs,
    "RO": _ro,
    "RR": _rr,
    "SC": _sc,
    "SP": _sp,
    "SE": _se,
    "TO": _to,
}


# ─── Public API ───────────────────────────────────────────────────────────────


def is_valid_ie(ie: str, state: str) -> bool:
    """
    Validates a Brazilian Inscrição Estadual (State Tax Registration).

    Args:
        ie: The IE string. May contain punctuation (dots, slashes, hyphens).
        state: Two-letter state code (e.g. "SP", "MG", "RJ").

    Returns:
        True if the IE is valid for the given state, False otherwise.
    """
    if not isinstance(ie, str) or not isinstance(state, str):
        return False

    state = state.upper().strip()
    if state not in _VALID_STATES:
        return False

    cleaned = _clean(ie)
    if not cleaned:
        return False

    digits = [int(c) for c in cleaned]
    validator = _VALIDATORS[state]
    return validator(digits)
