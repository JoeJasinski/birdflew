from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from .views import v1_views, v2_views

version_one_url = patterns('',

    url(r'^lookupUrls$', csrf_exempt(v1_views.lookupurlsView.as_view()), 
        {}, 
        name='api_lookupurls'),

    url(r'^registerUrls$', csrf_exempt(v1_views.registerurlsView.as_view()), 
        {}, 
        name='api_registerurls'),

    url(r'^whoami$', csrf_exempt(v1_views.whoamiView.as_view()), 
        {'emitter_format':'xml', }, 
        name='api_whoami'),

#    url(r'^logs/$', logs_handler, {'emitter_format':'xml', }, 
#       name='api_logs'),
)


version_two_url = patterns('',

    url(r'^users/$', csrf_exempt(v2_views.users_list.as_view()), 
        {}, 
        name='api_users_list'),

    url(r'^users/(?P<username>[-_\w]{1,30})$', csrf_exempt(v2_views.users_detail.as_view()), 
        {}, 
        name='api_users_detail'),

)

urlpatterns = patterns('',
    (r'^v1/', include(version_one_url)),
    (r'^v2/', include(version_two_url)),
)
