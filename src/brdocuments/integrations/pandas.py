"""Pandas Series accessor for brdocuments.

Requires pandas to be installed:
    pip install pandas

Usage:
    import pandas as pd
    import brdocuments.integrations.pandas  # registers accessor
    df["cpf"].brdocuments.is_valid_cpf()          # returns bool Series
    df["cnpj"].brdocuments.is_valid_cnpj()        # returns bool Series
    df["cpf"].brdocuments.format_cpf()             # returns str Series
    df["cpf"].brdocuments.mask_cpf()              # returns str Series
    df["cnpj"].brdocuments.format_cnpj()          # returns str Series
    df["cnpj"].brdocuments.mask_cnpj()            # returns str Series
    df["ie"].brdocuments.is_valid_ie("SP")       # returns bool Series
    df["ie"].brdocuments.format_ie("SP")         # returns str Series
    df["cep"].brdocuments.is_valid_cep()          # returns bool Series
    df["cep"].brdocuments.format_cep()            # returns str Series
    df["cnh"].brdocuments.is_valid_cnh()         # returns bool Series
    df["cnh"].brdocuments.format_cnh()           # returns str Series
    df["pis"].brdocuments.is_valid_pis()         # returns bool Series
    df["pis"].brdocuments.format_pis()           # returns str Series
    df["renavam"].brdocuments.is_valid_renavam()  # returns bool Series
    df["renavam"].brdocuments.format_renavam()   # returns str Series
    df["titulo"].brdocuments.is_valid_titulo_eleitor()  # returns bool Series
    df["titulo"].brdocuments.format_titulo_eleitor()   # returns str Series
    df["cnj"].brdocuments.is_valid_cnj()          # returns bool Series
    df["cnj"].brdocuments.format_cnj()           # returns str Series
    df["nfe"].brdocuments.is_valid_nfe()         # returns bool Series
    df["nfe"].brdocuments.format_nfe()           # returns str Series
    df["pix"].brdocuments.classify_pix()          # returns str Series
"""

from __future__ import annotations

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise ImportError("pandas is required. Install: pip install brdocuments[pandas]") from exc

import brdocuments
from brdocuments.secure import mask_cnpj as _mask_cnpj
from brdocuments.secure import mask_cpf as _mask_cpf


def _to_str_series(s: pd.Series) -> pd.Series:
    return s.astype(str)


def _classify(v: str) -> str:
    result = brdocuments.classify_pix(v)
    return result.name if result is not None else ""


class BRDocsAccessor:
    def __init__(self, series: pd.Series) -> None:
        self._series = series

    def is_valid_cpf(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_cpf)

    def is_valid_cnpj(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_cnpj)

    def is_valid_ie(self, state: str) -> pd.Series:
        return _to_str_series(self._series).apply(lambda v: brdocuments.is_valid_ie(v, state))

    def is_valid_cep(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_cep)

    def is_valid_cnh(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_cnh)

    def is_valid_pis(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_pis)

    def is_valid_renavam(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_renavam)

    def is_valid_titulo_eleitor(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_titulo_eleitor)

    def is_valid_cnj(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_cnj)

    def is_valid_nfe(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.is_valid_nfe)

    def classify_pix(self) -> pd.Series:
        return _to_str_series(self._series).apply(_classify)

    def format_cpf(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_cpf)

    def format_cnpj(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_cnpj)

    def format_ie(self, state: str) -> pd.Series:
        return _to_str_series(self._series).apply(lambda v: brdocuments.format_ie(v, state))

    def format_cep(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_cep)

    def format_cnh(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_cnh)

    def format_pis(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_pis)

    def format_renavam(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_renavam)

    def format_titulo_eleitor(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_titulo_eleitor)

    def format_cnj(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_cnj)

    def format_nfe(self) -> pd.Series:
        return _to_str_series(self._series).apply(brdocuments.format_nfe)

    def mask_cpf(self) -> pd.Series:
        return _to_str_series(self._series).apply(_mask_cpf)

    def mask_cnpj(self) -> pd.Series:
        return _to_str_series(self._series).apply(_mask_cnpj)


pd.api.extensions.register_series_accessor("brdocuments")(BRDocsAccessor)
