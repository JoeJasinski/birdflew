from django.conf.urls.defaults import patterns, include, url

from piston.resource import Resource
from birdflew.api.handlers import ( 
    LookupURLsHandler, RegisterURLsHandler, WhoamiHandler, LookupURLsHandler ) 

ad = {}

lookupurls_handler = Resource(handler=LookupURLsHandler, **ad)
registerurls_handler = Resource(handler=RegisterURLsHandler, **ad)
whoami_handler = Resource(handler=WhoamiHandler, **ad)
logs_handler = Resource(handler=LookupURLsHandler, **ad)


version_one_url = patterns('',
    url(r'^lookupurls/$', lookupurls_handler, {'emitter_format':'xml',}, 
       name='api_lookupurls'),
    url(r'^registerurls/$', registerurls_handler, {'emitter_format':'xml',}, 
       name='api_registerurls'),
    url(r'^whoami/$', registerurls_handler, {'emitter_format':'xml', }, 
       name='api_whoami'),
    url(r'^logs/$', logs_handler, {'emitter_format':'xml', }, 
       name='api_logs'),
)

urlpatterns = patterns('',
    (r'^v1/', include(version_one_url)),
)
