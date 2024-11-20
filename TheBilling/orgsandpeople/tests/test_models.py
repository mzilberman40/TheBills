"""
Tests for orgsandpeople models
"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from library.testlib import get_new_user, get_new_bank, get_new_bu, get_new_legal_form, get_new_country
from orgsandpeople.models import Email


class ModelTests(TestCase):
    """Test models"""

    def setUp(self):
        self.user = get_new_user()
        self.country = get_new_country()
        self.legal_form = get_new_legal_form()

    def test_create_bank(self):
        """Test creating a bank is successful """

        data = {
            'user': self.user,
            'corr_account': 'CA123467890',
            'name': 'TEST BANK'
        }
        bank = get_new_bank(**data)
        self.assertEqual(data['name'], bank.name)
        self.assertEqual(data['corr_account'], bank.corr_account)
        self.assertEqual(self.user.email, bank.user.email)

    def test_create_bu(self):
        """Test creating a business unit is successful """

        data = {
            'inn': 'INN567890',
            'full_name': 'Abram Isaakovich Ivanov ibn Hottab',
            'special_status': False,
            'payment_name': 'Abram_I_Ivanov',
        }

        bu = get_new_bu(user=self.user, country=self.country, legal_form=self.legal_form, **data)

        self.assertEqual(data['inn'], bu.inn)
        self.assertEqual(data['payment_name'], bu.payment_name)
        self.assertEqual(data['full_name'], bu.full_name)
        self.assertEqual(data['special_status'], bu.special_status)
        self.assertEqual(self.user.email, bu.user.email)

    def test_create_email(self):
        """Test creating an email is successful """
        bu = get_new_bu(user=self.user, country=self.country, legal_form=self.legal_form)
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

        bu = get_new_bu(user=self.user, country=self.country, legal_form=self.legal_form)

        data = {
            'bu': bu,
            'email': 'test1.example.com',
            'email_type': 'Private',
        }

        with self.assertRaises(ValidationError):
            Email.objects.create(**data)
