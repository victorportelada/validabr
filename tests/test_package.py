import pybrdoc


def test_public_api_exports_validators() -> None:
    assert callable(pybrdoc.is_valid_cpf)
    assert callable(pybrdoc.is_valid_cnpj)
    assert callable(pybrdoc.is_valid_cnj)
    assert callable(pybrdoc.is_valid_ie)
    assert callable(pybrdoc.is_valid_renavam)
    assert callable(pybrdoc.is_valid_titulo_eleitor)


def test_public_api_exports_generators() -> None:
    assert callable(pybrdoc.generate_cpf)
    assert callable(pybrdoc.generate_cnpj)
    assert callable(pybrdoc.generate_cnj)
    assert callable(pybrdoc.generate_ie)
    assert callable(pybrdoc.generate_renavam)
    assert callable(pybrdoc.generate_titulo_eleitor)


def test_public_api_exports_parsers() -> None:
    assert callable(pybrdoc.format_cpf)
    assert callable(pybrdoc.format_cnpj)
    assert callable(pybrdoc.format_cnj)
    assert callable(pybrdoc.format_ie)
    assert callable(pybrdoc.format_renavam)
    assert callable(pybrdoc.format_titulo_eleitor)


def test_version_is_accessible() -> None:
    assert isinstance(pybrdoc.__version__, str)
    assert len(pybrdoc.__version__) > 0
