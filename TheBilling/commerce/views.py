from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.paginator import Paginator
# from django.http import HttpResponse
# from django.shortcuts import render, get_object_or_404
# from django.urls import reverse_lazy
# from django.views import View

from commerce.forms import *
from commerce.models import *
from library.Param import Param
# from library.inject_values import inject_values
from utils import ObjectsListMixin, ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin


class Commerce(LoginRequiredMixin):
    # base_app_template = 'commerce/base_orgs_and_people.html'
    raise_exception = True
    objects_per_page = 8

class Projects(Commerce):
    model = Project
    form_class = ProjectForm
    title = "Projects"
    create_url_name = model.CREATE_URL_NAME
    update_url_name = model.UPDATE_URL_NAME
    delete_url_name = model.DELETE_URL_NAME
    details_url_name = model.DETAILS_URL_NAME
    list_url_name = model.LIST_URL_NAME
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name

class ProjectList(Projects, ObjectsListMixin):
    fields_to_show = ['title', 'beneficiary']
    query_fields = ['title']
    order_by = 'title'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}
    edit_button = True
    view_button = True
    delete_button = True

class ProjectDetails(Projects, ObjectDetailsMixin):
    title = f"Project Details"
    fields_to_header = ['id', 'title', 'beneficiary']
    fields_to_main = ['description']
    fields_to_footer = []

class ProjectCreate(Projects, ObjectCreateMixin):
    title = "Project Create"

class ProjectUpdate(Projects, ObjectUpdateMixin):
    title = "Updating Project"

class ProjectDelete(Projects, ObjectDeleteMixin):
    template_name = 'obj_delete.html'
    title = "Deleting Project"


class Contracts(Commerce):
    model = Contract
    form_class = ContractForm
    title = "Contracts"
    create_url_name = model.CREATE_URL_NAME
    update_url_name = model.UPDATE_URL_NAME
    delete_url_name = model.DELETE_URL_NAME
    details_url_name = model.DETAILS_URL_NAME
    list_url_name = model.LIST_URL_NAME
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name

class ContractList(Contracts, ObjectsListMixin):
    fields_to_show = ['number', 'title', 'seller', 'buyer', 'project', 'status']
    query_fields = ['title', 'number', 'seller__payment_name', 'buyer__payment_name']
    order_by = 'number'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}
    edit_button = True
    view_button = True
    delete_button = True

class ContractDetails(Contracts, ObjectDetailsMixin):
    template_name = 'commerce/contract_details.html'

    title = f"Contract Details"
    fields_to_header = ['id', 'title', 'number', 'seller', 'buyer', 'project',]
    fields_to_main = ['description']
    fields_to_footer = ['status', 'start_date', 'end_date', 'user', 'created', 'modified']

class ContractCreate(Contracts, ObjectCreateMixin):
    title = "Contract Create"

class ContractUpdate(Contracts, ObjectUpdateMixin):
    title = "Updating Contract"

class ContractDelete(Contracts, ObjectDeleteMixin):
    template_name = 'obj_delete.html'
    title = "Deleting Contract"

class Services(Commerce):
    model = Service
    form_class = ServiceForm
    title = "Services"
    create_url_name = model.CREATE_URL_NAME
    update_url_name = model.UPDATE_URL_NAME
    delete_url_name = model.DELETE_URL_NAME
    details_url_name = model.DETAILS_URL_NAME
    list_url_name = model.LIST_URL_NAME
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name

class ServiceList(Services, ObjectsListMixin):
    fields_to_show = ['contract', 'service_name', 'resource', 'price', 'currency']
    query_fields = ['service_name']
    order_by = 'service_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}
    edit_button = True
    view_button = True
    delete_button = True

class ServiceDetails(Services, ObjectDetailsMixin):
    template_name = 'commerce/service_details.html'
    title = f"Service Details"
    fields_to_header = ['id', 'contract', 'service_name', 'service_type', 'status']
    fields_to_main = ['billing_frequency', 'price', 'currency', 'resource', 'description']
    fields_to_footer = ['start_date', 'finish_date', 'user', 'created_at', 'updated_at']

class ServiceCreate(Services, ObjectCreateMixin):
    title = "Service Create"

class ServiceUpdate(Services, ObjectUpdateMixin):
    title = "Updating Service"

class ServiceDelete(Services, ObjectDeleteMixin):
    template_name = 'obj_delete.html'
    title = "Deleting Service"


class ServicePrices(Commerce):
    model = ServicePrice
    form_class = ServicePriceForm
    title = "Service Prices"
    create_url_name = 'commerce:service_price_create_url_name'
    # update_url_name = 'commerce:service_price_update_url_name'
    delete_url_name = 'commerce:service_price_delete_url_name'
    details_url_name = model.DETAILS_URL_NAME
    fk_param = Param(field_name='service', key='fkey')
    filter_param = fk_param
    redirect_param = fk_param
    create_param = fk_param
    list_url_name = 'commerce:service_price_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name

class ServicePricesList(ServicePrices, ObjectsListMixin):
    fields_to_show = ['created_at', 'user', 'price', 'currency', 'start_date', 'end_date']
    query_fields = []
    order_by = '-created_at'
    template_name = 'commerce/service_price_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}
    edit_button = False
    view_button = False
    delete_button = True

class ServicePriceDelete(ServicePrices, ObjectDeleteMixin):
    template_name = 'obj_delete.html'
    title = "Deleting price"

class ServicePriceCreate(ServicePrices, ObjectCreateMixin):
    title = "ServicePrice Create"

class ServicePriceUpdate(ServicePrices, ObjectUpdateMixin):
    title = "Updating Price"

class ContractServices(Commerce):
    model = Service
    form_class = ServiceForm
    title = "Services"
    create_url_name = 'commerce:contract_service_create_url_name'
    update_url_name = 'commerce:contract_service_update_url_name'
    delete_url_name = 'commerce:contract_service_delete_url_name'
    details_url_name = 'commerce:contract_service_detail_url_name'
    fk_param = Param(field_name='contract', key='fkey')
    list_url_name = 'commerce:contract_service_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    filter_param = fk_param
    create_param = fk_param
    redirect_param = fk_param
    fk_params = []

class ContractServiceList(ContractServices, ObjectsListMixin):
    fields_to_show = ['contract', 'service_name', 'resource', 'price', 'currency']
    query_fields = ['service_name']
    order_by = 'service_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}
    edit_button = True
    view_button = True
    delete_button = True

class ContractServiceDetails(ContractServices, ObjectDetailsMixin):
    title = f"Service Details"
    fields_to_header = ['id', 'contract', 'service_name', 'service_type', 'status']
    fields_to_main = ['billing_frequency', 'price', 'currency', 'resource', 'description']
    fields_to_footer = ['start_date', 'finish_date', 'user', 'created_at', 'updated_at']

class ContractServiceCreate(ContractServices, ObjectCreateMixin):
    title = "Service Create"

class ContractServiceUpdate(ContractServices, ObjectUpdateMixin):
    title = "Updating Service"

class ContractServiceDelete(ContractServices, ObjectDeleteMixin):
    template_name = 'obj_delete.html'
    title = "Deleting Service"

