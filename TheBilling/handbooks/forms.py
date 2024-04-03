from django import forms

from handbooks.models import LegalForm


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
