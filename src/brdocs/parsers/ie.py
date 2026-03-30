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

# States that accept more than one digit count
_DUAL_LENGTH: dict[str, tuple[int, ...]] = {
    "BA": (8, 9),
    "PE": (9, 14),
    "RN": (9, 10),
    "RO": (9, 14),
}

# Single accepted length for all other states
_SINGLE_LENGTH: dict[str, int] = {
    "AC": 13,
    "AL": 9,
    "AP": 9,
    "AM": 9,
    "CE": 9,
    "DF": 13,
    "ES": 9,
    "GO": 9,
    "MA": 9,
    "MT": 11,
    "MS": 9,
    "MG": 13,
    "PA": 9,
    "PB": 9,
    "PR": 10,
    "PE": 9,
    "PI": 9,
    "RJ": 8,
    "RN": 9,
    "RS": 10,
    "RR": 9,
    "SC": 9,
    "SP": 12,
    "SE": 9,
    "TO": 11,
}


def _raw(d: str) -> str:
    return d


def _fmt_ac_df(d: str) -> str:  # XXX.XXX.XXX/XXX-XX  (13 digits)
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}/{d[9:12]}-{d[12:]}"


def _fmt_am(d: str) -> str:  # XX.XXX.XXX-X  (9 digits)
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}-{d[8]}"


def _fmt_ba_8(d: str) -> str:  # XXXXXX-XX  (8 digits)
    return f"{d[:6]}-{d[6:]}"


def _fmt_ba_9(d: str) -> str:  # XXXXXXX-XX  (9 digits)
    return f"{d[:7]}-{d[7:]}"


def _fmt_ce_go_rn9(d: str) -> str:  # XX.XXX.XXX-X  (9 digits)
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}-{d[8]}"


def _fmt_mg(d: str) -> str:  # XXX.XXX.XXX/XXXX  (13 digits)
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}/{d[9:]}"


def _fmt_pa(d: str) -> str:  # XX-XXXXXX-X  (9 digits)
    return f"{d[:2]}-{d[2:8]}-{d[8]}"


def _fmt_pr(d: str) -> str:  # XXX.XXXXX-XX  (10 digits)
    return f"{d[:3]}.{d[3:8]}-{d[8:]}"


def _fmt_pe_9(d: str) -> str:  # XXXXXXX-XX  (9 digits)
    return f"{d[:7]}-{d[7:]}"


def _fmt_pe_14(d: str) -> str:  # XX.X.XXX.XXXXXXX-X  (14 digits)
    return f"{d[:2]}.{d[2]}.{d[3:6]}.{d[6:13]}-{d[13]}"


def _fmt_rj(d: str) -> str:  # XX.XXX.XX-X  (8 digits)
    return f"{d[:2]}.{d[2:5]}.{d[5:7]}-{d[7]}"


def _fmt_rn10(d: str) -> str:  # XX.XXX.XXX.X-X  (10 digits)
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}.{d[8]}-{d[9]}"


def _fmt_rs(d: str) -> str:  # XXX/XXXXXXX  (10 digits)
    return f"{d[:3]}/{d[3:]}"


def _fmt_sc(d: str) -> str:  # XXX.XXX.XXX  (9 digits)
    return f"{d[:3]}.{d[3:6]}.{d[6:]}"


def _fmt_sp(d: str) -> str:  # XXX.XXX.XXX.XXX  (12 digits)
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}.{d[9:]}"


# Dispatch: state → {length → formatter}
_FORMATTERS: dict[str, dict[int, Callable[[str], str]]] = {
    "AC": {13: _fmt_ac_df},
    "AL": {9: _raw},
    "AP": {9: _raw},
    "AM": {9: _fmt_am},
    "BA": {8: _fmt_ba_8, 9: _fmt_ba_9},
    "CE": {9: _fmt_ce_go_rn9},
    "DF": {13: _fmt_ac_df},
    "ES": {9: _raw},
    "GO": {9: _fmt_ce_go_rn9},
    "MA": {9: _raw},
    "MT": {11: _raw},
    "MS": {9: _raw},
    "MG": {13: _fmt_mg},
    "PA": {9: _fmt_pa},
    "PB": {9: _raw},
    "PR": {10: _fmt_pr},
    "PE": {9: _fmt_pe_9, 14: _fmt_pe_14},
    "PI": {9: _raw},
    "RJ": {8: _fmt_rj},
    "RN": {9: _fmt_ce_go_rn9, 10: _fmt_rn10},
    "RS": {10: _fmt_rs},
    "RO": {9: _raw, 14: _raw},
    "RR": {9: _raw},
    "SC": {9: _fmt_sc},
    "SP": {12: _fmt_sp},
    "SE": {9: _raw},
    "TO": {11: _raw},
}


def format_ie(ie: str, state: str) -> str:
    """
    Formats an IE (Inscrição Estadual) string to the canonical pattern for the
    given Brazilian state.

    Accepts raw digit strings or already-formatted strings (punctuation is stripped
    before formatting). State codes are case-insensitive (e.g. "sp", "SP", "Sp").

    Args:
        ie: The IE string to format.
        state: Two-letter state abbreviation (e.g. "SP", "MG").

    Returns:
        The IE formatted according to the canonical SEFAZ convention for the state.
        States without a canonical punctuation pattern return raw digits.

    Raises:
        ValueError: if ie or state is not a str, if the state code is unknown,
                    or if the digit count does not match the expected length(s).
    """
    if not isinstance(ie, str):
        raise ValueError(f"Expected str, got {type(ie).__name__}")
    if not isinstance(state, str):
        raise ValueError(f"Expected str, got {type(state).__name__}")

    state = state.upper().strip()

    if state not in _VALID_STATES:
        raise ValueError(f"Unknown state code: '{state}'")

    digits = re.sub(r"\D", "", ie)
    n = len(digits)

    formatters = _FORMATTERS[state]

    if n not in formatters:
        accepted = sorted(formatters)
        if len(accepted) == 1:
            raise ValueError(f"IE for {state} must have {accepted[0]} digits, got {n}")
        lengths = " or ".join(str(x) for x in accepted)
        raise ValueError(f"IE for {state} must have {lengths} digits, got {n}")

    return formatters[n](digits)
