import json
import subprocess
import sys
from unittest.mock import patch

import pytest


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "validabr.cli", *args],
        capture_output=True,
        text=True,
    )


class TestValidateCommand:
    def test_valid_cpf_exits_zero(self) -> None:
        result = _run("validate", "cpf", "529.982.247-25")
        assert result.returncode == 0

    def test_valid_cpf_prints_valid(self) -> None:
        result = _run("validate", "cpf", "529.982.247-25")
        assert "valid" in result.stdout.lower()

    def test_invalid_cpf_exits_one(self) -> None:
        result = _run("validate", "cpf", "000.000.000-00")
        assert result.returncode == 1

    def test_invalid_cpf_prints_invalid(self) -> None:
        result = _run("validate", "cpf", "000.000.000-00")
        assert "invalid" in result.stdout.lower()

    def test_valid_cnpj(self) -> None:
        result = _run("validate", "cnpj", "11.222.333/0001-81")
        assert result.returncode == 0

    def test_valid_renavam(self) -> None:
        result = _run("validate", "renavam", "0012345678-9")
        # renavam 00123456789 → validity depends on check digit; just test exit behavior
        assert result.returncode in (0, 1)

    def test_unknown_type_exits_nonzero(self) -> None:
        result = _run("validate", "passport", "123")
        assert result.returncode != 0


class TestGenerateCommand:
    def test_generates_cpf(self) -> None:
        result = _run("generate", "cpf")
        assert result.returncode == 0
        assert result.stdout.strip() != ""

    def test_generates_formatted_cpf(self) -> None:
        result = _run("generate", "cpf", "--formatted")
        assert result.returncode == 0
        assert "." in result.stdout

    def test_generates_multiple(self) -> None:
        result = _run("generate", "cpf", "--count", "3")
        assert result.returncode == 0
        lines = [line for line in result.stdout.strip().splitlines() if line]
        assert len(lines) == 3

    def test_generates_cnpj(self) -> None:
        result = _run("generate", "cnpj")
        assert result.returncode == 0
        assert result.stdout.strip() != ""

    def test_unknown_type_exits_nonzero(self) -> None:
        result = _run("generate", "passport")
        assert result.returncode != 0


class TestFormatCommand:
    def test_formats_cpf(self) -> None:
        result = _run("format", "cpf", "52998224725")
        assert result.returncode == 0
        assert result.stdout.strip() == "529.982.247-25"

    def test_formats_cnpj(self) -> None:
        result = _run("format", "cnpj", "11222333000181")
        assert result.returncode == 0
        assert result.stdout.strip() == "11.222.333/0001-81"

    def test_invalid_length_exits_nonzero(self) -> None:
        result = _run("format", "cpf", "123")
        assert result.returncode != 0

    def test_unknown_type_exits_nonzero(self) -> None:
        result = _run("format", "passport", "123")
        assert result.returncode != 0


class TestParseCommand:
    def test_parse_cpf_outputs_json(self) -> None:
        result = _run("parse", "cpf", "52998224725")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "root" in data
        assert "check_digits" in data

    def test_parse_cnpj_outputs_json(self) -> None:
        result = _run("parse", "cnpj", "11222333000181")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "branch" in data
        assert data["is_matriz"] is True

    def test_parse_invalid_exits_nonzero(self) -> None:
        result = _run("parse", "cpf", "123")
        assert result.returncode != 0

    def test_unknown_type_exits_nonzero(self) -> None:
        result = _run("parse", "passport", "123")
        assert result.returncode != 0


