from django import forms
from django.utils.translation import ugettext_lazy as _

class AwayForm(forms.Form):
    
    away_message = forms.CharField(label=_(u"Message"))
    
    def save(self, project_member):
        project_member.away = True
        project_member.away_message = self.cleaned_data['away_message']
        project_member.away_since = datetime.now()
        project_member.save()

