from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from groups.models import Role, Membership
from answers.models import Answer

from groups.models import Group, Role, Membership

class Party(Group):
    answers_count = models.IntegerField(default=0)
    candidates_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['answers_count', 'candidates_count']
        
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return ("view_party", [self.id])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def add_candidate(self, user, commit=True):
        if self.add_member(user, Role.objects.get(group=self, title="candidate")):
            self.candidates_count += 1
            if commit:
                self.save()
            return True
        else:
            return False

    def candidates(self):
        return self.membership().filter(role__title="candidate").values_list('user', flat=True)

def create_party_roles(sender, instance, created, **kwargs):
    print 'in create_party_roles'
    if created:
         Role.objects.create(title='candidate', group=instance)
signals.post_save.connect(create_party_roles, sender=Party)

def update_answer_count(sender, instance, created, **kwargs):
    if created:
        p=Memebership.objects.get(user=instance.adder, role__title='candidate').group
        p.answer_count += 1
        p.save()
signals.post_save.connect(update_answer_count, sender=Answer)

