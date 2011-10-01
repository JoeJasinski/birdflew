from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.measure import D
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.cache import cache
from django.dispatch import dispatcher
from django.db.models import signals
from . import models

def stats(request, template_name=""):
    urls = cache.get('dcore_stats_urls', None)
    if not urls:    
        urls = models.UrlModel.objects.all()
        cache.set('dcore_stats_urls', urls, 300)
        from_cache = False
    else:
        from_cache = True
    context = {'urls':urls,'from_cache':from_cache,}
    return render_to_response(template_name, 
        context, context_instance=RequestContext(request))


def del_dcore_stats_urls(sender, instance, **kwargs):
    cache.delete('dcore_stats_urls')
signals.post_save.connect(del_dcore_stats_urls)