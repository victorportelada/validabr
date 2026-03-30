from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

try:
    __version__: str = _pkg_version("brdocs")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

from .generators import (
    generate_cnj,
    generate_cnpj,
    generate_cpf,
    generate_ie,
    generate_renavam,
    generate_titulo_eleitor,
)
from .parsers import (
    format_cnj,
    format_cnpj,
    format_cpf,
    format_ie,
    format_renavam,
    format_titulo_eleitor,
)
from .validators import (
    is_valid_cnj,
    is_valid_cnpj,
    is_valid_cpf,
    is_valid_ie,
    is_valid_renavam,
    is_valid_titulo_eleitor,
)

__all__ = [
    "__version__",
    "format_cnj",
    "format_cnpj",
    "format_cpf",
    "format_ie",
    "format_renavam",
    "format_titulo_eleitor",
    "generate_cnj",
    "generate_cnpj",
    "generate_cpf",
    "generate_ie",
    "generate_renavam",
    "generate_titulo_eleitor",
    "is_valid_cnj",
    "is_valid_cnpj",
    "is_valid_cpf",
    "is_valid_ie",
    "is_valid_renavam",
    "is_valid_titulo_eleitor",
]
