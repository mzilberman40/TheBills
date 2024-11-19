# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from library.testlib import get_new_user, get_new_bu, get_new_country, get_new_legal_form
from orgsandpeople.models import BusinessUnit, Email

User = get_user_model()

class BusinessUnitViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_new_user(email='testuser@example.com', password='password')
        self.country = get_new_country()
        self.legal_form = get_new_legal_form()
        self.business_unit = get_new_bu(user=self.user, country=self.country, legal_form=self.legal_form)
        self.client.login(email='testuser@example.com', password='password')

    # def test_bu_get_list(self):
    #     url = reverse('orgsandpeople:bu_list_url')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #
    # # def test_business_unit_create_view_get(self):
    #     self.client.login(email='testuser@example.com', password='password')
    #     response = self.client.get(reverse('orgsandpeople:bu_create_url'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'obj_create.html')
#
#     def test_business_unit_create_view_post(self):
#         self.client.login(email='testuser@example.com', password='password')
#         data = {
#             'inn': '987654321098',
#             'ogrn': '987654321098765',
#             'first_name': 'New',
#             'last_name': 'Unit',
#             'full_name': 'New Unit',
#             'payment_name': 'NewUnitP',
#             'short_name': 'NewUnit',
#             'legal_form': 101,
#             'country': 1,
#             'emails': 'test@example.com, test2@example.com:type2'
#         }
#         response = self.client.post(reverse('orgsandpeople:bu_create_url'), data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(BusinessUnit.objects.filter(short_name='NewUnit').exists())
#
#     def test_business_unit_update_view_get(self):
#         self.client.login(email='testuser@example.com', password='password')
#         response = self.client.get(reverse('orgsandpeople:bu_update_url', args=[self.business_unit.pk]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'obj_update.html')
#
#     def test_business_unit_update_view_post(self):
#         self.client.login(email='testuser@example.com', password='password')
#         data = {
#             'inn': '123456789012',
#             'ogrn': '123456789012345',
#             'first_name': 'Updated',
#             'last_name': 'Unit',
#             'full_name': 'Updated Unit',
#             'payment_name': 'UpdatedUnitP',
#             'short_name': 'UpdatedUnit',
#             'legal_form': 1,
#             'country': 1,
#             'emails': 'updated@example.com'
#         }
#         response = self.client.post(reverse('orgsandpeople:bu_update_url', args=[self.business_unit.pk]), data)
#         self.assertEqual(response.status_code, 302)
#         self.business_unit.refresh_from_db()
#         self.assertEqual(self.business_unit.first_name, 'Updated')
#         self.assertTrue(Email.objects.filter(email='updated@example.com').exists())