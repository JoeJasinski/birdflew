from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.measure import D
from django.contrib.sites.models import Site
from django.conf import settings
from django.views.generic.base import View

from lxml import etree
from lxml.builder import ElementMaker 

def prepxml(xml, status):
    
    decl = """<?xml version="1.0" encoding="utf-8"?>"""
    response = HttpResponse("%s%s" % (decl, xml), status=status, content_type="application/xml")
    response['Content-Disposition'] = 'inline; filename=test.xml'
    return response


class BlankView(View):
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('Method not allowed', status=405)

    def post(self, request, *args, **kwargs):
        return HttpResponse('Method not allowed', status=405)

    def put(self, request, *args, **kwargs):
        return HttpResponse('Method not allowed', status=405)

    def delete(self, request, *args, **kwargs):
        return HttpResponse('Method not allowed', status=405)


class lookupurlsView(BlankView):

    def get(self, request, *args, **kwargs):
    
        url_list = ['10.0.0.1','10.0.0.2',]
        E = ElementMaker()
        URLS = E.urls
        URL = E.url
        status=200
        xml = URLS(*map(lambda x: URL(x), url_list))
        return prepxml(etree.tostring(xml), status)


class registerurlsView(BlankView):

    def post(self, request, *args, **kwargs):
    
        url_list = ['10.0.0.1','10.0.0.2',]
    
        E = ElementMaker()
        URLS = E.urls
        URL = E.url
        status=201
        xml = URLS(*map(lambda x: URL(x), url_list))
        return prepxml(etree.tostring(xml), status)


class whoamiView(BlankView):

    def get(self, request, *args, **kwargs):
         return HttpResponse("joe.jasinski+dp@gmail.com", status=200)
