from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def home (request, guests_template, users_url):
    if request.user.is_authenticated():
        return HttpResponseRedirect(users_url)
    else:
        return render_to_response(guests_template, context_instance=RequestContext(request))