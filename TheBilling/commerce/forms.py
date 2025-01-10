from django import forms

# from django.core.exceptions import ValidationError

from commerce.models import *


class ResourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            self.fields['user'].initial = kwargs['user']

    class Meta:
        model = Resource
        fields = '__all__'
        exclude = ['user', 'business_unit']
        labels = {
            'current_status': 'Current Status'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name',}),
            'description': forms.TextInput(attrs={'placeholder': 'Description'}),
            # 'rtype': forms.Select(),
            # 'current_status': forms.Select(),
            # 'business_unit': forms.Select(),
            # 'project': forms.Select(),

        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'
        exclude = []
        labels = {
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title',}),
            'description': forms.TextInput(attrs={'placeholder': 'Description'}),
            'beneficiary': forms.Select(),
        }

class ContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            self.fields['user'].initial = kwargs['user']

    class Meta:
        model = Contract
        fields = [
            'number', 'title', 'description',
            'seller', 'buyer', 'project',
            'start_date', 'end_date', 'status',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        seller = cleaned_data.get('seller')
        buyer = cleaned_data.get('buyer')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Ensure Seller and Buyer are different
        if seller == buyer:
            raise ValidationError("Seller and Buyer must be different.")

        # Validate date range
        if end_date and start_date and end_date < start_date:
            raise ValidationError("End date must be after start date.")

        return cleaned_data

    # Service Price History Form
    class ServicePriceHistoryForm(forms.ModelForm):

        class Meta:
            model = ServicePriceHistory
            fields = ['service', 'new_price', 'effective_date']
            widgets = {
                'service': forms.Select(attrs={'class': 'form-control'}),
                'new_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
                'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            }
            labels = {
                'service': 'Service',
                'new_price': 'New Price',
                'effective_date': 'Effective Date',
            }

class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            self.fields['user'].initial = kwargs['user']

    class Meta:
        model = Service
        fields = ['status', 'service_type', 'service_name', 'billing_frequency', 'start_date',
                  'finish_date', 'price', 'currency', 'contract', 'resource', 'description']
        widgets = {
            'status': forms.Select(),
            'service_name': forms.Select(),
            'service_type': forms.Select(),
            'billing_frequency': forms.Select(),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'finish_date': forms.DateInput(attrs={'type': 'date'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'currency': forms.Select(),
            'contract': forms.Select(),
            'resource': forms.Select(),
            'description': forms.Textarea(),
            'is_active': forms.CheckboxInput(),
        }
