from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from groups.models import Group, Membership
from groups.forms import AwayForm

def members(request, id, form_class=AwayForm,
        template_name="groups/members.html"):
    group = get_object_or_404(Group, id=id)
    group_members = Membership.objects.filter(group=group)
    
    if group.deleted:
        raise Http404
    
    is_member = group.has_member(request.user)
    try:
        group_member = group_members.get(user=request.user)
    except Membership.DoesNotExist:
        group_member = None

    away_form = None
    if is_member and request.method == "POST":
        if request.POST["action"] == "set_away":
            away_form = form_class(request.POST)
            if away_form.is_valid():
                away_form.save(group_member)
                away_form = form_class()
        elif request.POST["action"] == "set_back":
            group_member.away = False
            group_member.save()
    
    if away_form is None:
        away_form = form_class()
    
    active_members = group_members.filter(away=False)
    away_members = group_members.filter(away=True).order_by('away_since')
    
    return render_to_response(template_name, {
        "group": group,
        "is_member": is_member,
        "group_member": group_member,
        "away_form": away_form,
        "active_members": active_members,
        "away_members": away_members,
    }, context_instance=RequestContext(request))
members = login_required(members)
