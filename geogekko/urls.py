from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.debug import default_urlconf


urlpatterns = patterns('core.views',
    url(r'^map$', 'map'),

    url(r'^index/dashboard$', 'dashboard'),
    url(r'^index/create$', 'create_index'),

    url(r'^data/pull_historical_tweets$', 'pull_historical_tweets'),
)

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'Project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', default_urlconf),
)
