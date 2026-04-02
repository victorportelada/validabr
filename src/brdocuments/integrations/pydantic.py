"""Pydantic v2 integration for brdocuments."""

from __future__ import annotations

from typing import Any

try:
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import core_schema
except ImportError as exc:
    raise ImportError(
        "Pydantic is required for brdocuments.integrations.pydantic. "
        "Install it with: pip install brdocuments[pydantic]"
    ) from exc

import brdocuments


class CPF(str):
    """Pydantic type for Brazilian CPF."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not isinstance(value, str):
                raise TypeError(f"CPF must be a string, got {type(value).__name__}")
            if not brdocuments.is_valid_cpf(value):
                raise ValueError("Invalid CPF")
            return brdocuments.format_cpf(value)

        return core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate),
            ]
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> dict[str, Any]:
        return {"type": "string", "title": "CPF"}


class CNPJ(str):
    """Pydantic type for Brazilian CNPJ."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not isinstance(value, str):
                raise TypeError(f"CNPJ must be a string, got {type(value).__name__}")
            if not brdocuments.is_valid_cnpj(value):
                raise ValueError("Invalid CNPJ")
            return brdocuments.format_cnpj(value)

        return core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate),
            ]
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> dict[str, Any]:
        return {"type": "string", "title": "CNPJ"}


class CNJ(str):
    """Pydantic type for Brazilian CNJ (Processo)."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not isinstance(value, str):
                raise TypeError(f"CNJ must be a string, got {type(value).__name__}")
            if not brdocuments.is_valid_cnj(value):
                raise ValueError("Invalid CNJ")
            return brdocuments.format_cnj(value)

        return core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate),
            ]
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> dict[str, Any]:
        return {"type": "string", "title": "CNJ"}


class Renavam(str):
    """Pydantic type for Brazilian RENAVAM."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not isinstance(value, str):
                raise TypeError(f"Renavam must be a string, got {type(value).__name__}")
            if not brdocuments.is_valid_renavam(value):
                raise ValueError("Invalid Renavam")
            return brdocuments.format_renavam(value)

        return core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate),
            ]
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> dict[str, Any]:
        return {"type": "string", "title": "Renavam"}


class TituloEleitor(str):
    """Pydantic type for Brazilian Título de Eleitor."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not isinstance(value, str):
                raise TypeError(f"TituloEleitor must be a string, got {type(value).__name__}")
            if not brdocuments.is_valid_titulo_eleitor(value):
                raise ValueError("Invalid TituloEleitor")
            return brdocuments.format_titulo_eleitor(value)

        return core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate),
            ]
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> dict[str, Any]:
        return {"type": "string", "title": "TituloEleitor"}


class IE(str):
    """Pydantic type for Brazilian Inscrição Estadual (IE)."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not isinstance(value, str):
                raise TypeError(f"IE must be a string, got {type(value).__name__}")
            # Note: IE validation requires state, which is handled by ie_field factory
            return value

        return core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate),
            ]
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> dict[str, Any]:
        return {"type": "string", "title": "IE"}


def ie_field(state: str) -> type:
    """Factory function to create an IE type with a specific state.

    Returns a class (not instance) that can be used directly as a Pydantic
    annotation: `ie: IEField` where `IEField = ie_field("SP")`.

    Usage:
        SP_IE = ie_field("SP")
        class M(BaseModel):
            ie: SP_IE  # validates IE for SP

    The returned class is a subclass of `str` with Pydantic schema that
    validates using `is_valid_ie(value, state)` and formats with
    `format_ie(value, state)`.
    """

    _state = state.upper().strip()

    class IEWithState(str):
        """IE type with state validation for a specific state."""

        @classmethod
        def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
        ) -> core_schema.CoreSchema:
            def validate(value: str) -> str:
                if not isinstance(value, str):
                    raise TypeError(f"IE must be a string, got {type(value).__name__}")
                if not brdocuments.is_valid_ie(value, _state):
                    raise ValueError(f"Invalid IE for state {_state}")
                return brdocuments.format_ie(value, _state)

            return core_schema.chain_schema(
                [
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(validate),
                ]
            )

        @classmethod
        def __get_pydantic_json_schema__(
            cls, core_schema: core_schema.CoreSchema, handler: Any
        ) -> dict[str, Any]:
            return {"type": "string", "title": f"IE ({_state})"}

    IEWithState.__name__ = f"IE_{_state}"
    IEWithState.__qualname__ = "ie_field.<locals>.IEWithState"
    return IEWithState
