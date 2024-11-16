from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from orgsandpeople.forms import BusinessUnitForm

User = get_user_model()


# class BusinessUnitFormTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='testuser@example.com', password='password')
#
#     def test_business_unit_form_valid(self):
#         form_data = {
#             'inn': '987654321098',
#             'ogrn': '987654321098765',
#             'first_name': 'New',
#             'last_name': 'Unit',
#             'full_name': 'New Unit',
#             'short_name': 'NewUnit',
#             'payment_name': 'NewUnitP',
#             'legal_form': 1,
#             'country': 1,
#             'emails': 'test@example.com, test2@example.com:type2'
#         }
#         form = BusinessUnitForm(data=form_data, user=self.user)
#         self.assertTrue(form.is_valid())
#
#     def test_business_unit_form_invalid_email(self):
#         form_data = {
#             'inn': '987654321098',
#             'ogrn': '987654321098765',
#             'first_name': 'New',
#             'payment_name': 'NewUnitP',
#             'last_name': 'Unit',
#             'full_name': 'New Unit',
#             'short_name': 'NewUnit',
#             'legal_form': 1,
#             'country': 1,
#             'emails': 'invalid-email'
#         }
#         form = BusinessUnitForm(data=form_data, user=self.user)
#         self.assertFalse(form.is_valid())
#         self.assertIn('emails', form.errors)