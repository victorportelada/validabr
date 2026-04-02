import validabr


def test_public_api_exports_validators() -> None:
    assert callable(validabr.is_valid_cpf)
    assert callable(validabr.is_valid_cnpj)
    assert callable(validabr.is_valid_cnj)
    assert callable(validabr.is_valid_ie)
    assert callable(validabr.is_valid_renavam)
    assert callable(validabr.is_valid_titulo_eleitor)


def test_public_api_exports_generators() -> None:
    assert callable(validabr.generate_cpf)
    assert callable(validabr.generate_cnpj)
    assert callable(validabr.generate_cnj)
    assert callable(validabr.generate_ie)
    assert callable(validabr.generate_renavam)
    assert callable(validabr.generate_titulo_eleitor)


def test_public_api_exports_parsers() -> None:
    assert callable(validabr.format_cpf)
    assert callable(validabr.format_cnpj)
    assert callable(validabr.format_cnj)
    assert callable(validabr.format_ie)
    assert callable(validabr.format_renavam)
    assert callable(validabr.format_titulo_eleitor)


def test_version_is_accessible() -> None:
    assert isinstance(validabr.__version__, str)
    assert len(validabr.__version__) > 0
