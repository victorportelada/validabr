# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-04-02

### Added
- CNPJ alfanumérico support (IN RFB 2.229/2024): `is_valid_cnpj`, `generate_cnpj(alfa=True)`, `format_cnpj`, and `parse_cnpj` now handle the new alphanumeric format
- `format_pix` and `parse_pix` — completes the PIX module (all 5 key types: CPF, CNPJ, PHONE, EMAIL, EVP)
- `generate_nfe` — generates valid NFe/CTe/NFC-e/MDF-e access keys (44 digits) with correct mod-11 check digit

## [1.0.1] - 2026-04-02

### Changed
- README references updated to validabr

## [1.0.0] - 2026-04-02

### Added
- Initial release
- 12 document types: CPF, CNPJ, CNJ, IE, RENAVAM, Título de Eleitor, CNH, PIS/PASEP, CEP, CNS, NFe/CTe, Chave Pix
- CLI interface
- LGPD compliance features (masking, redaction, filtering)
- Pandas integration
- Polars integration
