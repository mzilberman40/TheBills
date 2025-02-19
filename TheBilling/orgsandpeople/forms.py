from typing import cast

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, MaxLengthValidator
from django.utils.text import slugify

from library.mydecorators import tracer
from orgsandpeople.models import Email, BusinessUnit, Bank, Account, PhoneNumber
from handbooks.models import LegalForm, Country

DEBUG = 0

class MultiEmailFieldWithEmailType(forms.Field):
    @tracer(DEBUG)
    def __init__(self, *args, **kwargs):
        help_text = 'Enter emails in the format: email1, email2:type, ...'
        kwargs['widget'] = forms.TextInput(attrs={'placeholder': help_text})
        kwargs['help_text'] = help_text
        super().__init__(*args, **kwargs)

    @tracer(DEBUG)
    def to_python(self, value):
        if not value:
            return {}

        result = {}
        emails = value.split(',')
        for email_data in emails:
            email, email_type = email_data.split(':', 1) if ':' in email_data else (email_data, None)
            result[email.strip()] = slugify(email_type) if email_type else None
        return result

    @tracer(DEBUG)
    def validate(self, value):
        super().validate(value)
        for email in value:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(f"'{email}' is not a valid email address.")
        return value

class EmailForm(forms.ModelForm):
    """
    Form to create or update Email data for a user.
    """

    class Meta:
        model = Email
        fields = ['email', 'email_type', 'bu']
        exclude= ['verified']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email'
            }),
            'email_type': forms.TextInput(attrs={
                'placeholder': 'Enter Email Type'
            }),
        }
        labels = {
            'email': 'Email',
            'email_type': 'Email Type',
        }

#
# class TelegramDataForm(forms.ModelForm):
#     """
#     Form to create or update Telegram data for a user.
#     """
#
#     class Meta:
#         model = TelegramData
#         fields = '__all__'
#         # exclude = ['bu']
#         widgets = {
#             'tg_id': forms.NumberInput(attrs={
#                 'placeholder': 'Enter Telegram ID'
#             }),
#             'tg_username': forms.TextInput(attrs={
#                 'placeholder': 'Enter Telegram Username (e.g., johndoe123)'
#             }),
#             'is_bot': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }
#         labels = {
#             'tg_id': 'Telegram ID',
#             'tg_type': 'Telegram Type',
#             'tg_username': 'Telegram Username',
#             'is_bot': 'Is Bot',
#         }
#         help_texts = {
#             'tg_id': 'Unique numeric ID assigned by Telegram.',
#             'tg_username': 'Username without @ (e.g., johndoe123).',
#             'is_bot': 'Check if the account is a bot.',
#         }
#
#     def clean_telegram_username(self):
#         """
#         Custom validation for Telegram username.
#         """
#         telegram_username = self.cleaned_data.get('tg_username')
#         if telegram_username and not telegram_username.isalnum() and "_" not in telegram_username:
#             raise forms.ValidationError(
#                 "Telegram username can only contain letters, numbers, and underscores."
#             )
#         return telegram_username


class PhoneNumberForm(forms.ModelForm):
    """
    Form to create or update a phone number.
    """
    class Meta:
        model = PhoneNumber
        fields = '__all__'
        exclude= ['verified']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter phone number (e.g., +123456789)'
            }),
            'is_for_call': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_for_whatsapp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_for_SMS': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_for_telegram': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activate_date': forms.DateInput(attrs={'type': 'date'}),
            'deactivate_date': forms.DateInput(attrs={'type': 'date'}),

            # 'verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BankForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.none(),
        empty_label='Choose Country',
        label='Country',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        country_field = cast(forms.ModelChoiceField, self.fields['country'])
        country_field.queryset = Country.objects.all()

    class Meta:
        model = Bank
        fields = '__all__'
        # fields = ['name', 'short_name', 'bik', 'corr_account', 'swift', 'notes', 'country']
        exclude = ['user']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name',}),
            'short_name': forms.TextInput(attrs={'placeholder': 'short_name',}),
            'bik': forms.TextInput(attrs={'placeholder': 'National Bank Identification Code',}),
            'corr_account': forms.TextInput(attrs={'placeholder': 'Corr account',}),
            'swift': forms.TextInput(attrs={'placeholder': 'swift',}),
            'notes': forms.Textarea(attrs={'placeholder': 'notes',}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'business_unit', 'bank', 'currency', 'account_number', 'starting_balance',
                  'status', 'notes']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name',}),
            'business_unit': forms.Select(attrs={'empty_label': 'Choose Business Unit', 'label': 'Choose Business Unit'}),
            'bank': forms.Select(attrs={'empty_label': 'Choose Bank', 'label': 'Choose Bank'}),
            'currency': forms.Select(attrs={'empty_label': 'Choose Currency', 'label': 'Choose Currency'}),
            'account_number': forms.TextInput(attrs={'placeholder': 'Account Number',}),
            'starting_balance': forms.TextInput(attrs={'placeholder': 'Starting balance',}),
            'status': forms.Select(),
            'notes': forms.Textarea(attrs={'placeholder': 'notes',}),
        }


