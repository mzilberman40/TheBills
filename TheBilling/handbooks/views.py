import moneyed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View

import config
from handbooks.add_objects import name2country
from handbooks.forms import LegalFormForm, CountryForm
from handbooks.models import LegalForm, Country
from utils import ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin


def show_currencies(request):
    template_name = "handbooks/currencies.html"
    currencies = [moneyed.CURRENCIES.get(c) for c in config.CURRENCIES]
    fields = ['name', 'code', 'numeric', 'countries']
    data = {
        'objects': currencies,
        'counter': len(currencies),
        'fields': fields,
        'title': 'Currencies',
        'redirect_to': 'handbooks:currencies'
    }

    return render(request, template_name=template_name, context=data)


class Handbooks(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8


class LegalForms(Handbooks):
    model = LegalForm
    form_model = LegalFormForm
    title = "Legal Forms"
    create_function_name = 'handbooks:legal_form_create_url'
    update_function_name = 'handbooks:legal_form_update_url'
    delete_function_name = 'handbooks:legal_form_delete_url'
    list_function_name = 'handbooks:legal_forms_list_url'
    redirect_to = list_function_name


class LegalFormsList(LegalForms, ObjectsListMixin, View):
    fields_toshow = ['short_name', 'full_name']
    query_fields = ['short_name', 'full_name', 'description']
    order_by = 'short_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}


class LegalFormDetails(LegalForms, ObjectDetailsMixin, View):
    title = f"Legal Form"
    fields_to_header = ['id', 'short_name', 'full_name', 'slug']
    fields_to_main = ['description']
    fields_to_footer = ['time_create', 'time_update', 'owner']


class LegalFormCreate(LegalForms, ObjectCreateMixin, View):
    title = "Legal Form Create"


class LegalFormUpdate(LegalForms, ObjectUpdateMixin, View):
    title = "Updating legal form"


class LegalFormDelete(LegalForms, ObjectDeleteMixin, View):
    title = "Deleting legal form"


class Countries(Handbooks):
    model = Country
    objects_per_page = 10
    form_model = CountryForm
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
    # edit_button = True
    # delete_button = True
    nav_custom_button = {'name': 'NewItem', 'show': True}


class CountryDetails(Countries, ObjectDetailsMixin, View):
    title = "Country Details"
    template_name = 'obj_list.html'


class CountryCreate(Countries, ObjectCreateMixin, View):

    title = "Create country"
    fields_to_fill = ['eng_name']

    def get(self, request):
        form = self.form_model()
        if self.fields_to_fill:
            form.fields = {key: value for key, value in form.fields.items() if key in self.fields_to_fill}

        context = {
            'title': self.title,
            'form': form,
            'base_app_template': self.base_app_template,
            'class_name': self.model.__name__.lower(),
            'object_create_url': self.create_function_name
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)

    def post(self, request):
        data = dict(request.POST)
        eng_name = request.POST['eng_name']

        # d = name2country(rus_name)
        data.update(name2country(eng_name))
        data['owner'] = request.user
        print(data)
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


class CountryUpdate(Countries, ObjectUpdateMixin, View):
    title = "Updating country"


class CountryDelete(Countries, ObjectDeleteMixin, View):
    pass