class TestCLIDirect:
    """Direct invocation tests for coverage (subprocess tests verify exit codes)."""

    def _invoke(self, argv: list[str], capsys: pytest.CaptureFixture[str]) -> int:
        from validabr.cli import main

        with patch("sys.argv", ["validabr", *argv]):
            try:
                main()
                return 0
            except SystemExit as e:
                return int(e.code) if e.code is not None else 0

    def test_validate_valid_cpf(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "cpf", "529.982.247-25"], capsys)
        assert code == 0
        assert "valid" in capsys.readouterr().out.lower()

    def test_validate_invalid_cpf(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "cpf", "000.000.000-00"], capsys)
        assert code == 1

    def test_validate_unknown_type(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "passport", "123"], capsys)
        assert code != 0

    def test_validate_ie_without_state(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "ie", "123456789012"], capsys)
        assert code != 0

    def test_generate_cpf(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["generate", "cpf"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() != ""

    def test_generate_formatted(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["generate", "cpf", "--formatted"], capsys)
        assert code == 0
        assert "." in capsys.readouterr().out

    def test_generate_count(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["generate", "cpf", "--count", "3"], capsys)
        assert code == 0
        lines = [ln for ln in capsys.readouterr().out.strip().splitlines() if ln]
        assert len(lines) == 3

    def test_generate_unknown_type(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["generate", "passport"], capsys)
        assert code != 0

    def test_format_cpf(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["format", "cpf", "52998224725"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() == "529.982.247-25"

    def test_format_invalid_length(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["format", "cpf", "123"], capsys)
        assert code != 0

    def test_format_unknown_type(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["format", "passport", "123"], capsys)
        assert code != 0

    def test_parse_cpf(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["parse", "cpf", "52998224725"], capsys)
        assert code == 0
        data = json.loads(capsys.readouterr().out)
        assert "root" in data

    def test_parse_unknown_type(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["parse", "passport", "123"], capsys)
        assert code != 0

    def test_parse_invalid_value(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["parse", "cpf", "123"], capsys)
        assert code != 0

    def test_mask_cpf(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "cpf", "529.982.247-25"], capsys)
        assert code == 0
        out = capsys.readouterr().out.strip()
        assert "*" in out

    def test_mask_cnpj(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "cnpj", "11.222.333/0001-81"], capsys)
        assert code == 0
        assert "*" in capsys.readouterr().out

    def test_mask_unknown_type(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "passport", "123"], capsys)
        assert code != 0

    def test_mask_short_cpf_fallback(self, capsys: pytest.CaptureFixture[str]) -> None:
        # Non-11-digit input falls back to full mask
        code = self._invoke(["mask", "cpf", "123"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() == "***"

    def test_mask_short_cnpj_fallback(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "cnpj", "123"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() == "***"

    def test_mask_renavam(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "renavam", "0012345678-9"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() == "*" * len("0012345678-9")

    def test_validate_ie_with_state(self, capsys: pytest.CaptureFixture[str]) -> None:
        import validabr

        raw = validabr.generate_ie("SP")
        code = self._invoke(["validate", "ie", raw, "--state", "SP"], capsys)
        assert code == 0

    def test_validate_ie_without_state_direct(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "ie", "123456789012"], capsys)
        assert code != 0

    def test_format_ie_with_state(self, capsys: pytest.CaptureFixture[str]) -> None:
        import validabr

        raw = validabr.generate_ie("SP")
        code = self._invoke(["format", "ie", raw, "--state", "SP"], capsys)
        assert code == 0

    def test_format_ie_without_state(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["format", "ie", "123456789012"], capsys)
        assert code != 0

    def test_parse_ie_with_state(self, capsys: pytest.CaptureFixture[str]) -> None:
        import validabr

        raw = validabr.generate_ie("SP")
        code = self._invoke(["parse", "ie", raw, "--state", "SP"], capsys)
        assert code == 0
        data = json.loads(capsys.readouterr().out)
        assert "digits" in data
        assert data["state"] == "SP"

    def test_parse_ie_without_state(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["parse", "ie", "123456789012"], capsys)
        assert code != 0

    def test_mask_unknown_triggers_unsupported(self, capsys: pytest.CaptureFixture[str]) -> None:
        # ie is in _CLI_TYPES but not in _MASKS — triggers "not supported"
        code = self._invoke(["mask", "ie", "123456789012"], capsys)
        assert code != 0

    def test_generate_ie_not_supported(self, capsys: pytest.CaptureFixture[str]) -> None:
        # IE is not in _GENERATORS (requires state) → "not supported"
        code = self._invoke(["generate", "ie"], capsys)
        assert code != 0

    def test_validate_invalid_ie_exits_one(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "ie", "000000000", "--state", "SP"], capsys)
        assert code != 0

    def test_validate_pix_valid(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "pix", "529.982.247-25"], capsys)
        assert code == 0
        out = capsys.readouterr().out
        assert "CPF" in out

    def test_validate_pix_invalid(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["validate", "pix", "not-a-pix-key"], capsys)
        assert code == 1


class TestMaskCommand:
    def test_masks_cpf(self) -> None:
        result = _run("mask", "cpf", "529.982.247-25")
        assert result.returncode == 0
        output = result.stdout.strip()
        assert "*" in output
        assert output != "529.982.247-25"

    def test_masks_cnpj(self) -> None:
        result = _run("mask", "cnpj", "11.222.333/0001-81")
        assert result.returncode == 0
        assert "*" in result.stdout

    def test_unknown_type_exits_nonzero(self) -> None:
        result = _run("mask", "passport", "123")
        assert result.returncode != 0


class TestMaskFallbackBranches:
    """Cover the else-branch of mask functions (non-standard-length input)."""

    def _invoke(self, argv: list[str], capsys: pytest.CaptureFixture[str]) -> int:
        from validabr.cli import main

        with patch("sys.argv", ["validabr", *argv]):
            try:
                main()
                return 0
            except SystemExit as e:
                return int(e.code) if e.code is not None else 0

    def test_mask_cep_valid(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "cep", "01310-100"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() == "01310-***"

    def test_mask_cep_short_fallback(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "cep", "123"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() == "***"

    def test_mask_pis_valid(self, capsys: pytest.CaptureFixture[str]) -> None:
        import validabr

        raw = validabr.generate_pis()
        code = self._invoke(["mask", "pis", raw], capsys)
        assert code == 0
        out = capsys.readouterr().out.strip()
        assert "**" in out

    def test_mask_pis_short_fallback(self, capsys: pytest.CaptureFixture[str]) -> None:
        code = self._invoke(["mask", "pis", "123"], capsys)
        assert code == 0
        assert capsys.readouterr().out.strip() == "***"
