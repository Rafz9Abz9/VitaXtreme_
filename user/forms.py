from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django_countries import countries
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext as _

from .models import CustomUser, ShippingAddress


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'autocomplete': 'off',
        }),
        required=True,
        min_length=8
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
            'autocomplete': 'off',
        }),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        email = cleaned_data.get('email')
        email_validator = EmailValidator(
            message="Enter a valid email address.")

        if CustomUser.objects.filter(email=email).exists():
            self.add_error(
                'email', 'An account with this email already exists. Please use a different email address.')

        try:
            email_validator(email)
        except forms.ValidationError as e:
            self.add_error('email', e)

    class Meta:
        model = CustomUser
        fields = ('email',  'password1', 'password2')


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',
        'id': 'login-email',
    }), required=True)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'id': 'login-password',
        }),
        required=True,
    )


class PasswordChangeForm(PasswordChangeForm):

    def cleaned_data(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')

        if old_password and old_password == new_password1:
            raise forms.ValidationError(
                "New password must be different from the old password.")

        return new_password1


class PasswordResetForm(PasswordResetForm):
    # Add new password and password confirmation fields
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'autocomplete': 'new-password'
        }),
        label=_("New Password"),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'autocomplete': 'new-password'
        }),
        label=_("Confirm New Password"),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields.pop('email')

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return new_password2

    def save(self, commit=True):
        # Reset the user's password here
        user = self.user  # Use the user obtained from the form's initialization
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()

        return user


class ShippingAddressForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'street address',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    post_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Post Code',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'city ',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'state/province ',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    country = forms.ChoiceField(
        choices=countries,  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ShippingAddress
        fields = ('email',  'phone', 'street_address',
                  'post_code', 'city', 'state', 'country')
