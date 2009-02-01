'''
This is the party test script:

>>> u1=User.objects.create(username='u1')
>>> u2=User.objects.create(username='u2')
>>> u3=User.objects.create(username='u3')
>>> p1=Party.objects.create(slug='a', name='p1')
>>> p2=Party.objects.create(slug='b', name='p2')
>>> p1.add_candidate(u1, ' ')
True
>>> p1.add_candidate(u2, ' ')
True
>>> p2.add_candidate(u3, ' ')
True
>>> Party.objects.get_member_count_in_bulk([p1, p2], 'candidate')
{1: 2, 2: 1}
>>>
'''
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
    
class PartyManager(models.Manager):
    def get_candidate_count_in_bulk(self, groups):
        """
        Get a dictionary mapping object ids to total score and number
        of votes for each object.
        """
        queryset = Membership.objects.filter(
            group__in=groups).extra(
            select={
                'count': 'COUNT(1)',
        }).values('group', 'count')
        queryset.query.group_by = ['group_id']
        r = {}
        for g in queryset:
            r[g['group']] = g['count']
        return r
    
class Party(Group):
    home =   models.URLField(null=True, blank=True)
    answers_count = models.IntegerField(default=0)
    candidates_count = models.IntegerField(default=0)

    objects = PartyManager()
    
    class Meta:
        ordering = ['-answers_count', 'name']
        
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return ("view_party", [self.id])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def add_candidate(self, user, feed, commit=True):
        if self.add_member(user, Role.objects.get(group=self, title="candidate")):
            f = Feed.objects.create(user=user, url=feed)
            self.add_content (f, "candidate_feed", by=user)
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

