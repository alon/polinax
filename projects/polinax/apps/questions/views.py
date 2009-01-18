from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext, ugettext_lazy as _
# TODO: from voting.models import Vote

from questions.models import Question, CATEGORY_CHOICES
from questions.forms import QuestionForm

def redirect_to_next(request,view):
    ''' A helper function that returns an http redirect request 
    '''
    return HttpResponseRedirect(request.REQUEST.get("next", reverse(view)))

def user_questions (request):
    ''' a Django context processor that added the user's own questions and the questions he voted for
    '''
    if request.user.is_authenticated():
        c = dict (user_qs = Question.objects.filter(adder=request.user),
                # user_voted_qs = Vote.objects.filter(user=request.user).values_list('object', flat=True).order_by("-added")
                )
    else:
        c = dict (user_qs = [], user_voted_qs=[])
    return c 

def questions(request):
    qs=Question.objects.filter(public=True).order_by('-added')
    if 'c' in request.GET:
        qs=qs.filter(category=request.GET['c'])
    if 'q' in request.GET:
        qs=qs.filter(text__icontains=request.GET['q'])
    
    return render_to_response("questions/questions.html", {
        "categories": CATEGORY_CHOICES,
        "questions": qs,
    }, context_instance=RequestContext(request, processors=[user_questions]))


@login_required
def my_questions(request):
    return render_to_response("questions/my_questions.html", {}, 
        context_instance=RequestContext(request, processors=[user_questions]))

@login_required
def add_q(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.adder = request.user
            q.save()
            return redirect_to_next(request, "my_questions")
    else:
        form = QuestionForm()
    print form
    return render_to_response("questions/add_q.html", {"form":form}, 
        context_instance=RequestContext(request))

@login_required
def delete_q(request, id):
    q = get_object_or_404(Question, id=id)
    if request.user == q.adder:
        q.delete()
        request.user.message_set.create(message=ugettext("Question Deleted"))
        
    return redirect_to_next(request, "questions.views.my_questions")
    
