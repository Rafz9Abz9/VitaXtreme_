from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your name',
        'class': 'form-control input-lg'
    }), required=True)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address',
        'class': 'form-control input-lg'
    }), required=True)

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your phone number',
        'class': 'form-control input-lg'
    }), required=True)

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Subject',
        'class': 'form-control input-lg'
    }), required=True)

    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter Message',
        'class': 'form-control input-lg'
    }), required=True)

    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'subject', 'message')
