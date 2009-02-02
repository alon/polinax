from django.conf.urls.defaults import *

# for voting
from voting.views import vote_on_object
from questions.models import Question

urlpatterns = patterns('',
    url(r'^$', 'questions.views.questions', name="all_questions"),
    url(r'^mine/$', 'questions.views.my_questions', name="my_questions"),
    url(r'^add/$', 'questions.views.add_q', name="add_question"),
    url(r'^(\d+)/$', 'questions.views.question', name="view_question"),
   url(r'^(\d+)/delete/$', 'questions.views.delete_q', name="delete_question"),
   url(r'^(\d+)/report/$', 'questions.views.report_q', name="report_question"),
    
    # for voting
    url(r'^(?P<object_id>\d+)/(?P<direction>up|clear)vote/?$',
        vote_on_object, dict(
            model=Question,
            template_object_name='question',
            template_name='questions/question.html',
            allow_xmlhttprequest=True), name="vote_on_question"),

)
