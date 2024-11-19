from django.contrib.auth import get_user_model

from handbooks.models import Country, LegalForm
from orgsandpeople.models import BusinessUnit, Bank
from commerce.models import Project
from tools.name2country import name2country

User = get_user_model()

def get_new_country(**d):
    eng_name = d.get("eng_name") or "Israel"
    data = name2country(eng_name)
    return Country.objects.create(**data)


def get_new_legal_form(**d):
    """Create and return Legal Form"""
    data = {
        'short_name': "MyLF",
        'full_name': "My Legal Form",
        'description': "Description of My Legal Form"
    }
    data.update(d)
    return LegalForm.objects.create(**data)


def get_new_user(**d):
    data = {
        'email': 'test1@example.com',
        'password': 'just_password',
        'is_active': True,
        'is_staff': False,
    }
    data.update(d)
    return User.objects.create_user(**data)


def get_new_bu(user, country, legal_form, **d):
    """Create and return BusinessUnit"""
    data = {
        'inn': 'INN123456789',
        'ogrn': 'OGRN123456789',
        'first_name': 'Abram',
        'middle_name': 'I',
        'last_name': 'Testman',
        'full_name': 'Abram Isaakovich Testman ibn Hottab',
        'short_name': 'Abram Testman',
        'special_status': False,
        'payment_name': 'Abram_I_Testman',
        'notes': 'Some notes about BU',
    }
    data.update(d)
    return BusinessUnit.objects.create(user=user, country=country, legal_form=legal_form, **data)


def get_new_bank(**d):
    """Create and return Bank"""
    data = {
        'bik': 'QWERTY567890',
        'corr_account': 'CA123467890',
        'name': 'TEST BANK',
        'short_name': 'TEST BANK',
        'swift': 'JUSTSWIFTCODE',
        'notes': 'Some notes about BANK',
    }
    data.update(d)
    return Bank.objects.create(**data)

def get_new_project(beneficiary, **d):
    """Create and return Project"""
    data = {
        'title': 'Test Project',
        'description': 'Some notes about Project',
        'beneficiary': beneficiary,
    }
    data.update(d)
    return Project.objects.create(**data)
