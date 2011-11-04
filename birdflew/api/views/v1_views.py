from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.cache import cache
from django.db.models import signals
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from bcore.models import UrlModel
from api.forms import RawUrlForm
from api import validators 
from api.views import BlankView, prepxml, messagexml

from lxml import etree
from lxml.builder import ElementMaker 


class lookupurlsView(BlankView):
    
    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):
        url_response = cache.get('api_lookupuurlsView')
        if not url_response:
            url_list = UrlModel.objects.values('url')
            E = ElementMaker()
            URLS = E.urls
            URL = E.url
            status=200
            
            xml = URLS(*map(lambda x: URL(x['url']), url_list))
            url_response = prepxml(etree.tostring(xml), status)
            cache.set('api_lookupuurlsView', url_response, settings.DEFAULT_CACHE_TIMEOUT)

        return url_response


@receiver(signals.post_save, sender=UrlModel)
def del_api_lookupuurlsView(sender, instance, **kwargs):
    cache.delete('api_lookupuurlsView')


class registerurlsView(BlankView):

    @method_decorator(csrf_exempt)
    @method_decorator(validators.RateLimitDecorator)
    def post(self, request, *args, **kwargs):
    
        form = RawUrlForm(data=request.raw_post_data)
        if form.is_valid():
            url_list = form.cleaned_data.get('urls')
            for u in url_list:
                url_model, created = UrlModel.objects.get_or_create(url=u,)
                
            num_added = len(url_list)
            xml = messagexml("Added %s Records" % (num_added))
        else:
            xml = messagexml('Error with form validation: %s' % form.errors)
            print form.errors
        
        status=201
        return prepxml(etree.tostring(xml), status)


class whoamiView(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):
         return HttpResponse(settings.WHOAMI, status=200)
