from datetime import datetime

from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from groups.models import Group
from wiki.views import get_articles_for_object
# @@@ from photos.models import Pool

try:
    from notification import models as notification
except ImportError:
    notification = None

# @@@ from wiki.views import get_articles_for_object

# @@@ this is based on Tribes -- can we re-use anything?

class Law(Group):
    """
    a law is a group of people working together on a law.
    """
    tags = TagField()
    
    class Meta:
        verbose_name = _('Law')
        verbose_name_plural = _('Laws')


    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ("view_law", [self.id])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def wiki_articles(self):
        return get_articles_for_object(self)
    


from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Law):
        law = instance.content_object
        law.modified = datetime.now()
        law.save()
        if notification:
            notification.send(law.members.all(), "laws_new_comment", {"user": instance.user, "law": law, "comment": instance})

signals.post_save.connect(new_comment, sender=ThreadedComment)
