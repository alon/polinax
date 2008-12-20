from django import template
from groups import models as groups
from django.conf import settings
from django import forms

register = template.Library()

def show_group_members(group):
    return {"members": groups.Membership.objects.filter(group=group)}
register.inclusion_tag("groups/group_members.html")(show_group_members)

def show_member_actions(group, user):
    try:
        m = groups.Membership.objects.get(group=group, user=user)
        if m.importance == 1.0:
            c = {"can_admin": True}
        else:
            c = {"can_leave": True}

    except groups.Membership.DoesNotExist:
        if group.policy != groups.OPEN_POLICY:
            c = {"can_ask_to_join":True}
        else:
            c = {"can_join": True }
        
    c.update({"group": group, "user": user, "MEDIA_URL": settings.MEDIA_URL})
    return c
    
register.inclusion_tag("groups/member_actions.html")(show_member_actions)

