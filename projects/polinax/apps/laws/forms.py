from django import forms
from laws.models import Law

class LawForm(forms.ModelForm):

    user_ip = forms.CharField(widget=forms.HiddenInput)
    
    class Meta:
        model = Law
        exclude = ('location', 'policy')
    