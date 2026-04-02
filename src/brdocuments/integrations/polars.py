"""Polars DataFrame extension for brdocuments.

Requires polars to be installed:
    pip install polars

Usage:
    import polars as pl
    import brdocuments.integrations.polars  # registers extension

    df = pl.DataFrame({"cpf": ["529.982.247-25", "000.000.000-00"]})
    df.select(pl.col("cpf").brdocuments.is_valid_cpf())     # returns Expr
    df.select(pl.col("cpf").brdocuments.format_cpf())       # returns Expr
    df.select(pl.col("cpf").brdocuments.mask_cpf())          # returns Expr
    df.select(pl.col("cnpj").brdocuments.is_valid_cnpj())   # returns Expr
    df.select(pl.col("cnpj").brdocuments.format_cnpj())     # returns Expr
    df.select(pl.col("cnpj").brdocuments.mask_cnpj())        # returns Expr
    df.select(pl.col("ie").brdocuments.is_valid_ie("SP"))    # returns Expr
    df.select(pl.col("ie").brdocuments.format_ie("SP"))       # returns Expr
    df.select(pl.col("cep").brdocuments.is_valid_cep())      # returns Expr
    df.select(pl.col("cep").brdocuments.format_cep())        # returns Expr
    df.select(pl.col("cnh").brdocuments.is_valid_cnh())      # returns Expr
    df.select(pl.col("cnh").brdocuments.format_cnh())        # returns Expr
    df.select(pl.col("pis").brdocuments.is_valid_pis())      # returns Expr
    df.select(pl.col("pis").brdocuments.format_pis())       # returns Expr
    df.select(pl.col("renavam").brdocuments.is_valid_renavam())  # returns Expr
    df.select(pl.col("renavam").brdocuments.format_renavam())    # returns Expr
    df.select(pl.col("titulo").brdocuments.is_valid_titulo_eleitor())  # returns Expr
    df.select(pl.col("titulo").brdocuments.format_titulo_eleitor())    # returns Expr
    df.select(pl.col("cnj").brdocuments.is_valid_cnj())      # returns Expr
    df.select(pl.col("cnj").brdocuments.format_cnj())        # returns Expr
    df.select(pl.col("nfe").brdocuments.is_valid_nfe())       # returns Expr
    df.select(pl.col("nfe").brdocuments.format_nfe())         # returns Expr
    df.select(pl.col("pix").brdocuments.classify_pix())     # returns Expr
"""

from __future__ import annotations

try:
    import polars as pl
except ImportError as exc:  # pragma: no cover
    raise ImportError("polars is required. Install: pip install brdocuments[polars]") from exc

import brdocuments
from brdocuments.secure import mask_cnpj as _mask_cnpj
from brdocuments.secure import mask_cpf as _mask_cpf


class BRDocsExpr:
    def __init__(self, expr: pl.Expr) -> None:
        self._expr = expr

    def is_valid_cpf(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_cpf, return_dtype=pl.Boolean)

    def is_valid_cnpj(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_cnpj, return_dtype=pl.Boolean)

    def is_valid_ie(self, state: str) -> pl.Expr:
        return self._expr.map_elements(
            lambda v: brdocuments.is_valid_ie(v, state), return_dtype=pl.Boolean
        )

    def is_valid_cep(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_cep, return_dtype=pl.Boolean)

    def is_valid_cnh(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_cnh, return_dtype=pl.Boolean)

    def is_valid_pis(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_pis, return_dtype=pl.Boolean)

    def is_valid_renavam(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_renavam, return_dtype=pl.Boolean)

    def is_valid_titulo_eleitor(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_titulo_eleitor, return_dtype=pl.Boolean)

    def is_valid_cnj(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_cnj, return_dtype=pl.Boolean)

    def is_valid_nfe(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.is_valid_nfe, return_dtype=pl.Boolean)

    def classify_pix(self) -> pl.Expr:
        def _classify(v: str) -> str:
            result = brdocuments.classify_pix(v)
            return result.name if result is not None else ""

        return self._expr.map_elements(_classify, return_dtype=pl.String)

    def format_cpf(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_cpf, return_dtype=pl.String)

    def format_cnpj(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_cnpj, return_dtype=pl.String)

    def format_ie(self, state: str) -> pl.Expr:
        def _fmt(v: str) -> str:
            return brdocuments.format_ie(v, state)

        return self._expr.map_elements(_fmt, return_dtype=pl.String)

    def format_cep(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_cep, return_dtype=pl.String)

    def format_cnh(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_cnh, return_dtype=pl.String)

    def format_pis(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_pis, return_dtype=pl.String)

    def format_renavam(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_renavam, return_dtype=pl.String)

    def format_titulo_eleitor(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_titulo_eleitor, return_dtype=pl.String)

    def format_cnj(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_cnj, return_dtype=pl.String)

    def format_nfe(self) -> pl.Expr:
        return self._expr.map_elements(brdocuments.format_nfe, return_dtype=pl.String)

    def mask_cpf(self) -> pl.Expr:
        return self._expr.map_elements(_mask_cpf, return_dtype=pl.String)

    def mask_cnpj(self) -> pl.Expr:
        return self._expr.map_elements(_mask_cnpj, return_dtype=pl.String)


def _brdocs_expr(expr: pl.Expr) -> pl.Expr:
    return expr._expr  # type: ignore[return-value, attr-defined]


pl.Expr.brdocuments = property(  # type: ignore[assignment]
    lambda self: BRDocsExpr(self)
)
