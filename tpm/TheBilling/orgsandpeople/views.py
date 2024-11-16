from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from orgsandpeople.forms import BankForm, BusinessUnitForm, AccountForm
from orgsandpeople.models import Bank, BusinessUnit, Email, Account
from utils import (ObjectDetailsMixin, ObjectCreateMixin,
                   ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin)
from library.inject_values import inject_values


class OrgsAndPeople(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8


class BusinessUnits(OrgsAndPeople):
    model = BusinessUnit
    form_model = BusinessUnitForm
    form_class = BusinessUnitForm
    title = "Business Units"
    create_function_name = 'orgsandpeople:bu_create_url'
    update_function_name = 'orgsandpeople:bu_update_url'
    details_function_name = 'orgsandpeople:bu_details_url'
    delete_function_name = 'orgsandpeople:bu_delete_url'
    list_function_name = 'orgsandpeople:bu_list_url'
    redirect_to = list_function_name
    special_fields = ['emails']
    # form_template = 'orgsandpeople/bu_form.html'


class BusinessUnitList(BusinessUnits, ObjectsListMixin, View):
    fields_toshow = ['full_name', 'payment_name']
    query_fields = ['full_name', 'payment_name']
    order_by = 'full_name'
    template_name = 'obj_list.html'
    nav_custom_button = {
        'name': 'NewItem',
        'show': True,
        'func': BusinessUnits.create_function_name,
    }


class BusinessUnitCreate(BusinessUnits, ObjectCreateMixin):
    title = "Create BusinessUnit"
    fields_to_fill = ['inn', 'ogrn', 'first_name', 'middle_name', 'last_name',
                      'full_name', 'short_name', 'emails', 'special_status',
                      'payment_name', 'legal_form', 'notes', 'country']
    template_name = 'obj_create.html'



class BusinessUnitUpdate(BusinessUnits, ObjectUpdateMixin):
    title = "Updating BusinessUnit"
    template_name = 'obj_update.html'
    redirect_to = 'orgsandpeople:bu_details_url'
    params = {'redirect_param': 'pk'}


class BusinessUnitDelete(BusinessUnits, ObjectDeleteMixin):
    title = "Deleting BusinessUnit"


class BusinessUnitDetails(BusinessUnits, ObjectDetailsMixin, View):
    template_name = 'orgsandpeople/bu_details.html'
    title = f"Business Unit Details"
    fields_to_header = ['id', 'inn', 'slug', 'payment_name', 'special_status']
    fields_to_main = ['legal_form', 'first_name', 'middle_name', 'last_name', 'full_name',
                      'short_name', 'notes', 'e_mails']
    fields_to_footer = ['country', 'created', 'modified', 'user']


class BUAccounts(OrgsAndPeople):
    title = "Accounts"
    model = Account
    form_model = AccountForm
    form_class = AccountForm
    create_function_name = 'orgsandpeople:bu_account_create_url'
    update_function_name = 'orgsandpeople:bu_account_update_url'
    delete_function_name = 'orgsandpeople:bu_account_delete_url'
    list_function_name = 'orgsandpeople:bu_accounts_url'
    redirect_to = list_function_name
    params = {'redirect_param': 'bu_pk', 'update_param': 'pk', 'delete_param': 'pk'}


class BUAccountList(BUAccounts, View):
    template_name = 'obj_list.html'
    fields_toshow = ['name', 'bank', 'currency']
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Account', 'show': True}
    create_function_name = 'orgsandpeople:bu_account_create_url'

    def get(self, request, bu_pk):
        bu = get_object_or_404(BusinessUnit, pk=bu_pk)
        accounts = bu.accounts.all()
        accounts = [inject_values(o, self.fields_toshow) for o in accounts]

        page_number = request.GET.get('page', 1)
        paginator = Paginator(accounts, self.objects_per_page)
        page_object = paginator.get_page(page_number)
        is_paginated = page_object.has_other_pages()

        self.nav_custom_button['func'] = self.create_function_name
        self.nav_custom_button['params'] = bu_pk

        context = {
            'title': f"{bu}'s {self.title}",
            'redirect_to': self.redirect_to,
            'page_object': page_object,
            'is_paginated': is_paginated,
            'counter': len(accounts),
            'fields': self.fields_toshow,
            'delete_function': self.delete_function_name,
            'update_function': self.update_function_name,
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'view_button': self.view_button,
            'nav_custom_button': self.nav_custom_button,
        }

        return render(request, self.template_name, context=context)


class BUAccountDetail(BUAccounts, ObjectDetailsMixin, View):
    title = f"Account Details"
    fields_to_header = ['id', 'business_unit']
    fields_to_main = ['bank', 'account_number', 'currency', 'starting_balance', 'notes']
    fields_to_footer = ['status', 'activate_date', 'deactivate_date']


class BUAccountCreate(BUAccounts, View):
    title = f"Creating account..."
    template_name = 'obj_create.html'
    fields_to_fill = ['name', 'bank', 'currency', 'account_number',
                      'starting_balance', 'status', 'notes']
    create_function_name = 'orgsandpeople:bu_account_create_url'

    def get(self, request, bu_pk):
        form = self.form_model()
        if self.fields_to_fill:
            form.fields = {key: value for key, value in form.fields.items()
                           if key in self.fields_to_fill}
        context = {
            'title': self.title,
            'form': form,
            'class_name': self.model.__name__.lower(),
            'object_create_url': self.create_function_name,
            'create_param': bu_pk
        }
        return render(request, self.template_name, context=context)

    def post(self, request, bu_pk):
        data = request.POST.copy()  # Make a mutable copy of POST data
        data['user'] = request.user  # Probably user is necessary for model
        bu = get_object_or_404(BusinessUnit, pk=bu_pk)

        data['business_unit'] = bu
        bound_form = self.form_model(data)

        if bound_form.is_valid():
            # print(bound_form.cleaned_data)
            bound_form.save()
            return redirect(self.redirect_to, bu_pk)

        context = {
            'title': self.title,
            'form': bound_form,
            'object_create_url': self.create_function_name,
            'create_param': bu_pk
        }

        return render(request, self.template_name, context=context)


class BUAccountDelete(BUAccounts, ObjectDeleteMixin, View):
    title = "Deleting Account"


class BUAccountUpdate(BUAccounts, ObjectUpdateMixin, View):
    title = "Updating Account"


class Banks(OrgsAndPeople):
    model = Bank
    form_model = BankForm
    form_class = BankForm

    title = "Banks"
    create_function_name = 'orgsandpeople:bank_create_url'
    update_function_name = 'orgsandpeople:bank_update_url'
    delete_function_name = 'orgsandpeople:bank_delete_url'
    list_function_name = 'orgsandpeople:bank_list_url'
    redirect_to = list_function_name
    base_app_template = None


class BankList(Banks, ObjectsListMixin, View):
    fields_toshow = ['short_name', 'bik', 'swift']
    query_fields = ['short_name', 'name', 'bik', 'swift']
    order_by = 'short_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}


class BankDetails(Banks, ObjectDetailsMixin, View):
    title = f"Bank Details"
    fields_to_header = ['id', 'short_name', 'name', 'slug']
    fields_to_main = ['bik', 'corr_account', 'swift', 'country', 'notes']
    fields_to_footer = ['created', 'modified', 'user']


class BankCreate(Banks, ObjectCreateMixin):
    title = "Create Bank"
    template_name = 'obj_create.html'

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)

        # If the form is invalid, re-render it with the same context
        context = {
            'title': self.title,
            'form': form,  # Bound form with validation errors
            'base_app_template': self.base_app_template,
            'object_create_url': self.create_function_name
        }
        return render(request, self.template_name, context)

    # Process valid form submission
    def form_valid(self, form):
        # Assign the user to the form instance
        form.instance.user = self.request.user
        return super().form_valid(form)


class BankUpdate(Banks, ObjectUpdateMixin, View):
    title = "Updating Bank"


class BankDelete(Banks, ObjectDeleteMixin, View):
    title = "Deleting Bank"

