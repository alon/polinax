from django.db.models import signals
from django.utils.translation import ugettext_noop as _

from groups.models import Role

from groups import models as groups

def create_common_roles(app, created_models, verbosity, **kwargs):
    print 'creating common roles'
    # TODO: add default_permission
    r = Role(title='admin', default_importance=1.0)
    r.save()
    r = Role(title='guest', default_importance=0.0)
    r.save()
    r = Role(title='member', default_importance=0.5)
    r.save()
signals.post_syncdb.connect(create_common_roles, sender=groups)

try:
    from notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("groups_new_member", _("New Group Member"), _("A new member has joined a group"), default=1)
        notification.create_notice_type("groups_new_content", _("New Content Member"), _("A new content was added to a group"), default=1)
    signals.post_syncdb.connect(create_notice_types, sender=notification)

except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"

