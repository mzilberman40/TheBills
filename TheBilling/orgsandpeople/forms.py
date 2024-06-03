from django.forms import *
from django.core.exceptions import ValidationError
from commerce.models import *
from django.utils.text import slugify

from orgsandpeople.models import Email, BusinessUnit


class BusinessUnitForm(ModelForm):
    class Meta:
        model = BusinessUnit
        fields = ['legal_form', 'inn', 'ogrn',
                  'first_name', 'middle_name', 'last_name',
                  'full_name', 'short_name', 'payment_name',
                  'special_status', 'notes']
        widgets = {
            'legal_form': Select(attrs={'class': 'form-control', 'placeholder': 'Legal Form'}),
            'inn': TextInput(attrs={'class': 'form-control', 'placeholder': 'INN'}),
            'ogrn': TextInput(attrs={'class': 'form-control', 'placeholder': 'OGRN'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'full_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'short_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Name'}),
            'payment_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Name'}),
            'special_status': CheckboxInput(attrs={
                'placeholder': 'Payment Name',
                'class': "form-control, form-check form-switch form-check-input",
                'type': 'checkbox',
                'role': 'switch',
                'id': "flexSwitchCheckDefault"
            }),
            'notes': Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes'}),
        }



class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ['email']
        widgets = {
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
        }

