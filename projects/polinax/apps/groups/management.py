from django.db.models import signals
from django.utils.translation import ugettext_noop as _
from django.contrib.auth.models import Permission

from groups.models import Role

from groups import models as groups

def create_common_roles(app, created_models, verbosity, **kwargs):
    # create default roles
    r = Role.objects.create(title='creator')
    for p in Permission.objects.all():
        r.default_permissions.add(p)
    Role.objects.create(title='editor')
    Role.objects.create(title='follower')
    Role.objects.create(title='member')
signals.post_syncdb.connect(create_common_roles, sender=groups)

try:
    from notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("groups_new_member", _("New Group Member"), _("A new member has joined a group"), default=1)
        notification.create_notice_type("groups_new_content", _("New Content"), _("A new content was added to a group"), default=2)
    signals.post_syncdb.connect(create_notice_types, sender=notification)

except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"

