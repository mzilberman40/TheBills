from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from commerce.models import Email, Account, BusinessUnit
from utils import ObjectsListMixin, ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin


class Commerce(LoginRequiredMixin):
    base_app_template = 'commerce/base_orgs_and_people.html'
    raise_exception = True
    objects_per_page = 8
    edit_button = False
    delete_button = False
    view_button = False


class Emails(Commerce):
    model = Email
    form_model = EmailForm
    title = "Emails"
    create_function_name = 'email_create_url'
    update_function_name = 'email_update_url'
    delete_function_name = 'email_delete_url'
    list_function_name = 'emails_list_url'
    redirect_to = list_function_name


class EmailsList(Emails, ObjectsListMixin, View):
    fields_toshow = ['email']
    query_fields = ['email']
    order_by = 'email'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True


class EmailDetails(Emails, ObjectDetailsMixin, View):
    title = "Email Details"
    template_name = 'obj_list.html'


class EmailCreate(Emails, ObjectCreateMixin, View):
    title = "Email Create"


class EmailUpdate(Emails, ObjectUpdateMixin, View):
    title = "Updating email"


class EmailDelete(Emails, ObjectDeleteMixin, View):
    pass


class BusinessUnits(Commerce):
    model = BusinessUnit
    form_model = BusinessUnitForm
    title = "Business Units"
    create_function_name = 'business_unit_create_url'
    update_function_name = 'business_unit_update_url'
    delete_function_name = 'business_unit_delete_url'
    list_function_name = 'business_units_list_url'
    redirect_to = list_function_name
    objects_per_page = 7


class BusinessUnitsList(BusinessUnits, ObjectsListMixin, View):
    fields_toshow = ['full_name', 'legal_form', 'inn', 'short_name', 'payment_name']
    query_fields = ['full_name', 'short_name', 'inn', 'payment_name']
    order_by = 'full_name'
    template_name = 'obj_list.html'
    view_button = True


class BusinessUnitCreate(BusinessUnits, ObjectCreateMixin, View):
    title = "Business Unit Create"


class BusinessUnitUpdate(BusinessUnits, ObjectUpdateMixin, View):
    title = "Updating business unit"


class BusinessUnitDelete(BusinessUnits, ObjectDeleteMixin, View):
    title = "Deleting business unit"


class BusinessUnitDetails(BusinessUnits, ObjectDetailsMixin, View):
    title = "Business unit details"
    fields_to_header = ['id', 'inn', 'ogrn', 'short_name']
    field_to_top_main = 'payment_name'
    fields_to_main = ['legal_form', 'first_name', 'middle_name', 'last_name', 'full_name', 'address', 'note']
    fields_to_footer = ['date_updated']


class Accounts(Commerce):
    model = Account
    form_model = AccountForm
    title = "Accounts"
    create_function_name = 'account_create_url'
    update_function_name = 'account_update_url'
    delete_function_name = 'account_delete_url'
    list_function_name = 'accounts_list_url'
    redirect_to = list_function_name


class AccountsList(Accounts, ObjectsListMixin, View):
    fields_toshow = ['bank', 'number', 'currency', 'business_unit']
    query_fields = ['number', 'business_unit']
    order_by = 'business_unit'
    view_button = False


class AccountDetails(Accounts, ObjectDetailsMixin, View):
    title = "Account Details"
    template_name = 'obj_list.html'


class AccountCreate(Accounts, ObjectCreateMixin, View):
    title = "Account Create"


class AccountUpdate(Accounts, ObjectUpdateMixin, View):
    title = "Updating account"


class AccountDelete(Accounts, ObjectDeleteMixin, View):
    pass
