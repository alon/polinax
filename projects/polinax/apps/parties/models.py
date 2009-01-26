from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from answers.models import Answer

from groups.models import Group, Role, Membership

class Feed(models.Model):
    user =   models.ForeignKey(User)
    url =   models.URLField()
    last_read = models.DateTimeField(default=datetime(1970,1,1))
    public = models.BooleanField(default=False)
    
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
    
    def add_candidate(self, user, feed, commit=True):
        if self.add_member(user, Role.objects.get(group=self, title="p_candidate")):
            f = Feed.objects.create(user=user, url=feed)
            self.add_content (f, "pending_feed", by=user)
            # don't increment as we're still pending self.candidates_count += 1
            if commit:
                self.save()
            return True
        else:
            return False

    def candidates(self):
        return self.membership().filter(role__title="candidate").values_list('user', flat=True)

def create_party_roles(sender, instance, created, **kwargs):
    if created:
         Role.objects.create(title='candidate', group=instance)
         Role.objects.create(title='p_candidate', group=instance)
signals.post_save.connect(create_party_roles, sender=Party)

def update_answer_count(sender, instance, created, **kwargs):
    if created:
        p=Membership.objects.get(user=instance.adder, role__title='candidate').group.party
        p.answers_count += 1
        p.save()
signals.post_save.connect(update_answer_count, sender=Answer)

