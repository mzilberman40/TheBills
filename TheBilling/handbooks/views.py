from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from tools.from_moneyed import code2currency
from tools.name2country import name2country
from handbooks.forms import LegalFormForm, CountryForm, CurrencyForm, ResourceGroupForm, ResourceTypeForm
from handbooks.models import LegalForm, Country, Currency, ResourceGroup, ResourceType
from utils import (ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin,
                   ObjectDeleteMixin, ObjectsListMixin)


class Handbooks(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8


class LegalForms(Handbooks):
    model = LegalForm
    # form_model = LegalFormForm
    form_class = LegalFormForm
    fields = None
    title = "Legal Forms"
    create_url_name = 'handbooks:legal_form_create_url_name'
    update_url_name = 'handbooks:legal_form_update_url_name'
    delete_url_name = 'handbooks:legal_form_delete_url_name'
    list_url_name = 'handbooks:legal_forms_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name


class LegalFormsList(LegalForms, ObjectsListMixin):
    context_object_name = "legal_forms"
    template_name = "obj_list.html"
    fields_to_show = ['short_name', 'full_name']
    query_fields = ['short_name', 'full_name']
    nav_custom_button = {'name': 'NewItem', 'show': True}


class LegalFormDetails(LegalForms, ObjectDetailsMixin):
    title = f"Legal Form"
    fields_to_header = ['id', 'short_name', 'full_name']
    fields_to_main = ['description']
    fields_to_footer = ['time_create', 'time_update', 'owner']


class LegalFormCreate(LegalForms, ObjectCreateMixin):
    title = "Legal Form Create"


class LegalFormUpdate(LegalForms, ObjectUpdateMixin):
    title = "Updating legal form"

class LegalFormDelete(LegalForms, ObjectDeleteMixin):
    title = "Deleting legal form"

class ResourceGroups(Handbooks):
    model = ResourceGroup
    form_class = ResourceGroupForm
    title = "Resource Group"
    create_url_name = 'handbooks:res_group_create_url_name'
    update_url_name = 'handbooks:res_group_update_url_name'
    delete_url_name = 'handbooks:res_group_delete_url_name'
    list_url_name = 'handbooks:res_group_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name

class ResourceGroupList(ResourceGroups, ObjectsListMixin):
    context_object_name = "legal_forms"
    fields_to_show = ['name']
    query_fields = ['name', 'description']
    order_by = 'name'
    template_name = "obj_list.html"
    nav_custom_button = {'name': 'NewItem', 'show': True}

class ResourceGroupDetails(ResourceGroups, ObjectDetailsMixin):
    fields_to_header = ['id', 'name',]
    fields_to_main = ['description']
    fields_to_footer = ['time_create', 'time_update', 'owner']


class ResourceGroupCreate(ResourceGroups, ObjectCreateMixin):
    title = "Resource Group Create"


class ResourceGroupUpdate(ResourceGroups, ObjectUpdateMixin):
    title = "Updating Resource Group"


class ResourceGroupDelete(ResourceGroups, ObjectDeleteMixin):
    title = "Deleting Resource Group"


class Countries(Handbooks):
    model = Country
    objects_per_page = 10
    form_model = CountryForm
    form_class = CountryForm

    title = "Countries"
    create_url_name = 'handbooks:country_create_url_name'
    update_url_name = 'handbooks:country_update_url_name'
    delete_url_name = 'handbooks:country_delete_url_name'
    list_url_name = 'handbooks:countries_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name



class CountriesList(Countries, ObjectsListMixin):
    fields_to_show = ['iso3166', 'eng_name', 'rus_name', 'alfa2']
    query_fields = ['eng_name', 'rus_name', 'iso3166', 'alfa2', 'alfa3']
    order_by = 'eng_name'
    template_name = 'obj_list.html'
    edit_button = False
    delete_button = True
    nav_custom_button = {'name': 'NewItem', 'show': True}


class CountryDetails(Countries, ObjectDetailsMixin):
    title = "Country Details"
    fields_to_header = ['iso3166', 'alfa2', 'alfa3']
    fields_to_main = ['eng_name', 'eng_name_official', 'rus_name', 'rus_name_short', 'rus_name_official']
    fields_to_footer = ['time_create', 'time_update', 'owner']
    edit_button = False
    delete_button = False


class CountryCreate(Countries, ObjectCreateMixin):
    title = "Create country"
    fields_to_fill = ['eng_name']

    def post(self, request, **kwargs):
        data = request.POST.copy()
        eng_name = data['eng_name']
        data.update(name2country(eng_name))
        bound_form = self.form_model(data)

        if bound_form.is_valid():
            bound_form.save()
            return redirect(self.redirect_url_name)

        context = {
            'title': self.title,
            'form': bound_form,
            'base_app_template': self.base_app_template,
            'object_create_url_name': self.create_url_name
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class CountryDelete(Countries, ObjectDeleteMixin):
    pass


class Currencies(Handbooks):
    model = Currency
    objects_per_page = 10
    form_model = CurrencyForm
    form_class = CurrencyForm

    title = "Currencies"
    create_url_name = 'handbooks:currency_create_url_name'
    update_url_name = 'handbooks:currency_update_url_name'
    delete_url_name = 'handbooks:currency_delete_url_name'
    list_url_name = 'handbooks:currencies_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name



class CurrenciesList(Currencies, ObjectsListMixin):
    fields_to_show = ['numeric', 'name', 'code']
    query_fields = ['numeric', 'name', 'code']
    order_by = 'name'
    template_name = 'obj_list.html'
    edit_button = False
    delete_button = True
    nav_custom_button = {'name': 'NewItem', 'show': True}


class CurrencyDetails(Currencies, ObjectDetailsMixin):
    title = "Currency Details"
    fields_to_header = ['numeric', 'name', 'code']
    fields_to_main = []
    fields_to_footer = []
    edit_button = False
    delete_button = False


class CurrencyCreate(Currencies, ObjectCreateMixin):
    title = "Create currency"
    fields_to_fill = ['name']
    template_name = 'obj_create.html'

    def post(self, request, **kwargs):
        data = request.POST.copy()
        name = request.POST['name']
        data.update(code2currency(name))
        bound_form = self.form_model(data)

        if bound_form.is_valid():
            bound_form.save()
            return redirect(self.redirect_url_name)

        context = {
            'title': self.title,
            'form': bound_form,
            'object_create_url_name': self.create_url_name
        }

        return render(request, self.template_name, context=context)

class CurrencyDelete(Currencies, ObjectDeleteMixin):
    pass

class ResourceTypes(Handbooks):
    model = ResourceType
    form_model = ResourceTypeForm
    form_class = ResourceTypeForm

    title = "ResourceTypes"
    create_url_name = 'handbooks:resource_type_create_url_name'
    update_url_name = 'handbooks:resource_type_update_url_name'
    delete_url_name = 'handbooks:resource_type_delete_url_name'
    list_url_name = 'handbooks:resource_type_list_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name



class ResourceTypeList(ResourceTypes, ObjectsListMixin):
    fields_to_show = ['rtype', 'group']
    query_fields = ['rtype', 'group']
    order_by = 'rtype'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    nav_custom_button = {
        'name': 'NewItem',
        'show': True,
        'func': ResourceTypes.create_url_name,
    }

class ResourceTypeDetails(ResourceTypes, ObjectDetailsMixin):
    title = "Resource Types Details"
    fields_to_header = ['id', 'group', 'rtype']
    fields_to_main = ['description']
    fields_to_footer = []

class ResourceTypeCreate(ResourceTypes, ObjectCreateMixin):
    title = "Resource Type Create"

class ResourceTypeUpdate(ResourceTypes, ObjectUpdateMixin):
    title = "Updating Resource Type"

class ResourceTypeDelete(ResourceTypes, ObjectDeleteMixin):
    pass