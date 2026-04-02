"""Tests for brdocuments Django integration."""

import pytest

django = pytest.importorskip("django")

from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={},
        INSTALLED_APPS=[],
        USE_I18N=True,
        USE_L10N=True,
    )
    import django

    django.setup()

from django import forms
from django.core.exceptions import ValidationError
from django.db import models

import brdocuments
from brdocuments.integrations.django import (
    CNJField,
    CNPJField,
    CNPJFormField,
    CPFField,
    CPFFormField,
    IEField,
    IEFormField,
    RenavamField,
    TituloEleitorField,
)

# ---------------------------------------------------------------------------
# CPF
# ---------------------------------------------------------------------------


class TestCPFModelField:
    def test_accepts_valid_cpf(self) -> None:
        class Person(models.Model):
            cpf = CPFField()

            class Meta:
                app_label = "test"

        p = Person(cpf="529.982.247-25")
        p.full_clean()
        assert p.cpf == "529.982.247-25"

    def test_accepts_unformatted(self) -> None:
        class Person(models.Model):
            cpf = CPFField()

            class Meta:
                app_label = "test"

        p = Person(cpf="52998224725")
        p.full_clean()
        assert p.cpf == "529.982.247-25"

    def test_rejects_invalid_cpf(self) -> None:
        class Person(models.Model):
            cpf = CPFField()

            class Meta:
                app_label = "test"

        p = Person(cpf="000.000.000-00")
        with pytest.raises(ValidationError):
            p.full_clean()

    def test_rejects_wrong_length(self) -> None:
        class Person(models.Model):
            cpf = CPFField()

            class Meta:
                app_label = "test"

        p = Person(cpf="123")
        with pytest.raises(ValidationError):
            p.full_clean()

    def test_null_blank(self) -> None:
        class Person(models.Model):
            cpf = CPFField(null=True, blank=True)

            class Meta:
                app_label = "test"

        p = Person()
        p.full_clean()
        assert p.cpf is None

    def test_round_trip(self) -> None:
        class Person(models.Model):
            cpf = CPFField()

            class Meta:
                app_label = "test"

        raw = brdocuments.generate_cpf()
        p = Person(cpf=raw)
        p.full_clean()
        assert brdocuments.is_valid_cpf(p.cpf)


# ---------------------------------------------------------------------------
# CNPJ
# ---------------------------------------------------------------------------


class TestCNPJModelField:
    def test_accepts_valid_cnpj(self) -> None:
        class Company(models.Model):
            cnpj = CNPJField()

            class Meta:
                app_label = "test"

        c = Company(cnpj="11.222.333/0001-81")
        c.full_clean()
        assert c.cnpj == "11.222.333/0001-81"

    def test_accepts_unformatted(self) -> None:
        class Company(models.Model):
            cnpj = CNPJField()

            class Meta:
                app_label = "test"

        c = Company(cnpj="11222333000181")
        c.full_clean()
        assert c.cnpj == "11.222.333/0001-81"

    def test_rejects_invalid_cnpj(self) -> None:
        class Company(models.Model):
            cnpj = CNPJField()

            class Meta:
                app_label = "test"

        c = Company(cnpj="00.000.000/0000-00")
        with pytest.raises(ValidationError):
            c.full_clean()

    def test_null_blank(self) -> None:
        class Company(models.Model):
            cnpj = CNPJField(null=True, blank=True)

            class Meta:
                app_label = "test"

        c = Company()
        c.full_clean()
        assert c.cnpj is None


# ---------------------------------------------------------------------------
# CNJ
# ---------------------------------------------------------------------------


class TestCNJModelField:
    def test_accepts_valid_cnj(self) -> None:
        class Process(models.Model):
            cnj = CNJField()

            class Meta:
                app_label = "test"

        raw = brdocuments.generate_cnj()
        p = Process(cnj=raw)
        p.full_clean()
        assert brdocuments.is_valid_cnj(p.cnj)

    def test_rejects_invalid_cnj(self) -> None:
        class Process(models.Model):
            cnj = CNJField()

            class Meta:
                app_label = "test"

        p = Process(cnj="0000000-00.0000.0.00.0000")
        with pytest.raises(ValidationError):
            p.full_clean()


# ---------------------------------------------------------------------------
# Renavam
# ---------------------------------------------------------------------------


