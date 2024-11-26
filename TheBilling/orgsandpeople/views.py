
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View

from commerce.forms import ResourceForm
from commerce.models import Resource
from orgsandpeople.forms import BankForm, BusinessUnitForm, AccountForm
from orgsandpeople.models import Bank, BusinessUnit, Account
from utils import (ObjectDetailsMixin, ObjectCreateMixin,
                   ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin)
from library.inject_values import inject_values


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
    # special_fields = ['emails']
    # form_template = 'orgsandpeople/bu_form.html'


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
    filter_param = ('business_unit', 'bu_pk')
    redirect_param = 'bu_pk'

class BUAccountList(BUAccounts, ObjectsListMixin):
    template_name = 'obj_list.html'
    fields_to_show = ['name', 'bank', 'currency']
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {'name': 'New Account', 'show': True}


class BUAccountDetail(BUAccounts, ObjectDetailsMixin):
    title = f"Account Details"
    fields_to_header = ['id', 'business_unit']
    fields_to_main = ['bank', 'account_number', 'currency', 'starting_balance', 'notes']
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

    # def get(self, request, **kwargs):
    #     pk = kwargs.get('pk')
    #     obj = get_object_or_404(self.model, pk=pk)
    #     form = self.form_class(instance=obj)
    #
    #     context = {
    #         'title': self.title + f" with pk {obj.pk}.....",
    #         'form': form,
    #         'object': obj,
    #         'update_function': reverse(self.update_url_name, kwargs={'pk': pk, 'bu_pk': obj.pk}),
    #         'redirect_function': reverse(self.redirect_url_name, kwargs={'bu_pk': obj.pk}),
    #     }
    #     context.update(self.additional_context)
    #
    #     return render(request, self.template_name, context=context)
    #
    # def post(self, request, **kwargs):
    #     print(kwargs)
    #     args = []
    #     pk = kwargs.get('pk')
    #     obj = get_object_or_404(self.model, pk=pk)
    #     bound_form = self.form_class(request.POST.copy(), instance=obj)
    #     redirect_function = reverse(self.redirect_url_name, kwargs={'bu_pk': obj.pk})
    #     if bound_form.is_valid():
    #         bound_form.save()
    #         return redirect(redirect_function)
    #     context = {
    #         'form': bound_form,
    #         'object': obj,
    #         'update_function': reverse(self.update_url_name, kwargs={'pk': pk, 'bu_pk': obj.pk}),
    #         # 'redirect_function': reverse(self.redirect_url_name, kwargs={'bu_pk': obj.pk}),
    #     }
    #     context.update(self.additional_context)
    #     return render(request, self.template_name, context=context)
    #


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

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)

        # If the form is invalid, re-render it with the same context
        context = {
            'title': self.title,
            'form': form,  # Bound form with validation errors
            'base_app_template': self.base_app_template,
            'object_create_url_name': self.create_url_name
        }
        return render(request, self.template_name, context)

    # Process valid form submission
    def form_valid(self, form):
        # Assign the user to the form instance
        form.instance.user = self.request.user
        return super().form_valid(form)


class BankUpdate(Banks, ObjectUpdateMixin):
    title = "Updating Bank"


class BankDelete(Banks, ObjectDeleteMixin):
    title = "Deleting Bank"


class Resources(OrgsAndPeople):
    model = Resource
    form_model = ResourceForm
    form_class = ResourceForm
    title = "Resources"
    create_url_name = 'orgsandpeople:bu_resource_create_url_name'
    update_url_name = 'orgsandpeople:bu_resource_update_url_name'
    delete_url_name = 'orgsandpeople:bu_resource_delete_url_name'
    list_url_name = 'orgsandpeople:bu_resources_url_name'
    nav_custom_button_func = create_url_name
    redirect_url_name = list_url_name
    success_url_name = list_url_name
    params = {'redirect_param': 'bu_pk', 'update_param': 'pk', 'delete_param': 'pk'}

class ResourceList(Resources, View):
    fields_toshow = ['name', 'rtype', 'available']
    # query_fields = ['name']
    # order_by = 'name'
    template_name = 'obj_list.html'
    edit_button = True
    view_button = True
    delete_button = True
    nav_custom_button = {
        'name': 'NewItem',
        'show': True,
    }
    create_url_name = 'orgsandpeople:bu_resource_create_url_name'

    def get(self, request, bu_pk):
        bu = get_object_or_404(BusinessUnit, pk=bu_pk)
        resources = bu.resources.all()
        resources = [inject_values(o, self.fields_toshow) for o in resources]

        page_number = request.GET.get('page', 1)
        paginator = Paginator(resources, self.objects_per_page)
        page_object = paginator.get_page(page_number)
        is_paginated = page_object.has_other_pages()

        self.nav_custom_button['func'] = self.create_url_name
        self.nav_custom_button['param'] = bu_pk

        context = {
            'title': f"{bu}'s {self.title}",
            'redirect_url_name': self.redirect_url_name,
            'page_object': page_object,
            'is_paginated': is_paginated,
            'counter': len(resources),
            'fields': self.fields_toshow,
            'delete_function': self.delete_url_name,
            'update_function': self.update_url_name,
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'view_button': self.view_button,
            'nav_custom_button': self.nav_custom_button,
            'bu_pk': bu_pk,
        }

        return render(request, self.template_name, context=context)


class ResourceDetails(Resources, ObjectDetailsMixin):
    edit_button = True
    title = "Resource Details"
    fields_to_header = ['id', 'rtype', 'name', 'owner']
    fields_to_main = [ 'description', 'available']
    fields_to_footer = ['created', 'modified', 'user']


class ResourceCreate(Resources, ObjectCreateMixin):
    title = "Resource Create"
    create_param = 'bu_pk'


class ResourceUpdate(Resources, ObjectUpdateMixin):
    title = "Updating email"


class ResourceDelete(Resources, ObjectDeleteMixin):
    pass
