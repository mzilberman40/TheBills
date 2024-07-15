from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.text import slugify
# import tools.from_pycountry as fp
from orgsandpeople.models import Email, BusinessUnit, Bank
from handbooks.models import LegalForm, Country


class BankForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label='Choose Country',
        label='Country',
    )

    def __init__(self, *args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            self.fields['user'].initial = kwargs['user']

    class Meta:
        model = Bank
        # fields = '__all__'
        fields = ['name', 'short_name', 'bik', 'corr_account', 'swift', 'notes', 'country']

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
            # 'country': forms.Select(
            #     attrs={'class': 'form-control',
            #            'empty_label': 'Choose Country',
            #            'label': 'Choose Country',
            #            }
            # ),
        }


class BusinessUnitForm(forms.ModelForm):
    legal_form = forms.ModelChoiceField(
        queryset=LegalForm.objects.all(),
        empty_label='Choose Legal Form',
        label='Legal Form',
    )

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label='Choose Country',
        label='Country',
    )

    # emails = forms.CharField(
    #     widget=forms.Textarea,
    #     required=False,
    #     help_text='Enter emails with optional types in the format: email1:type1, email2:type2, ...'
    # )

    emails = forms.CharField(
        help_text='Enter emails with optional types in the format: '
                  'email1:type1, email2:type2, ...',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter emails with optional types in the format: '
                           'email1:type1, email2:type2, ...'}),
    )

    def __init__(self, *args, **kwargs):
        super(BusinessUnitForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            self.fields['user'].initial = kwargs['user']

    class Meta:
        model = BusinessUnit
        fields = ['legal_form', 'inn', 'ogrn',
                  'first_name', 'middle_name', 'last_name',
                  'full_name', 'short_name', 'payment_name',
                  'special_status', 'notes', 'emails', 'country']
        widgets = {
            'country': forms.Select(
                attrs={'class': 'form-control',
                       'empty_label': 'Choose Country',
                       'label': 'Choose Country'}),
            'inn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INN'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'OGRN'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Name'}),
            'payment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Name'}),
            'special_status': forms.CheckboxInput(attrs={
                'placeholder': 'Payment Name',
                'class': "form-control, form-check form-switch form-check-input",
                'type': 'checkbox',
                'role': 'switch',
                'id': "flexSwitchCheckDefault"
            }),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes'}),
            'emails': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter emails with types in the format: '
                               'email1:type1, email2:type2, ...'}),
        }

    def clean_emails(self):
        emails = self.cleaned_data['emails']
        email_list = []
        for email_entry in emails.split(','):
            email_entry = email_entry.strip()
            if ':' in email_entry:
                email, email_type = email_entry.split(':', 1)
                email = email.strip()
                email_type = email_type.strip()
            else:
                email = email_entry
                email_type = None

            forms.EmailField().clean(email)  # Validate email
            email_list.append((email, email_type))
        return email_list
