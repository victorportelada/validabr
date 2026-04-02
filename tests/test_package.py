import brdocs


def test_public_api_exports_validators() -> None:
    assert callable(brdocs.is_valid_cpf)
    assert callable(brdocs.is_valid_cnpj)
    assert callable(brdocs.is_valid_cnj)
    assert callable(brdocs.is_valid_ie)
    assert callable(brdocs.is_valid_renavam)
    assert callable(brdocs.is_valid_titulo_eleitor)


def test_public_api_exports_generators() -> None:
    assert callable(brdocs.generate_cpf)
    assert callable(brdocs.generate_cnpj)
    assert callable(brdocs.generate_cnj)
    assert callable(brdocs.generate_ie)
    assert callable(brdocs.generate_renavam)
    assert callable(brdocs.generate_titulo_eleitor)


def test_public_api_exports_parsers() -> None:
    assert callable(brdocs.format_cpf)
    assert callable(brdocs.format_cnpj)
    assert callable(brdocs.format_cnj)
    assert callable(brdocs.format_ie)
    assert callable(brdocs.format_renavam)
    assert callable(brdocs.format_titulo_eleitor)


def test_version_is_accessible() -> None:
    assert isinstance(brdocs.__version__, str)
    assert len(brdocs.__version__) > 0