class BusinessUnitForm(forms.ModelForm):

    legal_form = forms.ModelChoiceField(
        queryset=LegalForm.objects.none(),
        empty_label='Choose Legal Form',
        label='Legal Form',
        widget=forms.Select()
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.none(),
        empty_label='Choose Country',
        label='Country',
        widget=forms.Select()
    )
    emails = MultiEmailFieldWithEmailType(required=False)

    @tracer(DEBUG)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.pop('user', None)
        self.user = user
        # Cast the field to the appropriate type to suppress the warning
        legal_form_field = cast(forms.ModelChoiceField, self.fields['legal_form'])
        legal_form_field.queryset = LegalForm.objects.all()
        # Similarly for country field
        country_field = cast(forms.ModelChoiceField, self.fields['country'])
        country_field.queryset = Country.objects.all()
        self.initial['emails'] = self.get_initial_emails()

    @tracer(DEBUG)
    def get_initial_emails(self):
        if self.instance and hasattr(self.instance, 'pk') and self.instance.pk:
            emails = self.instance.emails.all()
            return ', '.join(
                [f"{email.email}:{email.email_type}" if email.email_type else email.email for email in emails])
        return ''

    class Meta:
        model = BusinessUnit
        # fields = '__all__'
        fields = ['legal_form', 'country', 'inn', 'ogrn',
                  'first_name', 'middle_name', 'last_name',
                  'full_name', 'short_name', 'payment_name',
                  'special_status', 'notes', 'emails', 'address']
        widgets = {
            'inn': forms.TextInput(attrs={'placeholder': 'INN'}),
            'ogrn': forms.TextInput(attrs={'placeholder': 'OGRN'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'short_name': forms.TextInput(attrs={'placeholder': 'Short Name'}),
            'payment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Name'}),
            'special_status': forms.CheckboxInput(attrs={'class': "form-check-input",}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Notes', 'rows': 10}),
        }

    @tracer(DEBUG)
    def clean(self):
        cleaned_data = super().clean()
        # raise ValidationError({'emails': f'Херня0 какая-то'})

        emails = cleaned_data.get('emails')
        if emails:
            for email in emails:
                qs = Email.objects.filter(email=email)
                if self.instance.pk and qs.exclude(bu=self.instance).exists() or not self.instance.pk and qs.exists():
                    raise ValidationError({
                        'emails': f"The email addresss '{email}' is already in use by another BusinessUnit."
                    })
        # raise ValidationError({'emails': f'Херня какая-то'})
        return cleaned_data

    @tracer(DEBUG)
    def save_emails(self, instance):
        """
        Saves the email addresses associated with the given BusinessUnit instance.

        This method deletes any existing email records associated with the
        given instance and then processes the cleaned email data to create
        new email entries.
        """
        emails = self.cleaned_data.get('emails', [])
        # print(emails)
        instance.emails.all().delete()

        for email in emails:
            # Create or update email association
            # Ensure email is unique to avoid duplications (handled in the model level)
            try:
                Email.objects.create(bu=instance, email=email, email_type=emails[email])
            except ValidationError as e:
                raise ValidationError(e.message_dict)


    @tracer(DEBUG)
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set user if not already set (handle create case)
        if not instance.user_id:
            instance.user = self.user

        try:
            # Trigger model-level validation explicitly
            instance.full_clean()
        except ValidationError as e:
            # Add validation errors to the form
            for field, messages in e.message_dict.items():
                for message in messages:
                    self.add_error(field, message)
            return instance  # Return without saving to stop the process

        if commit:
            instance.save()

        # Handle email associations (if applicable)
        self.save_emails(instance)

        return instance
