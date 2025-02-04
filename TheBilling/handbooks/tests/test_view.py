# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from handbooks.models import LegalForm
from handbooks.views import LegalForms

User = get_user_model()

class LegalFormsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@example.com', password='password')
        self.legal_form = LegalForm.objects.create(
            short_name='TestLegalForm',
            full_name='Test Legal Form',
            description='Test Legal Form is for test only',
        )
        self.client.login(email='testuser@example.com', password='password')

    def test_lf_get_list(self):
        template_name = 'obj_list.html'
        url_name = LegalForm.LIST_URL_NAME
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_lf_create_view_get(self):
        template_name = 'obj_create.html'
        url_name = LegalForm.CREATE_URL_NAME
        response = self.client.get(reverse(url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_lf_create_view_post(self):
        data = {
            'short_name': 'NewUnit',
            'full_name': 'Test Legal Form1',
            'description': 'Test Legal Form is for test only2',
        }
        url_name = LegalForm.CREATE_URL_NAME
        url = reverse(url_name)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LegalForm.objects.filter(short_name='NEWUNIT').exists())

    def test_lf_update_view_get(self):
        template_name = 'obj_update.html'
        url_name = LegalForm.UPDATE_URL_NAME
        response = self.client.get(reverse(url_name, args=[self.legal_form.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_lf_update_view_post(self):
        url_name = LegalForm.UPDATE_URL_NAME
        data = {
            'short_name': 'UpdatedUnit',
            'full_name': 'Test Legal Form2 Updated',
            'description': 'Test Legal Form is for test only2',
        }
        response = self.client.post(reverse(url_name, args=[self.legal_form.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.legal_form.refresh_from_db()
        self.assertEqual(self.legal_form.short_name, 'UPDATEDUNIT')

    def test_lf_delete_view_get(self):
        url_name = LegalForm.DELETE_URL_NAME
        template_name = 'obj_delete.html'
        response = self.client.get(reverse(url_name, args=[self.legal_form.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_lf_delete_view_post(self):
        url_name = LegalForm.DELETE_URL_NAME
        self.assertTrue(LegalForm.objects.exists())
        response = self.client.post(reverse(url_name, args=[self.legal_form.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(LegalForm.objects.exists())

    def test_lf_details_view_get(self):
        template_name = 'obj_details.html'
        url_name = LegalForm.DETAILS_URL_NAME
        response = self.client.get(reverse(url_name, args=[self.legal_form.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
