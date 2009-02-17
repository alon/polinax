from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import direct_to_template, redirect_to

from account.openid_consumer import PinaxConsumer

from django.contrib import admin
admin.autodiscover()

import os

urlpatterns = patterns('',
    # url(r'^$', direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r'^$', 'about.views.home', { "guests_template": "homepage.html", "users_url": "questions/"}, name="home"),
    
    (r'^about/', include('about.urls')),
    (r'^account/', include('account.urls')),
    (r'^openid/(.*)', PinaxConsumer()),
    (r'^profiles/', include('profiles.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^announcements/', include('announcements.urls')),
    
    (r'^comments/', include('threadedcomments.urls')),

    (r'^groups/', include('groups.urls')),
    (r'^questions/', include('questions.urls')),
    (r'^parties/', include('parties.urls')),
    (r'^avatars/', include('avatar.urls')),
    (r'^answers/', include('answers.urls')),

    (r'^admin/(.*)', admin.site.root),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), "site_media")}),
    )

