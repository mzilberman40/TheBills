"""
Tests for orgsandpeople models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from handbooks.models import Country, LegalForm
from orgsandpeople import models
from tools.name2country import name2country


def create_lf():
    """Create and return Legal Form"""
    data = {
        'short_name': "MyLF",
        'full_name': "My Legal Form",
        'description': "Description of My Legal Form"
    }
    return LegalForm.objects.create(**data)


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

        bik = 'QWERTY567890'
        corr_account = 'CA123467890'
        name = 'TEST BANK'
        short_name = 'TEST BANK'
        swift = 'JUSTSWIFTCODE'
        notes = 'qqqqqqqqqqqqqqqqq'

        bank = models.Bank.objects.create(
            user=self.user,
            country=self.country,
            name=name,
            short_name=short_name,
            swift=swift,
            notes=notes,
            corr_account=corr_account,
            bik=bik
        )

        self.assertEqual(name, bank.name)
        self.assertEqual(short_name, bank.short_name)
        self.assertEqual(swift, bank.swift)
        self.assertEqual(notes, bank.notes)
        self.assertEqual(corr_account, bank.corr_account)
        self.assertEqual(self.user.email, bank.user.email)

    def test_create_bu(self):
        """Test creating a business unit is successful """

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
            'notes': 'Some notes about BU'
        }

        bu = models.BusinessUnit.objects.create(
            user=self.user,
            country=self.country,
            legal_form=create_lf(),
            **data
        )

        self.assertEqual(data['short_name'], bu.short_name)
        self.assertEqual(data['payment_name'], bu.payment_name)
        self.assertEqual(data['full_name'], bu.full_name)
        self.assertEqual(data['special_status'], bu.special_status)
        self.assertEqual(self.user.email, bu.user.email)
