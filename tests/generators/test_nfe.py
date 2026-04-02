import pytest

from validabr.generators.nfe import generate_nfe
from validabr.validators.nfe import is_valid_nfe


class TestGenerateNfe:
    def test_returns_string(self) -> None:
        assert isinstance(generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404"), str)

    def test_unformatted_is_44_digits(self) -> None:
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404")
        assert len(key) == 44
        assert key.isdigit()

    def test_formatted_has_correct_structure(self) -> None:
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", formatted=True)
        parts = key.split(" ")
        assert len(parts) == 9
        assert len(parts[0]) == 5
        assert len(parts[1]) == 5
        assert len(parts[2]) == 5
        assert len(parts[3]) == 5
        assert len(parts[4]) == 5
        assert len(parts[5]) == 5
        assert len(parts[6]) == 5
        assert len(parts[7]) == 5
        assert len(parts[8]) == 4

    def test_generated_key_is_valid(self) -> None:
        for _ in range(20):
            assert is_valid_nfe(generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404")) is True

    def test_formatted_key_is_valid(self) -> None:
        for _ in range(10):
            assert (
                is_valid_nfe(
                    generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", formatted=True)
                )
                is True
            )

    def test_generates_different_values(self) -> None:
        results = {generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404") for _ in range(30)}
        assert len(results) > 1

    def test_cuf_at_position_0_2(self) -> None:
        for cuf in [11, 35, 41, 53]:
            key = generate_nfe(cuf=cuf, cnpj="00000000000191", aamm="2404")
            assert key[0:2] == f"{cuf:02d}"

    def test_aamm_at_position_2_6(self) -> None:
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404")
        assert key[2:6] == "2404"

    def test_cnpj_at_position_6_20(self) -> None:
        key = generate_nfe(cuf=35, cnpj="12345678000195", aamm="2404")
        assert key[6:20] == "12345678000195"

    def test_mod_at_position_20_22(self) -> None:
        for mod in [55, 57, 58, 65]:
            key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", mod=mod)
            assert key[20:22] == f"{mod:02d}"

    def test_serie_at_position_22_25(self) -> None:
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", serie=1)
        assert key[22:25] == "001"
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", serie=999)
        assert key[22:25] == "999"

    def test_nnf_at_position_25_34(self) -> None:
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", nnf=1)
        assert key[25:34] == "000000001"
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", nnf=999999999)
        assert key[25:34] == "999999999"

    def test_tpemis_at_position_34_35(self) -> None:
        key = generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", tp_emis=1)
        assert key[34:35] == "1"

    def test_cnpj_formatted_accepted(self) -> None:
        key = generate_nfe(cuf=35, cnpj="00.000.000/0001-91", aamm="2404")
        assert len(key) == 44
        assert key.isdigit()


class TestGenerateNfeValidation:
    def test_raises_invalid_cuf(self) -> None:
        with pytest.raises(ValueError, match="cUF must be"):
            generate_nfe(cuf=99, cnpj="00000000000191", aamm="2404")

    def test_raises_invalid_mod(self) -> None:
        with pytest.raises(ValueError, match="mod must be"):
            generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", mod=99)

    def test_raises_invalid_aamm_wrong_length(self) -> None:
        with pytest.raises(ValueError, match="aamm must be"):
            generate_nfe(cuf=35, cnpj="00000000000191", aamm="24")

    def test_raises_invalid_aamm_non_digit(self) -> None:
        with pytest.raises(ValueError, match="aamm must be"):
            generate_nfe(cuf=35, cnpj="00000000000191", aamm="24AB")

    def test_raises_cnpj_wrong_digit_count(self) -> None:
        with pytest.raises(ValueError, match="CNPJ must have 14 digits"):
            generate_nfe(cuf=35, cnpj="123", aamm="2404")

    def test_raises_serie_out_of_range(self) -> None:
        with pytest.raises(ValueError, match="serie must be"):
            generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", serie=1000)

    def test_raises_nnf_out_of_range(self) -> None:
        with pytest.raises(ValueError, match="nnf must be"):
            generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", nnf=0)

    def test_raises_tp_emis_out_of_range(self) -> None:
        with pytest.raises(ValueError, match="tp_emis must be"):
            generate_nfe(cuf=35, cnpj="00000000000191", aamm="2404", tp_emis=0)


class TestGenerateNfeMultipleModels:
    @pytest.mark.parametrize("cuf", [35, 41, 53])
    @pytest.mark.parametrize("mod", [55, 65])
    def test_various_cuf_and_mod_combinations(self, cuf: int, mod: int) -> None:
        for _ in range(5):
            key = generate_nfe(cuf=cuf, cnpj="00000000000191", aamm="2404", mod=mod)
            assert is_valid_nfe(key) is True
            assert key[0:2] == f"{cuf:02d}"
            assert key[20:22] == f"{mod:02d}"
