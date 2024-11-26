# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from commerce.models import Project
from library.testlib import get_new_user, get_new_legal_form, get_new_country, get_new_bu, get_new_project

User = get_user_model()

class ProjectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_new_user(email='testuser@example.com', password='password')
        self.legal_form = get_new_legal_form()
        self.country = get_new_country()
        self.beneficiary = get_new_bu(user=self.user, country=self.country, legal_form=self.legal_form)
        self.client.login(email='testuser@example.com', password='password')
        self.project = get_new_project(self.beneficiary)

    def test_project_get_list(self):
        url = reverse('commerce:project_list_url_name')
        template_name = 'obj_list.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_project_create_view_get(self):
        template_name = 'obj_create.html'
        url = reverse('commerce:project_create_url_name')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_project_create_view_post(self):
        data = {
            'title': 'NewProject',
            'description': 'Test project is for test only2',
            'beneficiary': self.beneficiary.pk,
        }
        url = reverse('commerce:project_create_url_name')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title='NewProject').exists())

    def test_project_update_view_get(self):
        template_name = 'obj_update.html'
        url = reverse('commerce:project_update_url_name', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_project_update_view_post(self):
        data = {
            'title': 'UpdatedTitle',
            'description': 'Test project is for test only2',
            'beneficiary': self.beneficiary.pk
        }
        url = reverse('commerce:project_update_url_name', args=[self.project.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, data['title'])

    def test_project_delete_get(self):
        url = reverse('commerce:project_delete_url_name', args=[self.project.pk])
        template_name = 'obj_delete.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def test_project_delete_post(self):
        url = reverse('commerce:project_delete_url_name', args=[self.project.pk])
        self.assertTrue(Project.objects.exists())
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.exists())

    def test_project_details_view_get(self):
        template_name = 'obj_details.html'
        url = 'commerce:project_details_url_name'
        response = self.client.get(reverse(url, args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)


