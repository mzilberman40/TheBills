import moneyed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView

# import config
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
    form_model = LegalFormForm
    form_class = LegalFormForm
    fields = None
    title = "Legal Forms"
    create_function_name = 'handbooks:legal_form_create_url'
    update_function_name = 'handbooks:legal_form_update_url'
    delete_function_name = 'handbooks:legal_form_delete_url'
    list_function_name = 'handbooks:legal_forms_list_url'
    redirect_to = list_function_name
    success_url = reverse_lazy(list_function_name)


class LegalFormView(Handbooks):
    model = LegalForm
    success_url = reverse_lazy('handbooks:legal_forms_list_url')
    list_function_name = 'handbooks:legal_forms_list_url'


class LegalFormsList(LegalForms, ObjectsListMixin):
    fields_toshow = ['short_name', 'full_name']
    query_fields = ['short_name', 'full_name', 'description']
    order_by = 'short_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}

#
# class LegalFormsList(LegalForms, ListView):
#     fields = ['short_name', 'full_name']
#     query_fields = ['short_name', 'full_name', 'description']
#     order_by = 'short_name'
#     template_name = 'obj_list_new.html'
#     nav_custom_button = {'name': 'NewItem', 'show': True}
#     # nav_custom_button = {
#     #     'name': None,
#     #     'show': False,
#     #     'func': None,
#     #     'params': None,
#     # }
#     title = 'XXXXXXXXXXLegal Forms'
#     list_function_name = 'handbooks:legal_forms_list_url'
#
#     extra_context = {
#         'object_redirect_url': list_function_name,
#         'title': title,
#         'fields': fields,
#         'nav_custom_button': nav_custom_button,
#     }


class LegalFormDetails(LegalForms, ObjectDetailsMixin):
    title = f"Legal Form"
    fields_to_header = ['id', 'short_name', 'full_name']
    fields_to_main = ['description']
    fields_to_footer = ['time_create', 'time_update', 'owner']


class LegalFormCreate(LegalForms, ObjectCreateMixin):
    title = "Legal Form Create"


class LegalFormUpdate(LegalForms, ObjectUpdateMixin):
    title = "Updating legal form"


class LegalFormDelete(LegalFormView, DeleteView):

    template_name = 'obj_confirm_delete.html'
    title = "Deleting legal form"
    extra_context = {
        'title': title,
        'redirect_url': LegalFormView.list_function_name,
    }


class ResourceGroups(Handbooks):
    model = ResourceGroup
    form_model = ResourceGroupForm
    title = "Resource Group"
    create_function_name = 'handbooks:res_group_create_url'
    update_function_name = 'handbooks:res_group_update_url'
    delete_function_name = 'handbooks:res_group_delete_url'
    list_function_name = 'handbooks:res_group_list_url'
    redirect_to = list_function_name


class ResourceGroupList(ResourceGroups, ObjectsListMixin, View):
    fields_toshow = ['name']
    query_fields = ['name', 'description']
    order_by = 'name'
    # template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}


class ResourceGroupDetails(ResourceGroups, ObjectDetailsMixin, View):
    fields_to_header = ['id', 'name',]
    fields_to_main = ['description']
    fields_to_footer = ['time_create', 'time_update', 'owner']


class ResourceGroupCreate(ResourceGroups, ObjectCreateMixin, View):
    title = "Resource Group Create"


class ResourceGroupUpdate(ResourceGroups, ObjectUpdateMixin, View):
    title = "Updating Resource Group"


class ResourceGroupDelete(ResourceGroups, ObjectDeleteMixin, View):
    title = "Deleting Resource Group"


class Countries(Handbooks):
    model = Country
    objects_per_page = 10
    form_model = CountryForm
    form_class = CountryForm

    title = "Countries"
    create_function_name = 'handbooks:country_create_url'
    update_function_name = 'handbooks:country_update_url'
    delete_function_name = 'handbooks:country_delete_url'
    list_function_name = 'handbooks:countries_list_url'
    redirect_to = list_function_name


