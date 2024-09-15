from django import forms
import moneyed
# from django.core.exceptions import ValidationError

from handbooks.models import LegalForm, Country, Currency, ResourceGroup, ResourceType
# from tools.texts import clear_text
import tools.from_pycountry as fp


class LegalFormForm(forms.ModelForm):
    class Meta:
        model = LegalForm
        # fields = '__all__'
        fields = ('short_name', 'full_name', 'description')
        widgets = {
            'short_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Shortname',
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fullname',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            })
        }

    def clean_short_name(self):
        return self.cleaned_data['short_name'].upper()

    def clean_full_name(self):
        return ' '.join([word.capitalize() for word in self.cleaned_data['full_name'].split()])


class ResourceGroupForm(forms.ModelForm):

    class Meta:
        model = ResourceGroup
        # fields = '__all__'
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            })
        }

    def clean_name(self):
        return self.cleaned_data['name'].upper()


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

        widgets = {
            'eng_name': forms.Select(choices=sorted(
                [(c.name, c.name) for c in fp.get_all_countries()]
            ),
                                     attrs={
                                         'class': 'form-control',
                                            }),
            'iso3166': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISO3166 Country code',
            }),
            'alfa2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'alfa2',
            }),
            'alfa3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'alfa3',
            }),
            'rus_name_short': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Russian name short',
            }),
            'rus_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Russian name',
            }),

            # 'eng_name': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'English name',
            # }),

            'eng_name_official': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'English name official',
            }),

            'rus_name_official': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Official Russian name',
            }),
        }
#
#     def clean_rus_name_short(self):
#         print(self.cleaned_data)
#         if not self.cleaned_data.get('rus_name_short'):
#             raise ValidationError("Wrong russian name")
#         return self.cleaned_data['rus_name_short']
#
#     def clean_eng_name(self):
#         return clear_text((self.cleaned_data['eng_name']), allow_spaces=True)
#
#     def clean_iso3166(self):
#         return self.cleaned_data['iso3166']


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency
        fields = '__all__'

        widgets = {
            'name': forms.Select(
                choices=[(c.code, c.name) for c in sorted(moneyed.list_all_currencies(), key=lambda x: x.name)],
                attrs={'class': 'form-control'}
            ),
            'numeric': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numeric currency code',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3-char currency code',
            }),
        }


class ResourceTypeForm(forms.ModelForm):

    class Meta:
        model = ResourceType
        fields = '__all__'
        labels = {
            'group': 'Choose Resource Group',  # Label for 'group' field
        }
        widgets = {
            'rtype': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            }),
            'group': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Group'
            }),
        }
