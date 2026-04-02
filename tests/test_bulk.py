from unittest.mock import patch

import pytest

import brdocuments
from brdocuments.bulk import generate_list, validate_docs, validate_list


class TestValidateList:
    def test_all_valid_cpfs(self) -> None:
        valid = brdocuments.generate_cpf()
        result = validate_list("cpf", [valid])
        assert result == [True]

    def test_all_invalid_cpfs(self) -> None:
        result = validate_list("cpf", ["000.000.000-00"])
        assert result == [False]

    def test_mixed_cpfs(self) -> None:
        valid = brdocuments.generate_cpf()
        result = validate_list("cpf", [valid, "000.000.000-00"])
        assert result == [True, False]

    def test_empty_list(self) -> None:
        assert validate_list("cpf", []) == []

    def test_works_for_cnpj(self) -> None:
        valid = brdocuments.generate_cnpj()
        result = validate_list("cnpj", [valid])
        assert result == [True]

    def test_works_for_all_supported_types(self) -> None:
        for doc_type in ("cpf", "cnpj", "renavam", "titulo_eleitor"):
            result = validate_list(doc_type, [])
            assert result == []

    def test_raises_on_unknown_doc_type(self) -> None:
        with pytest.raises(ValueError, match="Unknown doc type"):
            validate_list("passport", ["123"])

    def test_result_length_matches_input(self) -> None:
        cpfs = [brdocuments.generate_cpf() for _ in range(5)]
        result = validate_list("cpf", cpfs)
        assert len(result) == 5

    def test_doc_type_case_insensitive(self) -> None:
        valid = brdocuments.generate_cpf()
        assert validate_list("CPF", [valid]) == [True]
        assert validate_list("Cpf", [valid]) == [True]


class TestGenerateList:
    def test_generates_n_cpfs(self) -> None:
        result = generate_list("cpf", 5)
        assert len(result) == 5

    def test_all_generated_are_valid(self) -> None:
        result = generate_list("cpf", 10)
        assert all(brdocuments.is_valid_cpf(v) for v in result)

    def test_all_generated_are_unique(self) -> None:
        result = generate_list("cpf", 20)
        assert len(set(result)) == 20

    def test_formatted_flag(self) -> None:
        result = generate_list("cpf", 3, formatted=True)
        assert all("." in v for v in result)

    def test_unformatted_by_default(self) -> None:
        result = generate_list("cpf", 3)
        assert all("." not in v for v in result)

    def test_generates_cnpj(self) -> None:
        result = generate_list("cnpj", 3)
        assert all(brdocuments.is_valid_cnpj(v) for v in result)

    def test_generates_renavam(self) -> None:
        result = generate_list("renavam", 3)
        assert all(brdocuments.is_valid_renavam(v) for v in result)

    def test_generates_titulo_eleitor(self) -> None:
        result = generate_list("titulo_eleitor", 3)
        assert all(brdocuments.is_valid_titulo_eleitor(v) for v in result)

    def test_zero_count_returns_empty(self) -> None:
        assert generate_list("cpf", 0) == []

    def test_raises_on_unknown_doc_type(self) -> None:
        with pytest.raises(ValueError, match="Unknown doc type"):
            generate_list("passport", 3)

    def test_doc_type_case_insensitive(self) -> None:
        result = generate_list("CPF", 3)
        assert all(brdocuments.is_valid_cpf(v) for v in result)

    def test_skips_duplicates(self) -> None:
        # Force generator to return duplicate on first two calls, then unique values
        cpf_a = brdocuments.generate_cpf()
        cpf_b = brdocuments.generate_cpf()
        side_effects = [cpf_a, cpf_a, cpf_b]  # first duplicate triggers skip branch
        with patch("brdocuments.bulk._GENERATORS", {"cpf": iter(side_effects).__next__}):
            result = generate_list("cpf", 2)
        assert len(result) == 2
        assert result[0] == cpf_a
        assert result[1] == cpf_b


class TestValidateDocs:
    def test_single_valid_cpf(self) -> None:
        valid = brdocuments.generate_cpf()
        assert validate_docs([("cpf", valid)]) == [True]

    def test_single_invalid_cpf(self) -> None:
        assert validate_docs([("cpf", "000.000.000-00")]) == [False]

    def test_mixed_types(self) -> None:
        cpf = brdocuments.generate_cpf()
        cnpj = brdocuments.generate_cnpj()
        result = validate_docs([("cpf", cpf), ("cnpj", cnpj)])
        assert result == [True, True]

    def test_mixed_valid_invalid(self) -> None:
        cpf = brdocuments.generate_cpf()
        result = validate_docs([("cpf", cpf), ("cpf", "000.000.000-00")])
        assert result == [True, False]

    def test_empty_list(self) -> None:
        assert validate_docs([]) == []

    def test_raises_on_unknown_doc_type(self) -> None:
        with pytest.raises(ValueError, match="Unknown doc type"):
            validate_docs([("passport", "123")])

    def test_result_length_matches_input(self) -> None:
        pairs = [("cpf", brdocuments.generate_cpf()) for _ in range(5)]
        result = validate_docs(pairs)
        assert len(result) == 5

    def test_doc_type_case_insensitive(self) -> None:
        valid = brdocuments.generate_cpf()
        assert validate_docs([("CPF", valid)]) == [True]


class TestBulkExportedFromBrdocs:
    def test_validate_list_importable_from_brdocs(self) -> None:
        assert hasattr(brdocuments, "validate_list")

    def test_generate_list_importable_from_brdocs(self) -> None:
        assert hasattr(brdocuments, "generate_list")

    def test_validate_docs_importable_from_brdocs(self) -> None:
        assert hasattr(brdocuments, "validate_docs")
