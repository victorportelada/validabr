# Integrations module — optional, requires external dependencies (pydantic, django).
# It is always safe to `import brdocs` without these dependencies installed.
# Importing this sub-package only fails if the relevant framework is absent.

__all__: list[str] = []

try:
    from brdocs.integrations.django import (
        CNJField,
        CNJFormField,
        CNPJField,
        CNPJFormField,
        CPFField,
        CPFFormField,
        IEField,
        IEFormField,
        RenavamField,
        RenavamFormField,
        TituloEleitorField,
        TituloEleitorFormField,
    )

    __all__ += [
        "CNJField",
        "CNJFormField",
        "CNPJField",
        "CNPJFormField",
        "CPFField",
        "CPFFormField",
        "IEField",
        "IEFormField",
        "RenavamField",
        "RenavamFormField",
        "TituloEleitorField",
        "TituloEleitorFormField",
    ]
except ImportError:
    pass

try:
    from brdocs.integrations.pydantic import (
        CNJ,
        CNPJ,
        CPF,
        IE,
        Renavam,
        TituloEleitor,
        ie_field,
    )

    __all__ += [
        "CNJ",
        "CNPJ",
        "CPF",
        "IE",
        "Renavam",
        "TituloEleitor",
        "ie_field",
    ]
except ImportError:
    pass
