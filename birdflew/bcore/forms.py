from django import forms 
from .models import UrlModel


class UrlForm(forms.ModelForm):
    
    class Meta:
        model = UrlModel