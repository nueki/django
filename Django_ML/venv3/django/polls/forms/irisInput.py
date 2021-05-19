from django import forms

class IrisInputForm(forms.Form):
    input = forms.DecimalField(decimal_places=1)