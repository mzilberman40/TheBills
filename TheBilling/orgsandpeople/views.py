
from django.contrib.auth.mixins import LoginRequiredMixin
from commerce.forms import ResourceForm, ContractForm, ServiceForm
from commerce.models import Resource, Contract, Service
from library.Param import Param
from orgsandpeople.forms import BankForm, BusinessUnitForm, AccountForm, PhoneNumberForm, TelegramDataForm, EmailForm
from orgsandpeople.models import Bank, BusinessUnit, Account, PhoneNumber, TelegramData, Email
from utils import (ObjectDetailsMixin, ObjectCreateMixin,
                   ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin)


class OrgsAndPeople(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8


class BusinessUnits(OrgsAndPeople):
    model = BusinessUnit
    form_class = BusinessUnitForm
    title = "Business Units"
    create_url_name = model.CREATE_URL_NAME
    update_url_name = model.UPDATE_URL_NAME
    delete_url_name = model.DELETE_URL_NAME
    list_url_name = model.LIST_URL_NAME
    details_url_name = model.DETAILS_URL_NAME

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
                      'short_name', 'notes', 'address', 'e_mails', 'telegramid']
    fields_to_footer = ['country', 'created', 'modified', 'user']


class BUAccounts(OrgsAndPeople):
    title = "Accounts"
    model = Account
    form_class = AccountForm
    create_url_name = 'orgsandpeople:bu_account_create_url_name'
    update_url_name = 'orgsandpeople:bu_account_update_url_name'
    delete_url_name = 'orgsandpeople:bu_account_delete_url_name'
    list_url_name = 'orgsandpeople:bu_accounts_url_name'
    details_url_name = 'orgsandpeople:bu_account_detail_url_name'

    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    fk_param = Param(field_name='business_unit', key='fkey')
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param

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
    fields_to_header = ['id', 'business_unit', 'bank', 'account_number']
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
    create_url_name = model.CREATE_URL_NAME
    update_url_name = model.UPDATE_URL_NAME
    delete_url_name = model.DELETE_URL_NAME
    list_url_name = model.LIST_URL_NAME
    details_url_name = model.DETAILS_URL_NAME

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
    details_url_name = 'orgsandpeople:bu_resource_detail_url_name'
    fk_param = Param(field_name='business_unit', key='fkey')

    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param

class BUResourceList(BUResources, ObjectsListMixin):
    fields_to_show = ['name', 'rtype', 'current_status']
    query_fields = ['name']
    order_by = 'name'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Resource', 'show': True}

class BUResourceDetails(BUResources, ObjectDetailsMixin):
    edit_button = True
    title = "Resource Details"
    fields_to_header = ['id', 'rtype', 'name', 'business_unit', 'project']
    fields_to_main = [ 'description', 'current_status']
    fields_to_footer = ['created', 'modified', 'user']

class BUResourceCreate(BUResources, ObjectCreateMixin):
    title = "Resource Create"

class BUResourceUpdate(BUResources, ObjectUpdateMixin):
    title = "Updating email"

class BUResourceDelete(BUResources, ObjectDeleteMixin):
    pass


class BUContracts(OrgsAndPeople):
    model = Contract
    form_class = ContractForm
    title = "Contracts"
    create_url_name = 'orgsandpeople:bu_contract_create_url_name'
    update_url_name = 'orgsandpeople:bu_contract_update_url_name'
    delete_url_name = 'orgsandpeople:bu_contract_delete_url_name'
    list_url_name = 'orgsandpeople:bu_contracts_url_name'
    details_url_name = 'orgsandpeople:bu_contract_detail_url_name'
    fk_param = Param(field_name='seller', key='fkey')

    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param

class BUContractList(BUContracts, ObjectsListMixin):
    fields_to_show = ['number', 'title', 'project', 'seller', 'buyer', 'status']
    query_fields = ['title', 'number']
    order_by = 'number'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Contract', 'show': True}

class BUContractDetails(BUContracts, ObjectDetailsMixin):
    edit_button = True
    title = "Contract Details"
    fields_to_header = ['id', 'number', 'title', 'seller', 'buyer', 'status']
    fields_to_main = [ 'description', 'project', 'start_date', 'end_date']
    fields_to_footer = ['created', 'modified', 'user']
    template_name = 'orgsandpeople/contract_details.html'

class BUContractCreate(BUContracts, ObjectCreateMixin):
    title = "Contract Create"

class BUContractUpdate(BUContracts, ObjectUpdateMixin):
    title = "Updating contract"

class BUContractDelete(BUContracts, ObjectDeleteMixin):
    pass


class Services(OrgsAndPeople):
    model = Service
    form_class = ServiceForm
    title = "Services"
    create_url_name = 'orgsandpeople:service_create_url_name'
    update_url_name = 'orgsandpeople:service_update_url_name'
    delete_url_name = 'orgsandpeople:service_delete_url_name'
    list_url_name = 'orgsandpeople:services_url_name'
    details_url_name = 'orgsandpeople:service_detail_url_name'

    fk_param = Param(field_name='contract', key='fkey')

    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param

class ServiceList(Services, ObjectsListMixin):
    fields_to_show = ['service_name', 'resource', 'service_type', 'billing_frequency', 'price', 'currency']
    query_fields = ['service_name',]
    order_by = 'service_name'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Service', 'show': True}

class ServiceDetails(Services, ObjectDetailsMixin):
    edit_button = True
    title = "Service Details"
    fields_to_header = ['id', 'service_name', 'service_type', 'billing_frequency', 'contract', 'resource']
    fields_to_main = [ 'description', 'project', 'price', 'currency']
    fields_to_footer = ['start_time', 'finish_time', 'user']

class ServiceCreate(Services, ObjectCreateMixin):
    title = "Service Create"