class TestRenavamModelField:
    def test_accepts_valid_renavam(self) -> None:
        class Vehicle(models.Model):
            renavam = RenavamField()

            class Meta:
                app_label = "test"

        raw = brdocuments.generate_renavam()
        v = Vehicle(renavam=raw)
        v.full_clean()
        assert brdocuments.is_valid_renavam(v.renavam)

    def test_rejects_invalid_renavam(self) -> None:
        class Vehicle(models.Model):
            renavam = RenavamField()

            class Meta:
                app_label = "test"

        v = Vehicle(renavam="00000000000")
        with pytest.raises(ValidationError):
            v.full_clean()


# ---------------------------------------------------------------------------
# TituloEleitor
# ---------------------------------------------------------------------------


class TestTituloEleitorModelField:
    def test_accepts_valid_titulo(self) -> None:
        class Voter(models.Model):
            titulo = TituloEleitorField()

            class Meta:
                app_label = "test"

        raw = brdocuments.generate_titulo_eleitor()
        v = Voter(titulo=raw)
        v.full_clean()
        assert brdocuments.is_valid_titulo_eleitor(v.titulo)

    def test_rejects_invalid_titulo(self) -> None:
        class Voter(models.Model):
            titulo = TituloEleitorField()

            class Meta:
                app_label = "test"

        v = Voter(titulo="000000000000")
        with pytest.raises(ValidationError):
            v.full_clean()


# ---------------------------------------------------------------------------
# IE (requires state)
# ---------------------------------------------------------------------------


class TestIEModelField:
    def test_accepts_valid_ie_with_state(self) -> None:
        class Establishment(models.Model):
            ie = IEField(state="SP")

            class Meta:
                app_label = "test"

        raw = brdocuments.generate_ie("SP")
        e = Establishment(ie=raw)
        e.full_clean()
        assert brdocuments.is_valid_ie(e.ie, "SP")

    def test_rejects_invalid_ie(self) -> None:
        class Establishment(models.Model):
            ie = IEField(state="SP")

            class Meta:
                app_label = "test"

        e = Establishment(ie="000000000")
        with pytest.raises(ValidationError):
            e.full_clean()

    def test_rejects_ie_for_wrong_state(self) -> None:
        class Establishment(models.Model):
            ie = IEField(state="SP")

            class Meta:
                app_label = "test"

        raw = brdocuments.generate_ie("RJ")
        e = Establishment(ie=raw)
        with pytest.raises(ValidationError):
            e.full_clean()

    def test_different_states(self) -> None:
        class Establishment(models.Model):
            ie = IEField(state="MG")

            class Meta:
                app_label = "test"

        raw = brdocuments.generate_ie("MG")
        e = Establishment(ie=raw)
        e.full_clean()
        assert brdocuments.is_valid_ie(e.ie, "MG")


# ---------------------------------------------------------------------------
# Form Fields
# ---------------------------------------------------------------------------


class TestCPFFormField:
    def test_accepts_valid_cpf(self) -> None:
        class PersonForm(forms.Form):
            cpf = CPFFormField()

        f = PersonForm({"cpf": "529.982.247-25"})
        assert f.is_valid(), f.errors
        assert f.cleaned_data["cpf"] == "529.982.247-25"

    def test_rejects_invalid_cpf(self) -> None:
        class PersonForm(forms.Form):
            cpf = CPFFormField()

        f = PersonForm({"cpf": "000.000.000-00"})
        assert not f.is_valid()
        assert "cpf" in f.errors


class TestCNPJFormField:
    def test_accepts_valid_cnpj(self) -> None:
        class CompanyForm(forms.Form):
            cnpj = CNPJFormField()

        f = CompanyForm({"cnpj": "11.222.333/0001-81"})
        assert f.is_valid(), f.errors
        assert f.cleaned_data["cnpj"] == "11.222.333/0001-81"


class TestIEFormField:
    def test_accepts_valid_ie_with_state(self) -> None:
        class EstablishmentForm(forms.Form):
            ie = IEFormField(state="SP")

        raw = brdocuments.generate_ie("SP")
        f = EstablishmentForm({"ie": raw})
        assert f.is_valid(), f.errors
        assert brdocuments.is_valid_ie(f.cleaned_data["ie"], "SP")

    def test_rejects_invalid_ie(self) -> None:
        class EstablishmentForm(forms.Form):
            ie = IEFormField(state="SP")

        f = EstablishmentForm({"ie": "000000000"})
        assert not f.is_valid()
        assert "ie" in f.errors
