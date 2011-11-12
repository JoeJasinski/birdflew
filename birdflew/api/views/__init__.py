from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from api.forms import RawUrlForm
from api import validators 

from lxml import etree
from lxml.builder import ElementMaker 

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import View


def prepxml(xml, status, headers={}):
    
    decl = """<?xml version="1.0" encoding="utf-8"?>"""
    response = HttpResponse("%s%s" % (decl, xml), status=status, content_type="application/xml")
    response['Content-Disposition'] = 'inline; filename=output.xml'
    for i, v in headers.items():
        response[i] = v
    return response

def prepxhtml(xml, status, headers={}):
    
    decl = """<?xml version="1.0" encoding="utf-8"?>"""
    response = HttpResponse("%s%s" % (decl, xml), status=status, content_type="application/xhtml+xml")
    response['Content-Disposition'] = 'inline; filename=output.xhtml'
    for i, v in headers.items():
        response[i] = v
    return response


class Emitter(object):
    pass

class XMLEmitter(Emitter):
    type = 'xml'
    
    def run(self, xml, status, headers={}):
        return prepxml(xml, status, headers)
        
class XHTMLEmitter(Emitter):
    type = 'xhtml'
    
    def run(self, xml, status, headers={}):
        return prepxhtml(xml, status, headers)



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


def xml_to_xslt(xml, template, context={} ):
    t = loader.get_template(template)
    c = Context(context)
    rendered = t.render(c)
    xslt = etree.XSLT(etree.fromstring(rendered))
    return xslt(xml)


class BlankView(View):
    
    def _xml_error(self, message):
        return etree.tostring(messagexml(message))
        
    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)

    @method_decorator(validators.RateLimitDecorator)
    def post(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)

    @method_decorator(validators.RateLimitDecorator)
    def put(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)

    @method_decorator(validators.RateLimitDecorator)
    def delete(self, request, *args, **kwargs):
        return prepxml(self._xml_error('Method not allowed'), status=405)
