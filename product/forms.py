from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'images']
        widgets = {
            'images': forms.ClearableFileInput(attrs={'multiple': True}),
        }