class CountriesList(Countries, ObjectsListMixin, View):
    fields_toshow = ['iso3166', 'eng_name', 'rus_name', 'alfa2']
    query_fields = ['eng_name', 'rus_name', 'iso3166', 'alfa2', 'alfa3']
    order_by = 'eng_name'
    template_name = 'obj_list.html'
    edit_button = False
    delete_button = True
    nav_custom_button = {'name': 'NewItem', 'show': True}


class CountryDetails(Countries, ObjectDetailsMixin, View):
    title = "Country Details"
    fields_to_header = ['iso3166', 'alfa2', 'alfa3']
    fields_to_main = ['eng_name', 'eng_name_official', 'rus_name', 'rus_name_short', 'rus_name_official']
    fields_to_footer = ['time_create', 'time_update', 'owner']
    edit_button = False
    delete_button = False


class CountryCreate(Countries, ObjectCreateMixin, View):
    title = "Create country"
    fields_to_fill = ['eng_name']

    def post(self, request, **kwargs):
        data = request.POST.copy()
        eng_name = data['eng_name']
        data.update(name2country(eng_name))
        bound_form = self.form_model(data)

        if bound_form.is_valid():
            bound_form.save()
            return redirect(self.redirect_to)

        context = {
            'title': self.title,
            'form': bound_form,
            'base_app_template': self.base_app_template,
            'object_create_url': self.create_function_name
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class CountryDelete(Countries, ObjectDeleteMixin, View):
    pass


class Currencies(Handbooks):
    model = Currency
    objects_per_page = 10
    form_model = CurrencyForm
    form_class = CurrencyForm

    title = "Currencies"
    create_function_name = 'handbooks:currency_create_url'
    update_function_name = 'handbooks:currency_update_url'
    delete_function_name = 'handbooks:currency_delete_url'
    list_function_name = 'handbooks:currencies_list_url'
    redirect_to = list_function_name


class CurrenciesList(Currencies, ObjectsListMixin, View):
    fields_toshow = ['numeric', 'name', 'code']
    query_fields = ['numeric', 'name', 'code']
    order_by = 'name'
    template_name = 'obj_list.html'
    edit_button = False
    delete_button = True
    nav_custom_button = {'name': 'NewItem', 'show': True}


class CurrencyDetails(Currencies, ObjectDetailsMixin, View):
    title = "Currency Details"
    fields_to_header = ['numeric', 'name', 'code']
    fields_to_main = []
    fields_to_footer = []
    edit_button = False
    delete_button = False


class CurrencyCreate(Currencies, ObjectCreateMixin, View):
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
            return redirect(self.redirect_to)

        context = {
            'title': self.title,
            'form': bound_form,
            'object_create_url': self.create_function_name
        }

        return render(request, self.template_name, context=context)


class CurrencyDelete(Currencies, ObjectDeleteMixin, View):
    pass


class ResourceTypes(Handbooks):
    model = ResourceType
    form_model = ResourceTypeForm
    title = "ResourceTypes"
    create_function_name = 'handbooks:resource_type_create_url'
    update_function_name = 'handbooks:resource_type_update_url'
    delete_function_name = 'handbooks:resource_type_delete_url'
    list_function_name = 'handbooks:resource_type_list_url'
    redirect_to = list_function_name


class ResourceTypeList(ResourceTypes, ObjectsListMixin, View):
    fields_toshow = ['rtype', 'group']
    query_fields = ['rtype', 'group']
    order_by = 'rtype'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    nav_custom_button = {
        'name': 'NewItem',
        'show': True,
        'func': ResourceTypes.create_function_name,
    }


class ResourceTypeDetails(ResourceTypes, ObjectDetailsMixin, View):
    title = "Resource Types Details"
    fields_to_header = ['id', 'group', 'rtype']
    fields_to_main = ['description']
    fields_to_footer = []


class ResourceTypeCreate(ResourceTypes, ObjectCreateMixin, View):
    title = "Resource Type Create"


class ResourceTypeUpdate(ResourceTypes, ObjectUpdateMixin, View):
    title = "Updating Resource Type"


class ResourceTypeDelete(ResourceTypes, ObjectDeleteMixin, View):
    pass