"""
Tests for handbooks models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from library.testlib import get_new_legal_form
from tools.from_moneyed import code2currency
from tools.name2country import name2country

from handbooks import models


# def create_legal_form(**d):
#     """Create and return Legal Form"""
#     data = {
#         'short_name': "MyLF",
#         'full_name': "My Legal Form",
#         'description': "Description of My Legal Form"
#     }
#     data.update(d)
#     return models.LegalForm.objects.create(**data)


class ModelTests(TestCase):
    """Test models"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test1@example.com",
                                                password="Password_123")

    def test_create_legal_form(self):
        """Test creating a legal form is successful """
        d = {
            'full_name': "My The Best Legal Form",
        }
        lf = get_new_legal_form(**d)

        self.assertEqual(d['full_name'], lf.full_name)

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

    def test_create_resource_type(self):
        """Test creating a ResourceType is successful """
        name = "МояГруппаРесурсов"
        description = "Тестовая группа ресурсов"
        rg = models.ResourceGroup.objects.create(
            name=name,
            description=description
        )

        rtype = "Мой ресурс"
        description = "My Resource Name"
        rn = models.ResourceType.objects.create(
            rtype=rtype,
            description=description,
            group=rg
        )
        self.assertEqual(rtype, rn.rtype)
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

