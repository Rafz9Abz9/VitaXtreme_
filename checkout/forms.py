from django import forms
from django_countries import countries
from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control',
        'autocomplete': 'off',
    }), required=True)

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
        model = Order
        fields = ('first_name', 'last_name', 'email',  'phone', 'street_address',
                  'post_code', 'city', 'state', 'country', 'shipping_method', 'shipping_price', 'sub_total', 'grand_total', 'stripe_pid')
