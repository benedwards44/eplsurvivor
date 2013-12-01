from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'survivor.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rules/$', TemplateView.as_view(template_name="rules.html")),
    url(r'^groups/$', 'survivor.views.groups'),
    url(r'^groups/(?P<group_id>\d+)/$', 'survivor.views.group'),
    url(r'^edit_pick/(?P<pick_id>\d+)/$', 'survivor.views.edit_pick'),
    url(r'^dologout/$', 'survivor.views.dologout'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^results/(?P<week_number>\d+)/$', 'survivor.views.results'),
    url(r'', include('social_auth.urls')),
)
