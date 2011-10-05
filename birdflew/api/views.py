from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.measure import D
from django.contrib.sites.models import Site
from django.conf import settings
from django.views.generic.base import View
from django.core.cache import cache
from django.db.models import signals
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from bcore.models import UrlModel
from api.forms import RawUrlForm

from lxml import etree
from lxml.builder import ElementMaker 

def prepxml(xml, status):
    
    decl = """<?xml version="1.0" encoding="utf-8"?>"""
    response = HttpResponse("%s%s" % (decl, xml), status=status, content_type="application/xml")
    response['Content-Disposition'] = 'inline; filename=test.xml'
    return response

def messagexml(message, type="error"):

    E = ElementMaker()
    MESSAGE = E.message
    if type == 'success':
        SUCCESS = E.success
        xml = MESSAGE(SUCCESS(message))
    else:
        ERROR = E.error
        xml = MESSAGE(ERROR(message)) 
    return xml   


class BlankView(View):
    
    def _xml_error(self, message):
        return etree.tostring(messagexml(message))
        
    
    def get(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)

    def post(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)

    def put(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)

    def delete(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)


class lookupurlsView(BlankView):

    def get(self, request, *args, **kwargs):
        url_response = cache.get('api_lookupuurlsView')
        if not url_response:
            url_list = UrlModel.objects.values('url')
            E = ElementMaker()
            URLS = E.urls
            URL = E.url
            status=200
            xml = URLS(*map(lambda x: URL(x), url_list))
            url_response = prepxml(etree.tostring(xml), status)
            cache.set('api_lookupuurlsView', url_response, settings.DEFAULT_CACHE_TIMEOUT)

        return url_response

def del_api_lookupuurlsView(sender, instance, **kwargs):
    cache.delete('api_lookupuurlsView')
signals.post_save.connect(del_api_lookupuurlsView)


class registerurlsView(BlankView):

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
    
        form = RawUrlForm(data=request.raw_post_data)
        if form.is_valid():
            url_list = form.cleaned_data.get('urls')
            for u in url_list:
                url_model = UrlModel(url=u)
                url_model.save()
                
            num_added = len(url_list)
            xml = messagexml("Added %s Records" % (num_added))
        else:
            xml = messagexml('Error with form validation: %s' % form.errors)
            print form.errors
        
        status=201
        return prepxml(etree.tostring(xml), status)


class whoamiView(BlankView):

    def get(self, request, *args, **kwargs):
         return HttpResponse(settings.WHOAMI, status=200)
