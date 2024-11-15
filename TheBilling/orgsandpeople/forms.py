from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from orgsandpeople.models import Email, BusinessUnit, Bank, Account
from handbooks.models import LegalForm, Country


class MultiEmailFieldWithEmailType(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter emails in the format: email1, email2:type, ...'}
        )
        kwargs['help_text'] = "Enter emails in the format: email1, email2:type2, email3"
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        super().validate(value)
        emails = []

        for entry in value:
            entry = entry.strip()
            if ':' in entry:
                email, email_type = entry.split(':', 1)
                email = email.strip()
                email_type = email_type.strip()
            else:
                email = entry
                email_type = None

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(f"'{email}' is not a valid email address.")

            emails.append({'email': email, 'email_type': email_type})

        return emails


class BankForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label='Choose Country',
        label='Country',
    )

    class Meta:
        model = Bank
        fields = '__all__'
        # fields = ['name', 'short_name', 'bik', 'corr_account', 'swift', 'notes', 'country']
        exclude = ['user']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'name',
            }),
            'short_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'short_name',
            }),
            'bik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'National Bank Identification Code',
            }),
            'corr_account': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Corr account',
            }),
            'swift': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'swift',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'notes',
            }),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'business_unit', 'bank', 'currency', 'account_number', 'starting_balance',
                  'status', 'notes']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'name',
                }),
            'business_unit': forms.Select(
                attrs={'class': 'form-control',
                       'empty_label': 'Choose Business Unit',
                       'label': 'Choose Business Unit'}),
            'bank': forms.Select(
                attrs={'class': 'form-control',
                       'empty_label': 'Choose Bank',
                       'label': 'Choose Bank'}),
            'currency': forms.Select(
                attrs={'class': 'form-control',
                       'empty_label': 'Choose Currency',
                       'label': 'Choose Currency'}),
            'account_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Account Number',
                }),
            'starting_balance': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Starting balance',
                }),
            'status': forms.Select(
                attrs={
                    'class': 'form-control',
                }),
            'notes': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'notes',
                       }),
        }


class BusinessUnitForm(forms.ModelForm):
    legal_form = forms.ModelChoiceField(
        queryset=LegalForm.objects.all(),
        empty_label='Choose Legal Form',
        label='Legal Form',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label='Choose Country',
        label='Country',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    emails = MultiEmailFieldWithEmailType(
        required=False,
        help_text='Enter emails in the format: email1, email2, ...',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter emails in the format: email1, email2, ...'}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        # print(kwargs)
        super().__init__(*args, **kwargs)
        self.user = user
        # print(args, kwargs)
        # print("User: ", self.user)
        if self.instance and hasattr(self.instance, 'pk') and self.instance.pk:
            # Prepopulate the emails_field with existing emails
            emails = self.instance.emails.all()
            emails_data = ', '.join([f"{email.email}:{email.email_type}" if email.email_type else email.email for email in emails])
            self.initial['emails'] = emails_data

    class Meta:
        model = BusinessUnit
        # fields = '__all__'
        fields = ['legal_form', 'country', 'inn', 'ogrn',
                  'first_name', 'middle_name', 'last_name',
                  'full_name', 'short_name', 'payment_name',
                  'special_status', 'notes', 'emails']
        widgets = {
            'inn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INN'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'OGRN'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Name'}),
            'payment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Name'}),
            'special_status': forms.CheckboxInput(attrs={
                'class': "form-control, form-check form-switch form-check-input",
                'type': 'checkbox',
                'role': 'switch',
                'id': "flexSwitchCheckDefault"
            }),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # print(instance)

        emails = self.cleaned_data.get('emails', [])
        # Set user if not set (handle create case)
        if not instance.user_id:
            instance.user = self.user
        # Always save the instance first if commit is False
        instance.save()
        # Clear existing emails and add new ones
        instance.emails.all().delete()
        for email_data in emails:
            # print(f"Email data: {email_data}")
            if isinstance(email_data, dict):
                Email.objects.create(bu=instance, email=email_data['email'], email_type=email_data['email_type'])
            else:
                email_data = email_data.strip()
                if ':' in email_data:
                    email, email_type = email_data.split(':', 1)
                    email = email.strip()
                    email_type = email_type.strip()
                else:
                    email = email_data
                    email_type = None
                Email.objects.create(bu=instance, email=email, email_type=email_type)
        if commit:
            self.save_m2m()  # Save many-to-many relationships if any

        return instance
