from datetime import datetime
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from voting.models import Vote

CATEGORY_CHOICES =(
    (1, _("Civil Rights")),
    (2, _("Security")),
    (3, _("Economy")), 
    (4, _("Education")),
    (5, _("Nature")),
    (6, _("Communications")),
    (7, _("Energy")),
    (8, _("Foreign Policy")),
    (9, _("Health Care")),
)
class Question(models.Model):
    """
    A questions posted by a User.
    """
    adder        = models.ForeignKey(User)
    added        = models.DateTimeField(_('created'), default=datetime.now)
    modified     = models.DateTimeField(_('modified'), default=datetime.now)
    text         = models.CharField(_('Q:'), max_length=256)
    public       = models.BooleanField(_('public'), default=True)
    flagged      = models.BooleanField(_('flagged as inappropriate'), default=False)
    category     = models.CharField(_('Category'), choices=CATEGORY_CHOICES, max_length=1)
    tags         = TagField()


    #class Meta:
    #    ordering = ('-added')
        
    def __unicode__(self):
        return _('by %(user)s: %(text)s%(more)s') % dict(user=self.adder, text=self.text[:60], more=len(self.text)>60 and '...' or '')

    def save(self, **kwargs):
        self.modified = datetime.now()
        super(Question, self).save(kwargs)
        
    def delete(self):
        my_ctype = ContentType.objects.get_for_model(Question)
        for v in Vote.objects.filter(content_type=my_ctype, object_id=self.id):
            v.delete()
        super(Question, self).delete()

    def category_name(self):
        return unicode(CATEGORY_CHOICES[int(self.category)-1][1])