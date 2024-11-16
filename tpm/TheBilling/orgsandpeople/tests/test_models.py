"""
Tests for orgsandpeople models
"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from handbooks.models import Country, LegalForm
from handbooks.tests.test_models import create_legal_form
from orgsandpeople import models
from orgsandpeople.models import Email
from tools.name2country import name2country


def create_bank(**d):
    """Create and return Bank"""
    data = {
        'bik': 'QWERTY567890',
        'corr_account': 'CA123467890',
        'name': 'TEST BANK',
        'short_name': 'TEST BANK',
        'swift': 'JUSTSWIFTCODE',
        'notes': 'qqqqqqqqqqqqqqqqq',
    }
    data.update(d)
    return models.Bank.objects.create(**data)


def create_bu(**d):
    """Create and return BusinessUnit"""
    data = {
        'inn': 'INNN567890',
        'ogrn': 'OGRN567890',
        'first_name': 'Abram',
        'middle_name': 'I',
        'last_name': 'Ivanov',
        'full_name': 'Abram Isakovich Ivanov ibn Hottab',
        'short_name': 'Abram Ivanov',
        'special_status': False,
        'payment_name': 'Abram_I_Ivanov',
        'notes': 'Some notes about BU',
        'legal_form': create_legal_form(),
        'country': Country.objects.first(),
    }
    data.update(d)
    return models.BusinessUnit.objects.create(**data)


class ModelTests(TestCase):
    """Test models"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test1@example.com",
                                                password="Password_123")
        eng_name = "Israel"
        data = name2country(eng_name)
        self.country = Country.objects.create(**data)

    def test_create_bank(self):
        """Test creating a bank is successful """

        data = {
            'user': self.user,
            'corr_account': 'CA123467890',
            'name': 'TEST BANK',
            'country': self.country,
            'swift': 'JUSTSWIFTCODE',
            'notes': 'qqqqqqqqqqqqqqqqq',

        }
        bank = create_bank(**data)

        self.assertEqual(data['name'], bank.name)
        self.assertEqual(data['corr_account'], bank.corr_account)
        self.assertEqual(self.user.email, bank.user.email)

    def test_create_bu(self):
        """Test creating a business unit is successful """

        data = {
            'inn': 'INNN567890',
            'full_name': 'Abram Isakovich Ivanov ibn Hottab',
            'special_status': False,
            'payment_name': 'Abram_I_Ivanov',
            'user': self.user,
            'country': self.country,
        }

        bu = create_bu(**data)

        self.assertEqual(data['inn'], bu.inn)
        self.assertEqual(data['payment_name'], bu.payment_name)
        self.assertEqual(data['full_name'], bu.full_name)
        self.assertEqual(data['special_status'], bu.special_status)
        self.assertEqual(self.user.email, bu.user.email)

    def test_create_email(self):
        """Test creating an email is successful """
        bu_data = {
            'user': self.user,
            'country': self.country,
        }
        bu = create_bu(**bu_data)

        data = {
            'bu': bu,
            'email': 'test1@example.com',
            'email_type': 'Private',
        }

        email = Email.objects.create(**data)

        self.assertEqual(data['email'], email.email)
        self.assertEqual(data['email_type'], email.email_type)

    def test_create_not_email_format(self):
        """Test creating an email with wrong email format is unsuccessful """
        bu_data = {
            'user': self.user,
            'country': self.country,
        }
        bu = create_bu(**bu_data)

        data = {
            'bu': bu,
            'email': 'test1.example.com',
            'email_type': 'Private',
        }

        with self.assertRaises(ValidationError):
            Email.objects.create(**data)

