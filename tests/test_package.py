import brdocuments


def test_public_api_exports_validators() -> None:
    assert callable(brdocuments.is_valid_cpf)
    assert callable(brdocuments.is_valid_cnpj)
    assert callable(brdocuments.is_valid_cnj)
    assert callable(brdocuments.is_valid_ie)
    assert callable(brdocuments.is_valid_renavam)
    assert callable(brdocuments.is_valid_titulo_eleitor)


def test_public_api_exports_generators() -> None:
    assert callable(brdocuments.generate_cpf)
    assert callable(brdocuments.generate_cnpj)
    assert callable(brdocuments.generate_cnj)
    assert callable(brdocuments.generate_ie)
    assert callable(brdocuments.generate_renavam)
    assert callable(brdocuments.generate_titulo_eleitor)


def test_public_api_exports_parsers() -> None:
    assert callable(brdocuments.format_cpf)
    assert callable(brdocuments.format_cnpj)
    assert callable(brdocuments.format_cnj)
    assert callable(brdocuments.format_ie)
    assert callable(brdocuments.format_renavam)
    assert callable(brdocuments.format_titulo_eleitor)


def test_version_is_accessible() -> None:
    assert isinstance(brdocuments.__version__, str)
    assert len(brdocuments.__version__) > 0
