from datetime import datetime
# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import models as admin_models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes import generic
#apps imports
from tagging.fields import TagField
try:
    from notification import models as notification
except ImportError:
    notification = None

OPEN_POLICY, APPROVAL_POLICY = range (0,2)
POLICY_CHOICES = (
    (OPEN_POLICY, _("Open")),
    (APPROVAL_POLICY, _("Approval required")),
)

class AssociatedContent:
    pass    
class Group(models.Model):
    """
    >>> g = Group.objects.create(slug='foo_group', name='foo group')
    >>> x = User.objects.create(username="MrX")
    >>> g.creator = x
    >>> g.has_member(x)
    True
    >>> g.creator.username
    u'MrX'
    >>> from tagging.models import Tag
    >>> c = Tag.objects.create(name="Foo")
    >>> g.add_content(content=c, distinction='my tag')
    >>> c == g.get_content(distinction='my tag')[0]
    True
    >>> [(l.action_flag, l.change_message, l.content_type, l.object_id) for l in g.log.all()]
    [(1, u'MrX added Foo as my tag', <ContentType: tag>, u'1'), (1, u'MrX added MrX as creator', <ContentType: user>, u'1')]


    """
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=80)
    description = models.TextField(_('description'))
    location = models.CharField(_('location'), max_length=80, default="global")
    policy = models.SmallIntegerField(choices=POLICY_CHOICES, default=OPEN_POLICY, help_text=_("Choose the way new members can join this group"))
    parent = models.ForeignKey('self', null=True, editable=False)
    created = models.DateTimeField(_('created'), default=datetime.now, editable=False)
    modified = models.DateTimeField(_('modified'), default=datetime.now, editable=False)
    members = models.ManyToManyField(User, through='Membership', verbose_name=_('Members'), editable=False)
    deleted = models.BooleanField(_('deleted'), default=False, editable=False)
    
    public = models.BooleanField(_('public'), default=True, editable=False)
    tags = TagField()
    
    def has_member(self, user):
        
        if user.is_authenticated():
            if Membership.objects.filter(group=self, user=user):
                return True
        return False

    if notification:
        def notify (self, note_type, d):
            d.update ({'group': self})
            notification.send(self.members.all(), note_type, d)
            #if note_type == "groups_new_member":
            #    notification.send(d["new_member"], "groups_joined", d)
    else:    
        def notify (self, note_type, dict):
            pass
    
    def _get_creator(self):
        # returns the 1st member - the creator
        return Membership.objects.filter(group=self)[0].user
    def _set_creator(self, user):
        try:    
            self.add_member(user, Group.creator_role)
        except AttributeError:
            Group.creator_role = Role.objects.get(title='creator')
            self.add_member(user, Group.creator_role)            
    creator = property(_get_creator,_set_creator)
    
    def membership(self):
        return Membership.objects.filter(group=self)
        
    def add_member(self, member, role, by=False):
        ''' adds a member to the group. Returns True unless member is already in the group
        '''
        if not self.id: 
            self.save()
        if self.has_member(member):
            return False
        m = Membership.objects.create(group = self, 
            user = member,
            role= role)
        # TODO: add default permissions from role
        m.permissions = role.default_permissions.all();
        self.notify ("groups_new_member", {"group": self, "member": member, "role":role})
        self.log.create(user=by or member, 
            content_type = ContentType.objects.get_for_model(member), 
            object_id = member.id, 
            action_flag = admin_models.ADDITION, 
            change_message = _("%(by)s added %(user)s as %(role)s") % dict(by=by or member, user=member, role=unicode(role)),
            )
        return True
    
    def get_content (self, distinction):
        # return AssociatedContent.objects.filter(group=self, distinction=distinction).values('content_object')
        return [a.content_object for a in AssociatedContent.objects.filter(group=self, distinction=distinction)]
    def add_content (self, content, distinction='', inheritable=True, by=False):
        by = by or self.creator
        content_type = ContentType.objects.get_for_model(content)
        oid = content.id
        AssociatedContent.objects.create(group = self,  
            content_type = content_type,
            object_id = oid,
            distinction = distinction,
            inheritable = inheritable,
        )
        
        self.notify ("groups_new_content", {"group":self, "content": content, "by": by})
        message=_("%(by)s added %(content)s") % dict(by=by, content=content)
        if distinction:
            message += _(" as %(distinction)s") % dict (distinction=distinction)
        self.log.create(user=by, 
            content_type=content_type,
            object_id = oid, 
            action_flag=admin_models.ADDITION, 
            change_message=message)
        
    def create_sub_group(self, *args, **kwargs):
        return self.objects.create (parent=self, *args, **kwargs)
        
    def __unicode__(self):
        return ",".join((self._meta.verbose_name,self.name))
        
class Role(models.Model):
    '''
    This models holds system wide roles as well as type-specific roles. Basic roles are created in post_syncdb
    '''
    group = models.ForeignKey(Group, null=True, blank=True, related_name='roles')          # use null for global roles - e.g. maker, guest
    title = models.CharField(_('Title'), max_length=30)
    default_permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True)

    def __unicode__(self):
        if self.group:
            return _("%(title)s in %(group)s") % dict(title=self.title, group=self.group)
        else:
            return self.title

class Membership(models.Model):
    """
    Setting relationship between users and groups.
    """
    # stuff needed by the ManyToMany relationship
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    # Membership attributes
    joined = models.DateTimeField(_('joined'), default=datetime.now)
    role = models.ForeignKey(Role, verbose_name=_('role'), max_length=30)
    merits = models.IntegerField(default=0)
    permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True)
    # member away
    away = models.BooleanField(_('away'), default=False)
    away_message = models.CharField(_('away_message'), max_length=500, blank=True)
    away_since = models.DateTimeField(_('away since'), default=datetime.now)

    class META:
        ordering = ('joined')
        unique_together = ('user', 'group')

    def __unicode__(self):
        r = _("%(user)s is %(role)s") % dict(user=self.user, role=unicode(self.role))
        if self.group:
            r += _(" in %s") % self.group        
        return r

class AssociatedContent(models.Model):
    """
    conecting groups with content. Notable fields (shamelessly copied from django-schedule):
        distinction - what makes this specific association distinct?
        inheritable - do all related groups inherit this content?
    """
    group = models.ForeignKey(Group)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    distinction = models.CharField(_('distinction'), max_length = 20, null=True)
    inheritable = models.BooleanField(_('inheritable'), default=True)
               
class GroupsLogEntry(admin_models.LogEntry):
    group = models.ForeignKey (Group, related_name='log')
    
