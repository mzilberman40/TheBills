from django import forms
# from django.core.exceptions import ValidationError

from commerce.models import *


class ResourceForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ResourceForm, self).__init__(*args, **kwargs)
    #     if 'user' in kwargs:
    #         self.fields['user'].initial = kwargs['user']

    class Meta:
        model = Resource
        # fields = ('name', 'description', 'group', 'available')
        fields = '__all__'
        exclude = ['activate_date', 'deactivate_date', 'user']
        labels = {
            # 'name': 'Name',  # This sets the label for the 'name' field
            # 'description': 'Description',  # Label for 'description' field
            'group': 'Choose Resource Group',  # Label for 'group' field
            'available': 'Resource Available'  # Label for 'available' field
        }
        widgets = {
            'name': forms.TextInput(attrs={
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
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
#
#
# class ResourceForm(forms.ModelForm):
#     name = forms.CharField(
#         label='Name',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Name'
#         })
#     )
#     description = forms.CharField(
#         label='Description',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Description'
#         })
#     )
#     group = forms.ModelChoiceField(
#         queryset=Resource.objects.all(),  # Assuming 'group' is a foreign key to 'Resource'
#         label='Choose Resource Group',
#         widget=forms.Select(attrs={
#             'class': 'form-control'
#         })
#     )
#     available = forms.BooleanField(
#         label='Resource Available',
#         widget=forms.CheckboxInput(attrs={
#             'class': 'form-check-input'
#         })
#     )
#
#     class Meta:
#         model = Resource
#         fields = ('name', 'description', 'group', 'available')

# class ResourceForm(forms.ModelForm):
#
#     available = forms.BooleanField(
#         label='Resource Available',
#         widget=forms.CheckboxInput(attrs={
#             'class': 'form-check-input'
#         })
#
#     class Meta:
#         model = Resource
#         fields = ('name', 'description', 'group', 'available')
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Name',
#             }),
#             'description': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Description'
#             }),
#             'group': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Group',
#                 'empty_label': 'Choose Resource Group',
#                 'label': 'Choose Resource Group'
#             }),
#             'available': forms.CheckboxInput(attrs={
#                 'class': 'form-check-input',
#             }),
#         }
#
#
#     def clean_name(self):
#         return self.cleaned_data['name'].capitalize()
#
