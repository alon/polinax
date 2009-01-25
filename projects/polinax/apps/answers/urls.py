from django.conf.urls.defaults import *

# for voting
from voting.views import vote_on_object
from answers.models import Answer

urlpatterns = patterns('',
    # for voting
    url(r'^(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, dict(
            model=Answer,
            template_object_name='a',
            template_name='kb/link_confirm_vote.html',
            allow_xmlhttprequest=True), name="vote_on_answer"),
)