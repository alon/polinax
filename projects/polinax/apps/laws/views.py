from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext, ugettext_lazy as _

from wiki.models import Article
from wiki.views import get_real_ip
from groups.models import Role
from laws.models import Law
from laws.forms import LawForm
from django.core.urlresolvers import reverse


def your_laws(request):
    pass
    
def delete_law(request, law_id, template_name='laws/delete_law.html'):

    law = get_object_or_404(Law, pk=law_id);

    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "delete":
            law.delete();
            return HttpResponseRedirect(reverse('laws_list'))

    return render_to_response(template_name, {
        "law": law,
    }, context_instance=RequestContext(request))
    
def create_law(request, form_class=LawForm,
        template_name="laws/create_law.html"):

    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "create":
            law_form = form_class(request.POST)
            if law_form.is_valid():
                law = law_form.save()
                law.add_member (by=request.user, member=request.user, role=Role.objects.get(title='creator'))
                draft = Article(
                    title='LawDraft',
                    summary=ugettext('The draft of the proposed law.'),
                    creator = request.user,
                    group = law,
                )
                draft.save()
                law.add_content(draft, 'draft', True)
                draft.new_revision(
                    '', '', 'rst',
                    ugettext('first version'), law_form.cleaned_data['user_ip'], request.user)


                return HttpResponseRedirect(law.get_absolute_url())

    law_form = form_class(initial = {'user_ip': get_real_ip(request)})

    return render_to_response(template_name, {
        "form": law_form,
    }, context_instance=RequestContext(request))

