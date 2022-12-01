from django import forms
from .models import serum_levels


class serum_levels_form(forms.ModelForm):
    class Meta:
        model = serum_levels
        fields = ('results_date', 'potassium_level', 'phosphorus_level',
                  'sodium_level', 'creatinine_level', 'albumin_level', 'blood_sugar_level')
