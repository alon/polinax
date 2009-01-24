from django.conf.urls.defaults import *

# for voting
from voting.views import vote_on_object
from questions.models import Question

urlpatterns = patterns('',
    url(r'^$', 'parties.views.parties', name="all_parties"),
    # url(r'^mine/$', 'parties.views.my_parties', name="my_parties"),
    url(r'^(\d+)/$', 'parties.views.party', name="view_party"),
)
