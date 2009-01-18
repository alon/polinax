from django import forms
from django.utils.translation import ugettext_lazy as _

from questions.models import Question

class QuestionForm(forms.ModelForm):
                
    text = forms.CharField(label = '',
        widget=forms.Textarea(attrs={'rows':3}),
    )
    
    class Meta:
        model = Question
        fields = ('text', 'category')

