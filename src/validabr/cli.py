"""
Command-line interface for validabr.

Usage:
    validabr validate <type> <value> [--state XX]
    validabr generate <type> [--formatted] [--count N]
    validabr format   <type> <value> [--state XX]
    validabr parse    <type> <value> [--state XX]
    validabr mask     <type> <value>
"""

import argparse
import json
import sys
from collections.abc import Callable
from typing import NoReturn

from .bulk import _GENERATORS, generate_list
from .parsers import (
    format_cep,
    format_cnj,
    format_cnpj,
    format_cns,
    format_cpf,
    format_ie,
    format_nfe,
    format_pis,
    format_renavam,
    format_titulo_eleitor,
    parse_cep,
    parse_cnj,
    parse_cnpj,
    parse_cns,
    parse_cpf,
    parse_ie,
    parse_nfe,
    parse_pis,
    parse_renavam,
    parse_titulo_eleitor,
)
from .secure import mask_cep, mask_cnpj, mask_cns, mask_cpf, mask_pis
from .validators import (
    classify_pix,
    is_valid_cep,
    is_valid_cnj,
    is_valid_cnpj,
    is_valid_cns,
    is_valid_cpf,
    is_valid_ie,
    is_valid_nfe,
    is_valid_pis,
    is_valid_renavam,
    is_valid_titulo_eleitor,
)

_ValidatorFn = Callable[[str], bool]
_FormatterFn = Callable[[str], str]
_ParserFn = Callable[[str], dict[str, object]]

_VALIDATORS_CLI: dict[str, _ValidatorFn] = {
    "cep": is_valid_cep,
    "cpf": is_valid_cpf,
    "cnpj": is_valid_cnpj,
    "cnj": is_valid_cnj,
    "cns": is_valid_cns,
    "nfe": is_valid_nfe,
    "pis": is_valid_pis,
    "renavam": is_valid_renavam,
    "titulo_eleitor": is_valid_titulo_eleitor,
}

_FORMATTERS_CLI: dict[str, _FormatterFn] = {
    "cep": format_cep,
    "cpf": format_cpf,
    "cnpj": format_cnpj,
    "cnj": format_cnj,
    "cns": format_cns,
    "nfe": format_nfe,
    "pis": format_pis,
    "renavam": format_renavam,
    "titulo_eleitor": format_titulo_eleitor,
}

_PARSERS_CLI: dict[str, _ParserFn] = {
    "cep": lambda v: parse_cep(v)._asdict(),
    "cpf": lambda v: parse_cpf(v)._asdict(),
    "cnpj": lambda v: parse_cnpj(v)._asdict(),
    "cnj": lambda v: parse_cnj(v)._asdict(),
    "cns": lambda v: parse_cns(v)._asdict(),
    "nfe": lambda v: parse_nfe(v)._asdict(),
    "pis": lambda v: parse_pis(v)._asdict(),
    "renavam": lambda v: parse_renavam(v)._asdict(),
    "titulo_eleitor": lambda v: parse_titulo_eleitor(v)._asdict(),
}


def _mask_generic(v: str) -> str:
    return "*" * len(v)


_MaskFn = Callable[[str], str]

_MASKS: dict[str, _MaskFn] = {
    "cep": mask_cep,
    "cpf": mask_cpf,
    "cnpj": mask_cnpj,
    "cnj": _mask_generic,
    "cns": mask_cns,
    "pis": mask_pis,
    "renavam": _mask_generic,
    "titulo_eleitor": _mask_generic,
}


_CLI_TYPES = frozenset(
    [
        "cep",
        "cpf",
        "cnpj",
        "cnj",
        "cns",
        "nfe",
        "pis",
        "pix",
        "renavam",
        "titulo_eleitor",
        "ie",
    ]
)


def _resolve_cli_type(doc_type: str) -> str:
    normalized = doc_type.lower()
    if normalized not in _CLI_TYPES:
        raise ValueError(f"Unknown doc type: '{doc_type}'. Supported: {sorted(_CLI_TYPES)}")
    return normalized


