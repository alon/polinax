from django import forms
from parties.models import Party
from django.utils.translation import ugettext_lazy as _

class JoinForm(forms.Form):
    
    party = forms.ModelChoiceField(label=_("Party")+":", queryset=Party.objects.filter(public=True))
    feed = forms.CharField(label=_("Blog feed:"))

    def save(self, user):
        # add the candidate with its feed to the selected party
        return self.cleaned_data['party'].add_candidate(user, self.cleaned_data['feed'])
