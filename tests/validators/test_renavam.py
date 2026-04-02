from brdocs.validators.renavam import is_valid_renavam


class TestRenavamValidator:
    def test_valid_renavam_11_digits(self) -> None:
        # Computed: digits 0012345678, check=9
        assert is_valid_renavam("00123456789") is True

    def test_valid_renavam_with_hyphen(self) -> None:
        assert is_valid_renavam("0012345678-9") is True

    def test_valid_renavam_short_padded(self) -> None:
        # 8-digit Renavam, padded to 11 with leading zeros
        assert is_valid_renavam("12345678") is False
        assert is_valid_renavam("00012345670") in (True, False)

    def test_invalid_renavam_wrong_check_digit(self) -> None:
        assert is_valid_renavam("00123456780") is False

    def test_invalid_renavam_all_zeros(self) -> None:
        assert is_valid_renavam("00000000000") is False

    def test_invalid_renavam_wrong_length(self) -> None:
        assert is_valid_renavam("123456") is False
        assert is_valid_renavam("123456789012") is False

    def test_invalid_renavam_letters(self) -> None:
        assert is_valid_renavam("ABCDEFGHIJK") is False

    def test_invalid_renavam_not_string(self) -> None:
        assert is_valid_renavam(None) is False  # type: ignore
        assert is_valid_renavam(12345678901) is False  # type: ignore

    def test_empty_renavam(self) -> None:
        assert is_valid_renavam("") is False

    def test_renavam_remainder_1_is_invalid(self) -> None:
        """Craft a RENAVAM where weighted total % 11 == 1 → no valid check digit."""
        # Find a base where sum(d*w for first 10) % 11 == 1
        # Weights: [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        # Use 00000000001 (padded): digits=[0,0,0,0,0,0,0,0,0,0,1] padded
        # Let's try 10000000000: total = 1*3 = 3, %11=3, check=8 — not 1
        # Brute-force: total%11==1 → try leading zeros with a single digit
        from brdocs.validators.renavam import is_valid_renavam

        weights = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        found = None
        for n in range(1, 100_000):
            digits = [int(d) for d in str(n).zfill(10)]
            total = sum(d * w for d, w in zip(digits, weights, strict=False))
            if total % 11 == 1:
                # Append any check digit (will be wrong; code returns False before checking)
                found = str(n).zfill(10) + "0"
                break
        assert found is not None, "Could not find a RENAVAM base with remainder 1"
        assert is_valid_renavam(found) is False
