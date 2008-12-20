from django.conf.urls.defaults import *

urlpatterns = patterns('',
        url(r'^(\d+)/members/$', 'groups.views.members', name="group_members"),
    )
