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

class Group(models.Model):
        
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=80)
    description = models.TextField(_('description'))
    location = models.CharField(_('location'), max_length=80, default="global")
    policy = models.SmallIntegerField(choices=POLICY_CHOICES, default=OPEN_POLICY, help_text=_("Choose the way new members can join this group"))

    # TBD: not used yet, I added it as large groups need to be broken to sub groups
    parent_group = models.ForeignKey('self', null=True, blank=True)

    created = models.DateTimeField(_('created'), default=datetime.now)
    modified = models.DateTimeField(_('modified'), default=datetime.now)

    members = models.ManyToManyField(User, through='Membership', verbose_name=_('users')) # tried adding related_name='groups' and failed
    deleted = models.BooleanField(_('deleted'), default=False)
    
    private = models.BooleanField(_('public'), default=True)
    
    tags = TagField()

    def has_member(self, user):
        if user.is_authenticated():
            #if ProjectMember.objects.filter(project=self, user=user).count() > 0: # @@@ is there a better way?
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
    
    @property
    def creator(self):
        # returns the oldest, most important user
        return Membership.objects.filter(group=self, importance=1.0)[0].user
        
    def membership(self):
        return Membership.objects.filter(group=self)
        
    def add_member(self, by, new_member, role='member', importance=False):
        if not self.id: self.save()
        m = Membership(group = self, 
            user = new_member,
            role= role, 
            importance = importance or role.default_importance)
        """ TODO: add default permissions
        init_perms = m.role.filter(group = self.group) or self.role.filter(in_group__isnull=True)
        for p in init_perms:
            self.permissions.add(p)
        """
        m.save()

        self.notify ("groups_new_member", {"new_member": new_member})
        self.log.create(user=by, 
            content_type = ContentType.objects.get_for_model(new_member), 
            object_id = new_member.id, 
            action_flag = admin_models.ADDITION, 
            change_message = _("%(by)s added %(user)s as %(role)s") % dict(by=by,user=new_member, role=role),
            )
    
    # TODO: untested. By connecting group to content we can get a good log of all content changes.  
    def add_content (self, by, new_content, distinction='', inheritable=True):
        if not self.id: self.save()
        content_type = ContentType.objects.get_for_model(new_content)
        oid = new_content.id
        a = AssociatedContent(group = self,  
            content_type = content_type,
            object_id = oid,
            distinction = distinction,
            inhertiable = inheritable,
        )
        a.save()
        
        self.notify ("groups_new_content", {"new_content": new_content})
        message=_("%(by)s added %(new_content)s") % dict(by=by, content=new_content)
        if distinction:
            message += _(" as %(distniction)s") % dict (distinction=distinction)
        self.log.create(user=by, 
            content_type=content_type, 
            object_id = oid, 
            action_flags=admin_models.ADDITION, 
            change_message=message)
        
    def create_sub_group(self, *args, **kwargs):
        return self.objects.create (parent_group=self, *args, **kwargs)
        
    def __unicode__(self):
        return self.name
        
class Role(models.Model):
    '''
    This models holds system wide roles as well as type-specific roles. Basic roles are created in post_syncdb
    '''
    group = models.ForeignKey(Group, null=True, blank=True)          # use null for global roles - e.g. maker, guest
    title = models.CharField(_('relation'), max_length=30)
    default_importance = models.FloatField(default=0.0)
    default_permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True)

    def __unicode__(self):
        if self.group:
            return _("%s in %s") % (self.title, self.group)
        else:
            return self.title

class Membership(models.Model):
    """
    Setting relationship between users and groups. Notable fields:
        role - short text describing the relationship  - e.g. 'founder', 'adviser'..
        importnace - a 0-1 float with 1 for the creator and 0 for the non-member
    """
    # stuff needed by the ManyToMany relationship
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    # Membership attributes
    joined = models.DateTimeField(_('joined'), default=datetime.now)
    role = models.ForeignKey(Role, verbose_name=_('role'), max_length=30)
    importance = models.FloatField(default=0.0)
    permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True)
    # member away
    away = models.BooleanField(_('away'), default=False)
    away_message = models.CharField(_('away_message'), max_length=500, blank=True)
    away_since = models.DateTimeField(_('away since'), default=datetime.now)

    class META:
        ordering = ['joined']

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
    
