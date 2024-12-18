
from django.contrib.auth.mixins import LoginRequiredMixin
from commerce.forms import ResourceForm
from commerce.models import Resource
from library.Param import Param
from orgsandpeople.forms import BankForm, BusinessUnitForm, AccountForm
from orgsandpeople.models import Bank, BusinessUnit, Account
from utils import (ObjectDetailsMixin, ObjectCreateMixin,
                   ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin)


class OrgsAndPeople(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8

class BusinessUnits(OrgsAndPeople):
    model = BusinessUnit
    form_class = BusinessUnitForm
    title = "Business Units"
    create_url_name = 'orgsandpeople:bu_create_url_name'
    update_url_name = 'orgsandpeople:bu_update_url_name'
    details_url_name = 'orgsandpeople:bu_details_url_name'
    delete_url_name = 'orgsandpeople:bu_delete_url_name'
    list_url_name = 'orgsandpeople:bu_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name


class BusinessUnitList(BusinessUnits, ObjectsListMixin):
    fields_to_show = ['full_name', 'payment_name']
    query_fields = ['full_name', 'payment_name']
    order_by = 'full_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True,}


class BusinessUnitCreate(BusinessUnits, ObjectCreateMixin):
    title = "Create BusinessUnit"
    fields_to_fill = ['inn', 'ogrn', 'first_name', 'middle_name', 'last_name',
                      'full_name', 'short_name', 'emails', 'special_status',
                      'payment_name', 'legal_form', 'notes', 'country']
    template_name = 'obj_create.html'

class BusinessUnitUpdate(BusinessUnits, ObjectUpdateMixin):
    title = "Updating BusinessUnit"
    template_name = 'obj_update.html'

class BusinessUnitDelete(BusinessUnits, ObjectDeleteMixin):
    title = "Deleting BusinessUnit"


class BusinessUnitDetails(BusinessUnits, ObjectDetailsMixin):
    template_name = 'orgsandpeople/bu_details.html'
    title = f"Business Unit Details"
    fields_to_header = ['id', 'inn', 'slug', 'payment_name', 'special_status']
    fields_to_main = ['legal_form', 'first_name', 'middle_name', 'last_name', 'full_name',
                      'short_name', 'notes', 'e_mails']
    fields_to_footer = ['country', 'created', 'modified', 'user']


class BUAccounts(OrgsAndPeople):
    title = "Accounts"
    model = Account
    form_class = AccountForm
    create_url_name = 'orgsandpeople:bu_account_create_url_name'
    update_url_name = 'orgsandpeople:bu_account_update_url_name'
    delete_url_name = 'orgsandpeople:bu_account_delete_url_name'
    list_url_name = 'orgsandpeople:bu_accounts_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = Param(field='business_unit', key='bu_pk')
    redirect_param = Param(field='business_unit_id', key='bu_pk')

class BUAccountList(BUAccounts, ObjectsListMixin):
    template_name = 'obj_list.html'
    fields_to_show = ['name', 'bank', 'balance', 'currency']
    query_fields = ['name']
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Account', 'show': True}


class BUAccountDetail(BUAccounts, ObjectDetailsMixin):
    title = f"Account Details"
    fields_to_header = ['id', 'business_unit', 'bank', 'account_namber']
    fields_to_main = ['balance', 'currency', 'starting_balance', 'notes']
    fields_to_footer = ['status', 'activate_date', 'deactivate_date']


class BUAccountCreate(BUAccounts, ObjectCreateMixin):
    title = f"Creating account..."
    fields_to_fill = ['name', 'bank', 'currency', 'account_number',
                      'starting_balance', 'status', 'notes']
    create_url_name = 'orgsandpeople:bu_account_create_url_name'

class BUAccountDelete(BUAccounts, ObjectDeleteMixin):
    title = "Deleting Account"

class BUAccountUpdate(BUAccounts, ObjectUpdateMixin):
    title = "Updating Account"

class Banks(OrgsAndPeople):
    model = Bank
    form_class = BankForm

    title = "Banks"
    create_url_name = 'orgsandpeople:bank_create_url_name'
    update_url_name = 'orgsandpeople:bank_update_url_name'
    delete_url_name = 'orgsandpeople:bank_delete_url_name'
    list_url_name = 'orgsandpeople:bank_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name


class BankList(Banks, ObjectsListMixin):
    fields_to_show = ['short_name', 'bik', 'swift']
    query_fields = ['short_name', 'name', 'bik', 'swift']
    order_by = 'short_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}


class BankDetails(Banks, ObjectDetailsMixin):
    template_name = 'obj_details.html'
    title = f"Bank Details"
    fields_to_header = ['id', 'short_name', 'name', 'slug']
    fields_to_main = ['bik', 'corr_account', 'swift', 'country', 'notes']
    fields_to_footer = ['created', 'modified', 'user']


class BankCreate(Banks, ObjectCreateMixin):
    title = "Create Bank"
    template_name = 'obj_create.html'


class BankUpdate(Banks, ObjectUpdateMixin):
    title = "Updating Bank"


class BankDelete(Banks, ObjectDeleteMixin):
    title = "Deleting Bank"


class BUResources(OrgsAndPeople):
    model = Resource
    form_class = ResourceForm
    title = "Resources"
    create_url_name = 'orgsandpeople:bu_resource_create_url_name'
    update_url_name = 'orgsandpeople:bu_resource_update_url_name'
    delete_url_name = 'orgsandpeople:bu_resource_delete_url_name'
    list_url_name = 'orgsandpeople:bu_resources_url_name'

    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = Param(field='business_unit', key='bu_pk')
    redirect_param = Param(field='business_unit_id', key='bu_pk')


class BUResourceList(BUResources, ObjectsListMixin):
    fields_to_show = ['name', 'rtype', 'available']
    query_fields = ['name']
    order_by = 'name'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Account', 'show': True}


class BUResourceDetails(BUResources, ObjectDetailsMixin):
    edit_button = True
    title = "Resource Details"
    fields_to_header = ['id', 'rtype', 'name', 'business_unit']
    fields_to_main = [ 'description', 'available']
    fields_to_footer = ['created', 'modified', 'user']


class BUResourceCreate(BUResources, ObjectCreateMixin):
    title = "Resource Create"


class BUResourceUpdate(BUResources, ObjectUpdateMixin):
    title = "Updating email"


class BUResourceDelete(BUResources, ObjectDeleteMixin):
    pass
