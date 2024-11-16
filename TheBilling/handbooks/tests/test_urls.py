from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
import handbooks.views as hview
import handbooks.urls as hurls
from handbooks.models import LegalForm

TEST_USER_PARAMS = {
    'email': 'test1@example.com',
    'password': 'Password_123',
}

TEST_LF_PARAMS1 = {
    'short_name': 'LForm1',
    'full_name': 'Test Legal Form1',
    'description': 'Test Legal Form1 Description',
}

TEST_LF_PARAMS2 = {
    'short_name': 'LForm2',
    'full_name': 'Test Legal Form2',
    'description': 'Test Legal Form2 Description',
}

class TestUrlsLegalForm(TestCase):
    def setUp(self):
        create_function_name = 'handbooks:legal_form_create_url'
        update_function_name = 'handbooks:legal_form_update_url'
        delete_function_name = 'handbooks:legal_form_delete_url'
        list_function_name = 'handbooks:legal_forms_list_url'

        self.user = get_user_model().objects.create_user(**TEST_USER_PARAMS)
        LegalForm.objects.create(**TEST_LF_PARAMS1)
        LegalForm.objects.create(**TEST_LF_PARAMS2)
        self.list_url = reverse(list_function_name)

    def test_legal_form_list_urls_if_not_logged_in(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    # def test_legal_form_list_urls_success(self):
    #     self.client.login(**TEST_USER_PARAMS)
    #     response = self.client.get(self.list_url)
    #     template = 'obj_list.html'
    #     self.assertTemplateUsed(response, template)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_legal_form_returns_lf_list(self):
        self.client.login(**TEST_USER_PARAMS)
        template = 'obj_list.html'

        response = self.client.get(self.list_url)
        self.assertTemplateUsed(response, template)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, TEST_LF_PARAMS1['short_name'])
        self.assertContains(response, TEST_LF_PARAMS2['short_name'])






