import re


def is_valid_cnpj(cnpj: str) -> bool:
    """
    Validates a Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica).

    Accepts formatted (12.345.678/0001-95) and unformatted (12345678000195) strings.
    """
    if not isinstance(cnpj, str):
        return False

    # 1. Reject if it contains anything other than digits, dots, hyphens, or slashes
    if re.search(r"[^\d.\/-]", cnpj):
        return False

    # 2. Clean the string, keeping only digits
    cleaned_cnpj = re.sub(r"[^\d]", "", cnpj)

    # 3. Check length
    if len(cleaned_cnpj) != 14:
        return False

    # 4. Prevent trivial false positives (all identical digits)
    if cleaned_cnpj == cleaned_cnpj[0] * 14:
        return False

    # Convert string to list of integers for math
    digits = [int(digit) for digit in cleaned_cnpj]

    # 4. Calculate First Verification Digit
    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_1 = sum(d * w for d, w in zip(digits[:12], weights_1, strict=True))
    remainder_1 = sum_1 % 11
    digit_1 = 0 if remainder_1 < 2 else 11 - remainder_1

    if digits[12] != digit_1:
        return False

    # 5. Calculate Second Verification Digit
    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_2 = sum(d * w for d, w in zip(digits[:13], weights_2, strict=True))
    remainder_2 = sum_2 % 11
    digit_2 = 0 if remainder_2 < 2 else 11 - remainder_2

    return digits[13] == digit_2
