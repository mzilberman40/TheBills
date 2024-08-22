from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django import forms
from .models import UserProfile

User = get_user_model()


class UserForm:
    """
    Form that uses built-in UserCreationForm to handel user creation
    """
    # username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
    email = forms.EmailField(required=True)
    # is_active = forms.BooleanField(required=True, widget=forms.CheckboxInput())
    # is_staff = forms.BooleanField(required=True, widget=forms.CheckboxInput())
    # is_superuser = forms.BooleanField(required=True, widget=forms.CheckboxInput())
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        # fields = ('username', 'password1', 'password2')
        # fields = ('email', 'password1', 'password2')
        fields = ('email', 'password1', 'password2')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AuthForm(AuthenticationForm):
    """
    Form that uses built-in AuthenticationForm to handel user auth
    """
    # username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
    # email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    """
    Basic model-form for our user profile
    """
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
    avatar = forms.ImageField(required=False)
    telephone = forms.CharField(max_length=255, required=False, widget=forms.TextInput())
    address = forms.CharField(max_length=100, required=False, widget=forms.TextInput())

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'avatar', 'telephone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserAlterationForm(forms.ModelForm):
    """
    Basic model-form for our user
    """
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
