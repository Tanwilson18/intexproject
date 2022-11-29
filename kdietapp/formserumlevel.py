from django import forms
from .models import serum_level


class serum_level_form(forms.ModelForm):
    class Meta:
        model = serum_level
        fields = '__all__'
