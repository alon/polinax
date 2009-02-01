from django import forms
from django.utils.translation import ugettext_lazy as _
from notification import models as notification
from questions.models import Question
from django.contrib.auth.models import Permission, User

class QuestionForm(forms.ModelForm):
                
    text = forms.CharField(label = '',
        widget=forms.Textarea(attrs={'rows':3}),
    )
    
    class Meta:
        model = Question
        fields = ('text', 'category')

class ReportQuestionForm(forms.Form):
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':3}))
    
    def notify(self, from_user, q):
        editors = Permission.objects.get(codename='change_question').user_set.all() | User.objects.filter(is_superuser=True)
        notification.send_now(editors, 'question_reported', {"from":from_user, "q":q, "description": self.cleaned_data['description']})


