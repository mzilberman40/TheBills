"""
Tests for commerce models
"""
from django.test import TestCase
# from commerce import models
from library.testlib import get_new_user, get_new_bu, get_new_country, get_new_legal_form, get_new_project


class ModelTests(TestCase):
    """Test models"""

    def setUp(self):
        self.user = get_new_user()
        self.country = get_new_country()
        self.legal_form = get_new_legal_form()
        self.beneficiary = get_new_bu(user=self.user, country=self.country, legal_form=self.legal_form)

    def test_create_project(self):
        """Test creating a project is successful """
        d = {
            'title': "My test project",
        }
        project = get_new_project(self.beneficiary, **d)

        self.assertEqual(d['title'], project.title)

