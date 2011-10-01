from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/', 'bcore.views.stats', 
        {'template_name':'bcore/stats.html'}, 
        name="bcore_stats"),
    url(r'^', include('birdflew.api.urls')),
)
