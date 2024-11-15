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
            # # 'name': 'Name',  # This sets the label for the 'name' field
            # # 'description': 'Description',  # Label for 'description' field
            # 'group': 'Choose Resource Group',  # Label for 'group' field
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
