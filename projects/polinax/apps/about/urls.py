from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {"template": "about/about.html"}, name="about"),
    
    url(r'^terms/$', direct_to_template, {"template": "about/terms.html"}, name="terms"),
    url(r'^privacy/$', direct_to_template, {"template": "about/privacy.html"}, name="privacy"),
    url(r'^dmca/$', direct_to_template, {"template": "about/dmca.html"}, name="dmca"),
    
    url(r'^what_next/$', redirect_to, {"url": "/questions/"}, name="what_next"),
)
