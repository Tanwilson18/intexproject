from django import forms
from .models import serum_levels


class serum_level_form(forms.ModelForm):
    class Meta:
        model = serum_levels
        fields = '__all__'
