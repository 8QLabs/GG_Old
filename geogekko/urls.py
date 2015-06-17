from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.debug import default_urlconf


urlpatterns = patterns('core.views',
    url(r'^index/dashboard$', 'dashboard'),
    url(r'^index/create$', 'create_index'),
)

urlpatterns += patterns('ui.views',
    url(r'^map$', 'map'),
)

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'Project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', default_urlconf),
)
