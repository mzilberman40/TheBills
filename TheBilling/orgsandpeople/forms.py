from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
# import tools.from_pycountry as fp
from orgsandpeople.models import Email, BusinessUnit, Bank
from handbooks.models import LegalForm, Country


class BankForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label='Choose Country if you want',
        label='Country',
    )

    def __init__(self, *args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)
        print(kwargs)
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
            'country': forms.Select(
                attrs={'class': 'form-control',
                       'empty_label': 'Choose Country if you want',
                       'label': 'Choose Country if you want',
                       }
            ),
        }


class BusinessUnitForm(forms.ModelForm):
    legal_form = forms.ModelChoiceField(
        queryset=LegalForm.objects.all(),
        empty_label='Form not choosen',
        label='Legal Form',
    )

    class Meta:
        model = BusinessUnit
        # fields = '__all__'
        fields = ['legal_form', 'inn', 'ogrn',
                  'first_name', 'middle_name', 'last_name',
                  'full_name', 'short_name', 'payment_name',
                  'special_status', 'notes']
        # widgets = {
        #     'legal_form': Select(attrs={'class': 'form-control', 'placeholder': 'Legal Form'}),
        #     'inn': TextInput(attrs={'class': 'form-control', 'placeholder': 'INN'}),
        #     'ogrn': TextInput(attrs={'class': 'form-control', 'placeholder': 'OGRN'}),
        #     'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        #     'middle_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
        #     'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        #     'full_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        #     'short_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Name'}),
        #     'payment_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Name'}),
        #     'special_status': CheckboxInput(attrs={
        #         'placeholder': 'Payment Name',
        #         'class': "form-control, form-check form-switch form-check-input",
        #         'type': 'checkbox',
        #         'role': 'switch',
        #         'id': "flexSwitchCheckDefault"
        #     }),
        #     'notes': Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes'}),
        # }


# class EmailForm(ModelForm):
#     class Meta:
#         model = Email
#         fields = ['email']
#         widgets = {
#             'email': EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email',
#             }),
#         }

