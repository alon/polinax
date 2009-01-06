from django.conf.urls.defaults import *

from laws.models import Law
from wiki import models as wiki_models

from laws.thing import LawThing
from laws.forms import LawForm

pt = LawThing(Law.objects.filter(deleted=False))

update_law_args = {
    'model': Law,
    'login_required': True,
    'form_class': LawForm,
    'template_name':'laws/edit_law.html',
}
law_detail_args = {
    'queryset': Law.objects.filter(deleted=False),
}
wiki_args = {
    'group_slug_field': 'id',
    'group_qs': Law.objects.filter(deleted=False),
    'is_member': (lambda user, group: group.has_member(user)),
    'is_private': (lambda group: group.private),
}

urlpatterns = \
    pt.urls(url_prefix='', name_prefix='laws') + \
    patterns('',
        url(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', kwargs = law_detail_args, name="view_law"),
        url(r'^delete/(?P<law_id>\d+)/$', 'laws.views.delete_law', name="delete_law"),
        url(r'^create/$', 'laws.views.create_law', name="create_law"),
        url(r'^update/(?P<object_id>\d+)/$', 'django.views.generic.create_update.update_object', kwargs = update_law_args, name="edit_law"),
        url(r'^your_laws/$', 'laws.views.your_laws', name="your_laws"),
        # wiki
        url(r'^(?P<group_slug>\d+)/wiki/', include('wiki.urls'), kwargs=wiki_args),
    )