class ServiceUpdate(Services, ObjectUpdateMixin):
    title = "Updating service"

class ServiceDelete(Services, ObjectDeleteMixin):
    pass


class Phones(OrgsAndPeople):
    model = PhoneNumber
    form_class = PhoneNumberForm
    title = "Phones"
    create_url_name = 'orgsandpeople:bu_phone_create_url_name'
    update_url_name = 'orgsandpeople:bu_phone_update_url_name'
    delete_url_name = 'orgsandpeople:bu_phone_delete_url_name'
    list_url_name = 'orgsandpeople:bu_phones_url_name'
    details_url_name = 'orgsandpeople:bu_phone_detail_url_name'

    fk_param = Param(field_name='bu', key='fkey')

    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param


class BUPhoneList(Phones, ObjectsListMixin):
    fields_to_show = ['phone_number', 'phone_type', 'bu']
    query_fields = ['phone_number']
    order_by = 'phone_number'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Phone', 'show': True}

class BUPhoneDetails(Phones, ObjectDetailsMixin):
    edit_button = True
    title = "Phone Details"
    fields_to_header = ['id', 'bu']
    fields_to_main = [  'phone_number', 'phone_type', 'is_for_call', 'is_for_SMS', 'is_for_whatsapp']
    fields_to_footer = ['created_at', 'updated_at',]

class BUPhoneCreate(Phones, ObjectCreateMixin):
    title = "Phone Create"

class BUPhoneUpdate(Phones, ObjectUpdateMixin):
    title = "Updating phone"

class BUPhoneDelete(Phones, ObjectDeleteMixin):
    pass


class Emails(OrgsAndPeople):
    model = Email
    form_class = EmailForm
    title = "Emails"
    create_url_name = model.CREATE_URL_NAME
    update_url_name = model.UPDATE_URL_NAME
    delete_url_name = model.DELETE_URL_NAME
    details_url_name = model.DETAILS_URL_NAME

    list_url_name = model.LIST_URL_NAME
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name

class EmailList(Emails, ObjectsListMixin):
    fields_to_show = ['email', 'bu', 'email_type']
    query_fields = ['email']
    order_by = 'email'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}

class EmailDetails(Emails, ObjectDetailsMixin):
    template_name = 'obj_details.html'
    title = f"Email Details"
    fields_to_header = ['id', 'email', 'bu']
    fields_to_main = []
    fields_to_footer = ['email_type']

class EmailCreate(Emails, ObjectCreateMixin):
    title = "Create Email"
    template_name = 'obj_create.html'

class EmailUpdate(Emails, ObjectUpdateMixin):
    title = "Updating Email"

class EmailDelete(Emails, ObjectDeleteMixin):
    title = "Deleting Email"


class BUEmails(OrgsAndPeople):
    model = Email
    form_class = EmailForm
    title = "Emails"
    create_url_name = 'orgsandpeople:bu_email_create_url_name'
    update_url_name = 'orgsandpeople:bu_email_update_url_name'
    delete_url_name = 'orgsandpeople:bu_email_delete_url_name'
    list_url_name = 'orgsandpeople:bu_emails_url_name'
    details_url_name = 'orgsandpeople:bu_email_details_url_name'
    fk_param = Param(field_name='bu', key='fkey')
    # model.fk_param = fk_param
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param

class BUEmailList(BUEmails, ObjectsListMixin):
    fields_to_show = ['email', 'email_type', 'bu']
    query_fields = ['email']
    order_by = 'email'
    template_name = 'obj_list.html'
    # template_name = 'orgsandpeople/email_list.html'
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Email', 'show': True}

class BUEmailDetails(BUEmails, ObjectDetailsMixin):
    edit_button = True
    # template_name = 'orgsandpeople/email_details.html'

    title = "Email Details"
    fields_to_header = ['id', 'bu']
    fields_to_main = [  'email', 'email_type', ]
    fields_to_footer = ['created_at', 'updated_at',]

class BUEmailCreate(BUEmails, ObjectCreateMixin):
    title = "Email Create"

class BUEmailUpdate(BUEmails, ObjectUpdateMixin):
    title = "Updating email"

class BUEmailDelete(BUEmails, ObjectDeleteMixin):
    pass


class BUTelegramData(OrgsAndPeople):
    model = TelegramData
    form_class = TelegramDataForm
    title = "Telegram accounts"
    create_url_name = 'orgsandpeople:bu_telegram_create_url_name'
    update_url_name = 'orgsandpeople:bu_telegram_update_url_name'
    delete_url_name = 'orgsandpeople:bu_telegram_delete_url_name'
    details_url_name = 'orgsandpeople:bu_telegram_detail_url_name'

    list_url_name = 'orgsandpeople:bu_telegrams_url_name'
    fk_param = Param(field_name='bu', key='fkey')

    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    failure_url_name = list_url_name
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param


class BUTelegramDataList(BUTelegramData, ObjectsListMixin):
    fields_to_show = ['tg_id', 'tg_type', 'bu']
    query_fields = ['tg_id', 'tg_name', 'tg_type']
    order_by = 'tg_id'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Telega', 'show': True}

class BUTelegramDataDetails(BUTelegramData, ObjectDetailsMixin):
    edit_button = True
    title = "Telegram account Details"
    fields_to_header = ['id', 'bu']
    fields_to_main = [  'tg_number', 'tg_type']
    fields_to_footer = ['created_at', 'updated_at',]

class BUTelegramDataCreate(BUTelegramData, ObjectCreateMixin):
    title = "Create TG account"

class BUTelegramDataUpdate(BUTelegramData, ObjectUpdateMixin):
    title = "Updating TG account"

class BUTelegramDataDelete(BUTelegramData, ObjectDeleteMixin):
    pass
