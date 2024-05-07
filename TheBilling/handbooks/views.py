import moneyed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.text import slugify
from django.views import View

import config
from handbooks.forms import LegalFormForm
from handbooks.models import LegalForm
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
