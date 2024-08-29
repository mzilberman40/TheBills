"""
Tests for handbooks models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from tools.from_moneyed import code2currency
from tools.name2country import name2country

from handbooks import models


class ModelTests(TestCase):
    """Test models"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test1@example.com",
                                                password="Password_123")

    def test_create_legal_form(self):
        """Test creating a legal form is successful """

        short_name = "MyLF"
        full_name = "My Legal Form"
        description = "Description of My Legal Form"
        lf = models.LegalForm.objects.create(
            short_name=short_name,
            full_name=full_name,
            description=description
        )
        self.assertEqual(full_name, lf.full_name)
        self.assertEqual(short_name, lf.short_name)
        self.assertEqual(description, lf.description)

    def test_resource_group(self):
        """Test creating a resource group is successful """

        name = "МояФорма"
        description = "Тестовая группа ресурсов"
        rg = models.ResourceGroup.objects.create(
            name=name,
            description=description
        )
        self.assertEqual(name, rg.name)
        self.assertEqual(description, rg.description)

    def test_create_resource_name(self):
        """Test creating a ResourceName is successful """
        name = "МояФорма"
        description = "Тестовая группа ресурсов"
        rg = models.ResourceGroup.objects.create(
            name=name,
            description=description
        )

        name = "Мой ресурс"
        description = "My Resource Name"
        rn = models.ResourceName.objects.create(
            name=name,
            description=description,
            group=rg
        )
        self.assertEqual(name, rn.name)
        self.assertEqual(description, rn.description)
        self.assertEqual(rg, rn.group)

    def test_currency(self):
        """Test creating a currency is successful """

        code = "USD"
        data = code2currency(code)
        # print(code, data)
        cur = models.Currency.objects.create(**data)
        self.assertEqual(data['name'], cur.name)
        self.assertEqual(data['code'], cur.code)
        self.assertEqual(data['numeric'], cur.numeric)

    def test_country(self):
        """Test creating a country is successful """

        eng_name = "Israel"
        data = name2country(eng_name)
        # print(data)
        country = models.Country.objects.create(**data)
        self.assertEqual(data['eng_name'], country.eng_name)
        self.assertEqual(data['rus_name'], country.rus_name)
        self.assertEqual(data['eng_name_official'], country.eng_name_official)

