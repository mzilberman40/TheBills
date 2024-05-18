from django.forms import *
from django.core.exceptions import ValidationError
from commerce.models import *
from django.utils.text import slugify

from orgsandpeople.models import Email


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

