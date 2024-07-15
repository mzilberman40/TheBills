from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from orgsandpeople.forms import BankForm, BusinessUnitForm
from orgsandpeople.models import Bank, BusinessUnit, Email
from utils import (ObjectDetailsMixin, ObjectCreateMixin,
                   ObjectUpdateMixin, ObjectDeleteMixin, ObjectsListMixin)


class OrgsAndPeople(LoginRequiredMixin):
    raise_exception = True
    objects_per_page = 8


class BusinessUnits(OrgsAndPeople):
    model = BusinessUnit
    form_model = BusinessUnitForm
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
    nav_custom_button = {'name': 'NewItem', 'show': True}


class BusinessUnitCreate(BusinessUnits, ObjectCreateMixin, View):
    title = "Create BusinessUnit"
    # fields_to_fill = ['inn', 'ogrn', 'first_name', 'middle_name', 'last_name',
    #                   'full_name', 'short_name', 'emails', 'special_status',
    #                   'payment_name', 'legal_form', 'notes']

    def post(self, request):
        data = request.POST.copy()
        data['user'] = request.user
        form = self.form_model(data)
        if form.is_valid():
            bu = form.save(commit=False)
            bu.save()
            emails = form.cleaned_data['emails']
            email_list = [email.strip() for email in emails.split(',')]
            for email, email_type in email_list:
                Email.objects.get_or_create(owner=bu, email=email, email_type=email_type)
            return redirect(self.redirect_to)

        context = {
            'title': self.title,
            'form': form,
            'base_app_template': self.base_app_template,
            'object_create_url': self.create_function_name
        }

        return render(request, 'obj_create.html', context)


class BusinessUnitUpdate(BusinessUnits, ObjectUpdateMixin, View):
    title = "Updating BusinessUnit"
    template_name = 'obj_update.html'

    def get(self, request, pk):
        bu = get_object_or_404(BusinessUnit, pk=pk)
        initial_emails = ', '.join([f"{email.email}:{email.email_type}"
                                    if email.email_type else email.email
                                    for email in bu.emails.all()])

        form = BusinessUnitForm(instance=bu, initial={'emails': initial_emails})
        return render(request, self.template_name, {'form': form})

    # def get(self, request, pk):
    #     person = get_object_or_404(Person, pk=pk)
    #     initial_emails = ', '.join([f"{email.email}:{email.email_type}" if email.email_type else email.email for email in person.email_addresses.all()])
    #     initial_data = {
    #         'name': person.name,
    #         'emails': initial_emails
    #     }
    #     form = PersonForm(initial=initial_data)
    #     return render(request, 'person_form.html', {'form': form})

    def post(self, request, pk):
        bu_obj = get_object_or_404(self.model, pk=pk)
        new_data = request.POST.copy()
        new_data['user'] = request.user
        form = self.form_model(new_data, instance=bu_obj)
        if form.is_valid():
            bu = form.save()
            bu.emails.all().delete()
            emails = form.cleaned_data['emails']
            for email, email_type in emails:
                Email.objects.get_or_create(bu=bu, email=email, email_type=email_type)

            return redirect(self.redirect_to)

        context = {
            'title': self.title,
            'form': form,
            'base_app_template': self.base_app_template,
            # 'object_create_url': self.create_function_name
        }

        return render(request, self.template_name, context)

    # def post(self, request, pk):
    #     person = get_object_or_404(Person, pk=pk)
    #     form = PersonForm(request.POST)
    #     if form.is_valid():
    #         person.name = form.cleaned_data['name']
    #         person.save()
    #         person.email_addresses.all().delete()
    #         emails = form.cleaned_data['emails']
    #         for email, email_type in emails:
    #             EmailAddress.objects.create(person=person, email=email, email_type=email_type)
    #         return redirect('person-list')
    #     return render(request, 'person_form.html', {'form': form})


class BusinessUnitDelete(BusinessUnits, ObjectDeleteMixin, View):
    title = "Deleting BusinessUnit"


class BusinessUnitDetails(BusinessUnits, ObjectDetailsMixin, View):
    title = f"Business Unit Details"
    fields_to_header = ['id', 'inn', 'slug', 'payment_name', 'special_status']
    fields_to_main = ['first_name', 'middle_name', 'last_name', 'full_name',
                      'short_name', 'country', 'notes', 'e_mails']
    fields_to_footer = ['created', 'modified', 'user']

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        emails = ', '.join(obj.emails.values_list('email', flat=True))
        setattr(obj, 'e_mails', emails)
        header_dict = {k: getattr(obj, k, None) for k in self.fields_to_header}
        main_dict = {k: getattr(obj, k, None) for k in self.fields_to_main}
        footer_dict = {k: getattr(obj, k, None) for k in self.fields_to_footer}

        context = {
            'title': f'{self.title}: {obj} ',
            f'{self.model.__name__.lower()}': obj,
            'model_name': f'{self.model.__name__.lower()}',
            'object': obj,
            'admin_object': obj,
            'header_dict': header_dict,
            'card_title': self.card_title,
            'main_dict': main_dict,
            'footer_dict': footer_dict,
            'details': True,
            'list_function': self.list_function_name,
            'delete_function': self.delete_function_name,
            'update_function': self.update_function_name,
            'object_update_url': self.update_function_name,
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'nav_custom_button': self.nav_custom_button
        }
        # print(context)
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class Banks(OrgsAndPeople):
    model = Bank
    form_model = BankForm
    title = "Banks"
    create_function_name = 'orgsandpeople:bank_create_url'
    update_function_name = 'orgsandpeople:bank_update_url'
    delete_function_name = 'orgsandpeople:bank_delete_url'
    list_function_name = 'orgsandpeople:bank_list_url'
    redirect_to = list_function_name


class BankList(Banks, ObjectsListMixin, View):
    fields_toshow = ['short_name', 'bik']
    query_fields = ['short_name', 'name', 'bik', 'swift']
    order_by = 'short_name'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}


class BankDetails(Banks, ObjectDetailsMixin, View):
    title = f"Bank Details"
    fields_to_header = ['id', 'short_name', 'name', 'slug']
    fields_to_main = ['bik', 'corr_account', 'swift', 'country', 'notes']
    fields_to_footer = ['created', 'modified', 'user']


class BankCreate(Banks, ObjectCreateMixin, View):
    title = "Create Bank"


class BankUpdate(Banks, ObjectUpdateMixin, View):
    title = "Updating Bank"


class BankDelete(Banks, ObjectDeleteMixin, View):
    title = "Deleting Bank"
