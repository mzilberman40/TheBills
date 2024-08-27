"""
Tests for handbooks models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from handbooks import models


class ModelTests(TestCase):
    """Test models"""


    def test_create_legal_form(self):
        """Test creating a legal form is successful """
        user = get_user_model().objects.create_user(email="test1@example.com",
                                                    password="Password_123")

        short_name = "MyLF"
        full_name = "My Legal Form"
        description = "Description of My Legal Form"
        lf = models.LegalForm.objects.create(
            owner=user,
            short_name=short_name,
            full_name=full_name,
            description=description
        )
        self.assertEqual(full_name, lf.full_name)
        self.assertEqual(short_name, lf.short_name)
        self.assertEqual(description, lf.description)
        self.assertEqual(user.email, lf.owner.email)

    def test_create_cyr_legal_form(self):
        """Test creating a cyrillic legal form is successful """
        user = get_user_model().objects.create_user(email="test1@example.com",
                                                    password="Password_123")

        short_name = "МояФорма"
        full_name = "Моя юридическая форма"
        description = "Описание формы"
        lf = models.LegalForm.objects.create(
            owner=user,
            short_name=short_name,
            full_name=full_name,
            description=description
        )
        self.assertEqual(full_name, lf.full_name)
        self.assertEqual(short_name, lf.short_name)
        self.assertEqual(description, lf.description)
        self.assertEqual(user.email, lf.owner.email)
    # def test_create_ingredient(self):
    #     """Test creating a ingredient is successful """
    #     log_call()
    #
    #     user = get_user_model().objects.create_user(email="test@example.com", password="Password_123")
    #     ingredient = models.Ingredient.objects.create(user=user, name="Salt")
    #     self.assertEqual(str(ingredient), ingredient.name)
