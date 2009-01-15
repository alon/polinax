from django.conf.urls.defaults import *

# for voting
from voting.views import vote_on_object
from bookmarks.models import Bookmark

urlpatterns = patterns('',
    url(r'^$', 'questions.views.questions', name="all_questions"),
    url(r'^(\w+)/$', 'questions.views.user_bookmarks', name="user_questions"),
    url(r'^add/$', 'questions.views.add', name="add_question"),
    url(r'^(\d+)/delete/$', 'questions.views.delete', name="delete_question"),
    
    # for voting
    (r'^(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, dict(
            model=Bookmark,
            template_object_name='q',
            template_name='kb/link_confirm_vote.html',
            allow_xmlhttprequest=True)),
)
