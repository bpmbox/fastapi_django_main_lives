from django import forms
from .models import WebSite

class WebSiteForm(forms.ModelForm):
    class Meta:
        model = WebSite
        fields = ('name', 'url')