def _err(msg: str) -> NoReturn:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def _cmd_validate(args: argparse.Namespace) -> None:
    try:
        doc_type = _resolve_cli_type(args.type)
    except ValueError as e:
        _err(str(e))

    state: str = args.state or ""

    if doc_type == "pix":
        key_type = classify_pix(args.value)
        if key_type is None:
            print(f"Invalid PIX: {args.value}")
            sys.exit(1)
        print(f"PIX key type: {key_type.name} ({key_type.value})")
        return

    if doc_type == "ie":
        if not state:
            _err("--state is required for ie")
        valid = is_valid_ie(args.value, state)
    else:
        valid = _VALIDATORS_CLI[doc_type](args.value)

    if valid:
        print(f"Valid {doc_type.upper()}: {args.value}")
    else:
        print(f"Invalid {doc_type.upper()}: {args.value}")
        sys.exit(1)


def _cmd_generate(args: argparse.Namespace) -> None:
    try:
        doc_type = _resolve_cli_type(args.type)
    except ValueError as e:
        _err(str(e))

    if doc_type not in _GENERATORS:
        _err(f"Generation not supported for '{doc_type}'")

    count = args.count or 1
    results = generate_list(doc_type, count, formatted=bool(args.formatted))
    for item in results:
        print(item)


def _cmd_format(args: argparse.Namespace) -> None:
    try:
        doc_type = _resolve_cli_type(args.type)
    except ValueError as e:
        _err(str(e))

    state: str = args.state or ""

    try:
        if doc_type == "ie":
            if not state:
                _err("--state is required for ie")
            result = format_ie(args.value, state)
        else:
            result = _FORMATTERS_CLI[doc_type](args.value)
    except ValueError as e:
        _err(str(e))

    print(result)


def _cmd_parse(args: argparse.Namespace) -> None:
    try:
        doc_type = _resolve_cli_type(args.type)
    except ValueError as e:
        _err(str(e))

    state: str = args.state or ""

    try:
        if doc_type == "ie":
            if not state:
                _err("--state is required for ie")
            data: dict[str, object] = parse_ie(args.value, state)._asdict()
        else:
            data = _PARSERS_CLI[doc_type](args.value)
    except ValueError as e:
        _err(str(e))

    print(json.dumps(data, ensure_ascii=False))


def _cmd_mask(args: argparse.Namespace) -> None:
    try:
        doc_type = _resolve_cli_type(args.type)
    except ValueError as e:
        _err(str(e))

    if doc_type not in _MASKS:
        _err(f"Masking not supported for '{doc_type}'")

    print(_MASKS[doc_type](args.value))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validabr",
        description="Brazilian document validation, generation, and formatting toolkit.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # validate
    p_validate = sub.add_parser("validate", help="Validate a document (or classify a PIX key).")
    p_validate.add_argument(
        "type",
        help="Document type: cep, cpf, cnpj, cnj, cns, nfe, pis, pix, renavam, titulo_eleitor, ie.",
    )
    p_validate.add_argument("value", help="Document value to validate.")
    p_validate.add_argument("--state", help="State code (required for ie).")

    # generate
    p_generate = sub.add_parser("generate", help="Generate a valid document.")
    p_generate.add_argument("type", help="Document type.")
    p_generate.add_argument("--formatted", action="store_true", help="Return formatted output.")
    p_generate.add_argument("--count", type=int, default=1, help="Number of documents.")

    # format
    p_format = sub.add_parser("format", help="Format a document string.")
    p_format.add_argument("type", help="Document type.")
    p_format.add_argument("value", help="Document value to format.")
    p_format.add_argument("--state", help="State code (required for ie).")

    # parse
    p_parse = sub.add_parser("parse", help="Parse a document into structured JSON.")
    p_parse.add_argument("type", help="Document type.")
    p_parse.add_argument("value", help="Document value to parse.")
    p_parse.add_argument("--state", help="State code (required for ie).")

    # mask
    p_mask = sub.add_parser("mask", help="Mask sensitive document digits.")
    p_mask.add_argument("type", help="Document type.")
    p_mask.add_argument("value", help="Document value to mask.")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    dispatch = {
        "validate": _cmd_validate,
        "generate": _cmd_generate,
        "format": _cmd_format,
        "parse": _cmd_parse,
        "mask": _cmd_mask,
    }

    dispatch[args.command](args)


if __name__ == "__main__":  # pragma: no cover
    main()
