from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from orgsandpeople.forms import EmailForm
from orgsandpeople.models import Email
from utils import ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin


class OrgsAndPeople(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8


class Emails(OrgsAndPeople):
    model = Email
    form_model = EmailForm
    title = "Legal Forms"
    create_function_name = 'orgsandpeople:email_create_url'
    update_function_name = 'orgsandpeople:email_update_url'
    delete_function_name = 'orgsandpeople:email_delete_url'
    list_function_name = 'orgsandpeople:emails_list_url'
    redirect_to = list_function_name


class EmailsList(Emails, ObjectsListMixin, View):
    fields_toshow = ['email',]
    query_fields = ['email',]
    order_by = 'email'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}


class EmailCreate(Emails, ObjectCreateMixin, View):
    title = "Email Create"


class EmailUpdate(Emails, ObjectUpdateMixin, View):
    title = "Updating email"


class EmailDelete(Emails, ObjectDeleteMixin, View):
    title = "Deleting email"
