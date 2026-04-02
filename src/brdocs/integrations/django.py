"""Django integration for brdocs.

This module requires Django to be installed:
    pip install django>=4.0

Model Fields:
    from brdocs.integrations.django import CPFField

    class Person(models.Model):
        cpf = CPFField()

Form Fields:
    from brdocs.integrations.django import CPFFormField

    class PersonForm(forms.Form):
        cpf = CPFFormField()
"""

from __future__ import annotations

import re
from typing import Any

try:
    from django import forms as django_forms
    from django.db import models as django_models
except ImportError as exc:
    raise ImportError(
        "Django is required for brdocs.integrations.django. "
        "Install it with: pip install brdocs[django]"
    ) from exc

import brdocs

__all__ = [
    "CNJField",
    "CNJFormField",
    "CNPJField",
    "CNPJFormField",
    "CPFField",
    "CPFFormField",
    "IEField",
    "IEFormField",
    "RenavamField",
    "RenavamFormField",
    "TituloEleitorField",
    "TituloEleitorFormField",
]


# ---------------------------------------------------------------------------
# CPF
# ---------------------------------------------------------------------------


class CPFFormField(django_forms.CharField):
    """Django form field for CPF."""

    def __init__(self, *, required: bool = True, **kwargs: Any) -> None:
        super().__init__(required=required, **kwargs)

    def clean(self, value: Any) -> str:
        if not value or (isinstance(value, str) and not value.strip()):
            if self.required:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field is required.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid input type.")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 11:
            from django.core.exceptions import ValidationError

            raise ValidationError("CPF must have 11 digits.")
        if not brdocs.is_valid_cpf(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid CPF.")
        return brdocs.format_cpf(digits)


class CPFField(django_models.CharField):  # type: ignore[type-arg]
    """Django model field for CPF."""

    def __init__(
        self,
        *,
        null: bool = False,
        blank: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            max_length=14,
            null=null,
            blank=blank,
            **kwargs,
        )

    def to_python(self, value: Any) -> str | None:
        if value is None or value == "":
            if self.null:
                return None
            if not self.blank:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field cannot be null.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Expected str, got {type(value).__name__}")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 11:
            from django.core.exceptions import ValidationError

            raise ValidationError("CPF must have 11 digits.")
        if not brdocs.is_valid_cpf(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid CPF.")
        return brdocs.format_cpf(digits)

    def get_prep_value(self, value: Any) -> str | None:
        if value is None:
            return None
        return re.sub(r"\D", "", str(value))

    def formfield(self, **kwargs: Any) -> django_forms.CharField:  # type: ignore[override]
        defaults: dict[str, Any] = {"required": not self.blank}
        defaults.update(kwargs)
        return CPFFormField(**defaults)

    def deconstruct(self) -> tuple[Any, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["null"] = self.null
        kwargs["blank"] = self.blank
        return name, path, args, kwargs  # type: ignore[return-value]  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# CNPJ
# ---------------------------------------------------------------------------


class CNPJFormField(django_forms.CharField):
    """Django form field for CNPJ."""

    def __init__(self, *, required: bool = True, **kwargs: Any) -> None:
        super().__init__(required=required, **kwargs)

    def clean(self, value: Any) -> str:
        if not value or (isinstance(value, str) and not value.strip()):
            if self.required:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field is required.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid input type.")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 14:
            from django.core.exceptions import ValidationError

            raise ValidationError("CNPJ must have 14 digits.")
        if not brdocs.is_valid_cnpj(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid CNPJ.")
        return brdocs.format_cnpj(digits)


class CNPJField(django_models.CharField):  # type: ignore[type-arg]
    """Django model field for CNPJ."""

    def __init__(
        self,
        *,
        null: bool = False,
        blank: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            max_length=18,
            null=null,
            blank=blank,
            **kwargs,
        )

    def to_python(self, value: Any) -> str | None:
        if value is None or value == "":
            if self.null:
                return None
            if not self.blank:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field cannot be null.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Expected str, got {type(value).__name__}")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 14:
            from django.core.exceptions import ValidationError

            raise ValidationError("CNPJ must have 14 digits.")
        if not brdocs.is_valid_cnpj(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid CNPJ.")
        return brdocs.format_cnpj(digits)

    def get_prep_value(self, value: Any) -> str | None:
        if value is None:
            return None
        return re.sub(r"\D", "", str(value))

    def formfield(self, **kwargs: Any) -> django_forms.CharField:  # type: ignore[override]
        defaults: dict[str, Any] = {"required": not self.blank}
        defaults.update(kwargs)
        return CNPJFormField(**defaults)

    def deconstruct(self) -> tuple[Any, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["null"] = self.null
        kwargs["blank"] = self.blank
        return name, path, args, kwargs  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# CNJ
# ---------------------------------------------------------------------------


class CNJFormField(django_forms.CharField):
    """Django form field for CNJ."""

    def __init__(self, *, required: bool = True, **kwargs: Any) -> None:
        super().__init__(required=required, **kwargs)

    def clean(self, value: Any) -> str:
        if not value or (isinstance(value, str) and not value.strip()):
            if self.required:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field is required.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid input type.")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 20:
            from django.core.exceptions import ValidationError

            raise ValidationError("CNJ must have 20 digits.")
        if not brdocs.is_valid_cnj(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid CNJ.")
        return brdocs.format_cnj(digits)


class CNJField(django_models.CharField):  # type: ignore[type-arg]
    """Django model field for CNJ (Processo)."""

    def __init__(
        self,
        *,
        null: bool = False,
        blank: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            max_length=25,
            null=null,
            blank=blank,
            **kwargs,
        )

    def to_python(self, value: Any) -> str | None:
        if value is None or value == "":
            if self.null:
                return None
            if not self.blank:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field cannot be null.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Expected str, got {type(value).__name__}")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 20:
            from django.core.exceptions import ValidationError

            raise ValidationError("CNJ must have 20 digits.")
        if not brdocs.is_valid_cnj(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid CNJ.")
        return brdocs.format_cnj(digits)

    def get_prep_value(self, value: Any) -> str | None:
        if value is None:
            return None
        return re.sub(r"\D", "", str(value))

    def formfield(self, **kwargs: Any) -> django_forms.CharField:  # type: ignore[override]
        defaults: dict[str, Any] = {"required": not self.blank}
        defaults.update(kwargs)
        return CNJFormField(**defaults)

    def deconstruct(self) -> tuple[Any, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["null"] = self.null
        kwargs["blank"] = self.blank
        return name, path, args, kwargs  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Renavam
# ---------------------------------------------------------------------------


class RenavamFormField(django_forms.CharField):
    """Django form field for RENAVAM."""

    def __init__(self, *, required: bool = True, **kwargs: Any) -> None:
        super().__init__(required=required, **kwargs)

    def clean(self, value: Any) -> str:
        if not value or (isinstance(value, str) and not value.strip()):
            if self.required:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field is required.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid input type.")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 11:
            from django.core.exceptions import ValidationError

            raise ValidationError("RENAVAM must have 11 digits.")
        if not brdocs.is_valid_renavam(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid RENAVAM.")
        return brdocs.format_renavam(digits)


class RenavamField(django_models.CharField):  # type: ignore[type-arg]
    """Django model field for RENAVAM."""

    def __init__(
        self,
        *,
        null: bool = False,
        blank: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            max_length=12,
            null=null,
            blank=blank,
            **kwargs,
        )

    def to_python(self, value: Any) -> str | None:
        if value is None or value == "":
            if self.null:
                return None
            if not self.blank:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field cannot be null.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Expected str, got {type(value).__name__}")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 11:
            from django.core.exceptions import ValidationError

            raise ValidationError("RENAVAM must have 11 digits.")
        if not brdocs.is_valid_renavam(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid RENAVAM.")
        return brdocs.format_renavam(digits)

    def get_prep_value(self, value: Any) -> str | None:
        if value is None:
            return None
        return re.sub(r"\D", "", str(value))

    def formfield(self, **kwargs: Any) -> django_forms.CharField:  # type: ignore[override]
        defaults: dict[str, Any] = {"required": not self.blank}
        defaults.update(kwargs)
        return RenavamFormField(**defaults)

    def deconstruct(self) -> tuple[Any, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["null"] = self.null
        kwargs["blank"] = self.blank
        return name, path, args, kwargs  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# TituloEleitor
# ---------------------------------------------------------------------------


class TituloEleitorFormField(django_forms.CharField):
    """Django form field for Título de Eleitor."""

    def __init__(self, *, required: bool = True, **kwargs: Any) -> None:
        super().__init__(required=required, **kwargs)

    def clean(self, value: Any) -> str:
        if not value or (isinstance(value, str) and not value.strip()):
            if self.required:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field is required.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid input type.")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 12:
            from django.core.exceptions import ValidationError

            raise ValidationError("Título de Eleitor must have 12 digits.")
        if not brdocs.is_valid_titulo_eleitor(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid Título de Eleitor.")
        return brdocs.format_titulo_eleitor(digits)


class TituloEleitorField(django_models.CharField):  # type: ignore[type-arg]
    """Django model field for Título de Eleitor."""

    def __init__(
        self,
        *,
        null: bool = False,
        blank: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            max_length=14,
            null=null,
            blank=blank,
            **kwargs,
        )

    def to_python(self, value: Any) -> str | None:
        if value is None or value == "":
            if self.null:
                return None
            if not self.blank:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field cannot be null.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Expected str, got {type(value).__name__}")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 12:
            from django.core.exceptions import ValidationError

            raise ValidationError("Título de Eleitor must have 12 digits.")
        if not brdocs.is_valid_titulo_eleitor(digits):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid Título de Eleitor.")
        return brdocs.format_titulo_eleitor(digits)

    def get_prep_value(self, value: Any) -> str | None:
        if value is None:
            return None
        return re.sub(r"\D", "", str(value))

    def formfield(self, **kwargs: Any) -> django_forms.CharField:  # type: ignore[override]
        defaults: dict[str, Any] = {"required": not self.blank}
        defaults.update(kwargs)
        return TituloEleitorFormField(**defaults)

    def deconstruct(self) -> tuple[Any, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["null"] = self.null
        kwargs["blank"] = self.blank
        return name, path, args, kwargs  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# IE (Inscrição Estadual) - requires state
# ---------------------------------------------------------------------------


class IEFormField(django_forms.CharField):
    """Django form field for Inscrição Estadual (IE)."""

    def __init__(
        self,
        *,
        state: str,
        required: bool = True,
        **kwargs: Any,
    ) -> None:
        if not state:
            raise ValueError("state is required for IEFormField")
        self._state = state.upper().strip()
        super().__init__(required=required, **kwargs)

    def clean(self, value: Any) -> str:
        if not value or (isinstance(value, str) and not value.strip()):
            if self.required:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field is required.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid input type.")
        digits = re.sub(r"\D", "", value)
        if not brdocs.is_valid_ie(digits, self._state):
            from django.core.exceptions import ValidationError

            raise ValidationError("Invalid Inscrição Estadual.")
        return brdocs.format_ie(digits, self._state)


class IEField(django_models.CharField):  # type: ignore[type-arg]
    """Django model field for Inscrição Estadual (IE)."""

    def __init__(
        self,
        *,
        state: str,
        null: bool = False,
        blank: bool = False,
        **kwargs: Any,
    ) -> None:
        if not state:
            raise ValueError("state is required for IEField")
        self._state = state.upper().strip()
        super().__init__(
            max_length=16,
            null=null,
            blank=blank,
            **kwargs,
        )

    def to_python(self, value: Any) -> str | None:
        if value is None or value == "":
            if self.null:
                return None
            if not self.blank:
                from django.core.exceptions import ValidationError

                raise ValidationError("This field cannot be null.")
            return ""
        if not isinstance(value, str):
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Expected str, got {type(value).__name__}")
        digits = re.sub(r"\D", "", value)
        if not brdocs.is_valid_ie(digits, self._state):
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Invalid IE for state {self._state}.")
        return brdocs.format_ie(digits, self._state)

    def get_prep_value(self, value: Any) -> str | None:
        if value is None:
            return None
        return re.sub(r"\D", "", str(value))

    def formfield(self, **kwargs: Any) -> IEFormField:  # type: ignore[override]
        defaults: dict[str, Any] = {"required": not self.blank}
        defaults.update(kwargs)
        return IEFormField(state=self._state, **defaults)

    def deconstruct(self) -> tuple[Any, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["state"] = self._state
        kwargs["null"] = self.null
        kwargs["blank"] = self.blank
        return name, path, args, kwargs  # type: ignore[return-value]
