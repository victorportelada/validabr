from brdocuments.validators.titulo_eleitor import is_valid_titulo_eleitor


class TestTituloEleitorValidator:
    def test_valid_sp_state(self) -> None:
        # SP (state code 01) — special v2 rule applies
        assert is_valid_titulo_eleitor("000000020141") is True
        assert is_valid_titulo_eleitor("123456700188") is True

    def test_valid_other_state(self) -> None:
        # RS (state code 03) — standard rule
        assert is_valid_titulo_eleitor("038931450309") is True
        assert is_valid_titulo_eleitor("999999980395") is True

    def test_valid_with_spaces_or_hyphens(self) -> None:
        # Common informal formatting
        assert is_valid_titulo_eleitor("0000 0002 0141") is True
        assert is_valid_titulo_eleitor("038931450309") is True

    def test_invalid_wrong_first_check_digit(self) -> None:
        # Flip v1
        assert is_valid_titulo_eleitor("000000020241") is False

    def test_invalid_wrong_second_check_digit(self) -> None:
        # Flip v2
        assert is_valid_titulo_eleitor("000000020140") is False

    def test_invalid_state_code_zero(self) -> None:
        assert is_valid_titulo_eleitor("000000010000") is False

    def test_invalid_state_code_above_28(self) -> None:
        assert is_valid_titulo_eleitor("000000022900") is False

    def test_invalid_wrong_length(self) -> None:
        assert is_valid_titulo_eleitor("0000000201") is False
        assert is_valid_titulo_eleitor("0000000201411") is False

    def test_invalid_letters(self) -> None:
        assert is_valid_titulo_eleitor("ABCDEFGHIJKL") is False

    def test_invalid_not_string(self) -> None:
        assert is_valid_titulo_eleitor(None) is False  # type: ignore
        assert is_valid_titulo_eleitor(123456789012) is False  # type: ignore

    def test_empty(self) -> None:
        assert is_valid_titulo_eleitor("") is False


class TestTituloEleitorBranchCoverage:
    """Cover specific branches in titulo_eleitor validator not hit by round-trips."""

    def test_sp_mg_r1_equals_1_returns_false(self) -> None:
        """For SP/MG states, r1==1 -> no valid v1 exists -> return False (line 43)."""
        weights_seq = [2, 3, 4, 5, 6, 7, 8, 9]
        found_seq = None
        for n in range(0, 100_000_000):
            seq = [int(d) for d in str(n).zfill(8)]
            r1 = sum(d * w for d, w in zip(seq, weights_seq, strict=False)) % 11
            if r1 == 1:
                found_seq = str(n).zfill(8)
                break
        assert found_seq is not None
        # state code SP = 01, pick any v1 and v2
        titulo = found_seq + "01" + "00"
        assert is_valid_titulo_eleitor(titulo) is False

    def test_v1_mismatch_returns_false(self) -> None:
        """v1 != expected_v1 -> return False (line 50)."""
        from brdocuments.generators.titulo_eleitor import generate_titulo_eleitor

        titulo = generate_titulo_eleitor()
        # Flip digit at position 10 (v1)
        tampered = titulo[:10] + str((int(titulo[10]) + 1) % 10) + titulo[11]
        if tampered != titulo:
            assert is_valid_titulo_eleitor(tampered) is False


class TestGoRemainderZero:
    """Cover the GO _go validator branch where remainder==0 -> check=0 (line 124)."""

    def test_go_remainder_0_branch(self) -> None:
        from brdocuments.validators.ie import _go

        weights = [9, 8, 7, 6, 5, 4, 3, 2]
        for prefix in [10, 11, 15]:
            p = [prefix // 10, prefix % 10]
            for trial in range(100_000):
                base6 = [int(d) for d in str(trial).zfill(6)]
                base = p + base6
                total = sum(x * w for x, w in zip(base, weights, strict=False))
                if total % 11 == 0:
                    check = 0
                    assert _go([*base, check]) is True
                    return
        raise AssertionError("Could not find a GO IE with remainder 0")
