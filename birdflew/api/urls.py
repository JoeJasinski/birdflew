from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from . import views

version_one_url = patterns('',

    url(r'^lookupurls/$', csrf_exempt(views.lookupurlsView.as_view()), {}, 
       name='api_lookupurls'),

    url(r'^registerurls/$', csrf_exempt(views.registerurlsView.as_view()), {}, 
       name='api_registerurls'),

    url(r'^whoami/$', csrf_exempt(views.whoamiView.as_view()), {'emitter_format':'xml', }, 
       name='api_whoami'),

#    url(r'^logs/$', logs_handler, {'emitter_format':'xml', }, 
#       name='api_logs'),
)

urlpatterns = patterns('',
    (r'^v1/', include(version_one_url)),
)
