from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from questions.models import Question
from voting.models import Vote

class AnswerManager(models.Manager):
    def public(self):
        return self.filter(public=True)
        
    def count_for(self, objects):
        """
        Get a dictionary mapping object ids to total score and number
        of votes for each object.
        """
        queryset = self.filter(
            q__in=objects).extra(select={
                'count': 'COALESCE(COUNT(url), 0)',
        }).values_list('q__id', 'count')
        print queryset
        # queryset.query.group_by.append('object_id')
        count_dict = {}
        for id, count in queryset:
            count_dict[id] = {'count': int(count)}
        print count_dict
        return count_dict

        
class Answer(models.Model):
    """
    A questions posted by a User.
    """
    adder        = models.ForeignKey(User, related_name='answers')
    q            = models.ForeignKey(Question, related_name='answers')
    added        = models.DateTimeField(_('created'), default=datetime.now)
    summary      = models.CharField(max_length=256)
    text         = models.TextField()
    url          = models.URLField()
    public       = models.BooleanField(_('public'), default=True)
    flagged      = models.BooleanField(_('flagged as inappropriate'), default=False)

    objects = AnswerManager()

    #class Meta:
    #    ordering = ( '-added')
        
    def __unicode__(self):
        return _('by %(user)s: %(text)s%(more)s') % dict(user=self.adder, text=self.text[:60], more=len(self.text)>60 and '...' or '')
        
    def delete(self):
        my_ctype = ContentType.objects.get_for_model(Answer)
        for v in Vote.objects.filter(content_type=my_ctype, object_id=self.id):
            v.delete()
        super(Answer, self).delete()
