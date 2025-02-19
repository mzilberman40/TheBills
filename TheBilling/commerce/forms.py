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

class ServicePriceForm(forms.ModelForm):
    # Service Price History Form
    def __init__(self, *args, **kwargs):
        print(kwargs)
        super(ServicePriceForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            self.fields['changed_by'].initial = kwargs['user']

    class Meta:
        model = ServicePrice
        fields = ['service', 'price', 'start_date', 'end_date', 'currency']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            # 'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'service': 'Service',
            'price': 'New Price',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'currency': 'Currency',
        }

class ServiceForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                               help_text="See the current price for the service")
    currency = forms.CharField(required=False)

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)  # Expect user to be passed during form initialization
    #     super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        # print(kwargs)
        # Extract the instance if it exists
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['style'] = 'background-color: #e9ecef;'
        self.fields['currency'].widget.attrs['readonly'] = True
        self.fields['currency'].widget.attrs['style'] = 'background-color: #e9ecef;'

        if instance:
            # Set the price field to the actual price for today
            self.fields['price'].initial = instance.price
            self.fields['currency'].initial = instance.currency

    class Meta:
        model = Service
        fields = ['status', 'service_type', 'service_name', 'billing_frequency', 'start_date',
                  'finish_date', 'price', 'currency', 'contract', 'resource', 'description']
        readonly_fields = ['price', 'currency']
        widgets = {
            'status': forms.Select(),
            'service_name': forms.Select(),
            'service_type': forms.Select(),
            'billing_frequency': forms.Select(),
            'contract': forms.Select(),
            'resource': forms.Select(),
            'description': forms.Textarea(),
            'is_active': forms.CheckboxInput(),
        }

    # def save(self, commit=True):
    #     # Save the service instance
    #     service = super().save(commit=False)
    #
    #     # Set the price if provided
    #     # print(self.cleaned_data)
    #     # if 'price' in self.cleaned_data and self.cleaned_data['price'] is not None:
    #         # if not self.user:
    #         #     raise ValueError("User must be provided to set the price.")
    #         # service.set_user(self.user)  # Set the current user for price tracking
    #         # service.price = self.cleaned_data['price']  # This triggers the `price` setter logic
    #
    #     if commit:
    #         service.save()
    #     return service