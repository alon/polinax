from datetime import datetime
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from voting.managers import VoteManager

SCORES = (
    (u'+1', +1),
    (u'-1', -1),
)

class Question(models.Model):
    """
    A questions posted by a User.
    """
    adder        = models.ForeignKey(User)
    added        = models.DateTimeField(_('created'), default=datetime.now)
    modified     = models.DateTimeField(_('modified'), default=datetime.now)
    text         = models.CharField(_('Q:'), max_length=256)

    def __unicode__(self):
        return _('by %(user)s: %(text)s%(more)s') % dict(user=self.user, text=self.text[:60], more=len(self.text)>60 and '...' or '')

    def save(self, **kwargs):
        self.modified = datetime.now()
        super(Question, self).save(kwargs)
    

