from django.forms import *
from django.core.exceptions import ValidationError
from commerce.models import *
from django.utils.text import slugify




class BusinessUnitForm(ModelForm):
    class Meta:
        model = BusinessUnit
        fields = '__all__'
        # exclude = ['address_data']
        widgets = {
            'inn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'INN'
            }),
            'ogrn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'OGRN'
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'special_status': CheckboxInput(attrs={
                'class': "form-check form-switch form-check-input",
                'type': 'checkbox',
                'role': 'switch',
                'id': "flexSwitchCheckDefault"
            }),
            'middle_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Middle Name'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'full_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
            }),
            'payment_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Payment Name',
            }),
            'short_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Short Name'
            }),
            'legal_form': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Legal Form'
            }),
            'address': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Address'
            }),
            'address_data': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address Data'
            }),
            # 'emails': SelectMultiple(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Email'
            # }),
            'notes': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Notes'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('inn') is None and cleaned_data.get('payment_name') is None:
            raise ValidationError('inn or payment_name should not be null')

    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()

    def clean_middle_name(self):
        return self.cleaned_data['middle_name'].capitalize()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'] or \
                    self.cleaned_data['first_name'] + self.cleaned_data['middle_name'] + self.cleaned_data['last_name']
        return full_name

    def clean_short_name(self):
        short_name = self.cleaned_data['short_name'].upper() or slugify(self.cleaned_data['full_name'])
        return short_name

    def clean_address(self):
        return self.cleaned_data['address'].capitalize()

    def clean_notes(self):
        return self.cleaned_data['notes']


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'bank': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Bank',
            }),
            'number': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Payment's number"
            }),
            'currency': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Currency',
            }),
            'business_unit': Select(attrs={
                'class': 'form-control',
                'placeholder': 'BusinessUnit',
            }),
            'starting_date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Starting Date',
            }),
            'starting_balance': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Starting Balance',
            }),
            'notes': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Notes'
            })
        }

    def clean_number(self):
        # if len(str(self.cleaned_data['number'])) > 20:
        #     raise ValidationError("Account's number too long!")
        return self.cleaned_data['number']
