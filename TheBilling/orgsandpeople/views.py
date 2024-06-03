from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from orgsandpeople.forms import EmailForm, BusinessUnitForm
from orgsandpeople.models import Email, BusinessUnit
from utils import ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin


class OrgsAndPeople(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8


class BusinessUnits(OrgsAndPeople):
    model = BusinessUnit
    form_model = BusinessUnitForm
    title = "Business Units"
    create_function_name = 'orgsandpeople:bu_create_url'
    update_function_name = 'orgsandpeople:bu_update_url'
    delete_function_name = 'orgsandpeople:bu_delete_url'
    list_function_name = 'orgsandpeople:bu_list_url'
    redirect_to = list_function_name


class BusinessUnitList(BusinessUnits, ObjectsListMixin, View):
    fields_toshow = ['full_name', 'payment_name']
    query_fields = ['full_name', 'payment_name']
    order_by = 'full_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}


class BusinessUnitCreate(BusinessUnits, ObjectCreateMixin, View):
    title = "Create BusinessUnit"


class BusinessUnitUpdate(BusinessUnits, ObjectUpdateMixin, View):
    title = "Updating BusinessUnit"


class BusinessUnitDelete(BusinessUnits, ObjectDeleteMixin, View):
    title = "Deleting BusinessUnit"


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
