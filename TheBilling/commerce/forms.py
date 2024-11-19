from django import forms
# from django.core.exceptions import ValidationError

from commerce.models import *
from handbooks.models import ResourceType


class ResourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        print(kwargs)
        if 'user' in kwargs:
            self.fields['user'].initial = kwargs['user']

    class Meta:
        model = Resource
        # fields = ('owner', 'name', 'description', 'rtype', 'available')
        fields = '__all__'
        exclude = ['activate_date', 'deactivate_date', 'user']
        labels = {
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
            'rtype': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'ResourceType'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'owner': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'BusinessUnit'
            }),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'
        exclude = []
        labels = {
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            }),
            'beneficiary': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Beneficiary'
            }),
        }
