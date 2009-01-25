from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext, ugettext_lazy as _
# TODO: from voting.models import Vote

from parties.forms import JoinForm
from parties.models import Party

def redirect_to_next(request,view):
    ''' A helper function that returns an http redirect request 
    '''
    return HttpResponseRedirect(request.REQUEST.get("next", reverse(view)))

def parties(request):
    parties=Party.objects.filter(public=True)
    
    return render_to_response("parties/parties.html", {
        "parties": parties,
    }, context_instance=RequestContext(request))

def party(request, id):
    party = get_object_or_404(Party, id=id)
    return render_to_response("parties/party.html", {
        "party": party,
    }, context_instance=RequestContext(request))
    
@login_required
def join(request):
    if request.method == "POST":
        form = JoinForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['party'].add_candidate(request.user):
                m = _("You are now registered as a candidate for %(party)s") % dict(party=form.cleaned_data['party'])
            else:
                m = ugettext("Registration failed. Could it be you are already registered?")
            request.user.message_set.create(message=m)
    else:
        form = JoinForm()
    return render_to_response("account/candidate_registration.html", {"form":form}, 
        context_instance=RequestContext(request))




