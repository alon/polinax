from django import forms
from parties.models import Party

class JoinForm(forms.Form):
    
    party = forms.ModelChoiceField(queryset=Party.objects.filter(public=True))

