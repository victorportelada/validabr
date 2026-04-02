import re

from validabr.generators.cnj import generate_cnj
from validabr.validators.cnj import is_valid_cnj


class TestCNJGenerator:
    def test_generates_valid_cnj(self) -> None:
        for _ in range(50):
            assert is_valid_cnj(generate_cnj())

    def test_formatted_output_structure(self) -> None:
        cnj = generate_cnj(formatted=True)
        assert re.match(r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$", cnj)

    def test_unformatted_output_is_20_digits(self) -> None:
        cnj = generate_cnj(formatted=False)
        assert len(cnj) == 20
        assert cnj.isdigit()

    def test_unformatted_validates(self) -> None:
        for _ in range(20):
            assert is_valid_cnj(generate_cnj(formatted=False))

    def test_justice_segment_in_range(self) -> None:
        for _ in range(50):
            cnj = generate_cnj(formatted=False)
            justice = int(cnj[13])
            assert 1 <= justice <= 9

    def test_year_in_range(self) -> None:
        for _ in range(50):
            cnj = generate_cnj(formatted=False)
            year = int(cnj[9:13])
            assert 2000 <= year <= 2030
