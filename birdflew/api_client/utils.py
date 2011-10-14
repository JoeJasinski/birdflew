from urllib2 import Request, urlopen, URLError, HTTPError
from lxml import etree
from api import validators

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db.models import signals
from django.dispatch import receiver
from django.conf import settings
from bcore.models import UrlModel
from api.forms import RawUrlForm

import socket, urllib2

class TransferException(Exception):
    
    def __init__(self, messages=[], *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.messages = messages




class ClientParser(object):

    def get_url_as_file(self, url):
        
        neighbor_file = None
        socket.setdefaulttimeout(10)
        req = Request(url)
    
        try:
            response = urlopen(req)
            neighbor_file = StringIO(response.read())
        except HTTPError, e:
            #print "HTTP Error:",e.code , url
            raise 
        except URLError, e:
            print "URL ERROR"
            #print "URL Error:",e.reason , url
            raise 
            
        return neighbor_file

    def get_urls_to_check(self):
        urls = cache.get('api_client_urls_to_check', None)
        if not urls:
            urls = list(set(UrlModel.objects.values_list('url', 'id')))
            cache.set('api_client_urls_to_check', urls, settings.DEFAULT_CACHE_TIMEOUT)
        return urls
    
    
    def process(self, *args, **kwargs):
        messages = []
        urls_to_check = self.get_urls_to_check()
        for url_socket, id in urls_to_check:
            messages_loc = self.get_neighbors_urls(url_socket, id)
            print messages_loc
    
    def validate_base_url(self, url_socket):

        valid, messages = validators.validate_url_chars(url_socket)
        if messages:
            raise TransferException(messages=messages)  

        burl, messages_loc = validators.validate_url_format(url_socket)
        messages = messages + messages_loc
        if messages:
            raise TransferException(messages=messages)             
            
        return burl, messages
        
    
    def get_neighbors_urls(self, url_socket, id):
        """ START PARSING HERE """
        messages = []
        print "URL (%s) %s" % (id, url_socket)
        try:
            burl, messages = self.validate_base_url(url_socket)
            url = "%s%s" % (burl.url_socket, reverse('api_lookupurls') )
            neighbor_file = self.get_url_as_file(url)
            form = RawUrlForm(data=neighbor_file.read())
            if form.is_valid():
                parent, created = UrlModel.objects.get_or_create(url=burl.url_socket)
                url_list = form.cleaned_data.get('urls')
                for u in url_list:
                    url_model, created = UrlModel.objects.get_or_create(url=u, 
                            defaults={'parent':parent})
            else:
                messages = messages + form.errors
        except TransferException, e:
            messages = messages + e.messages     
        except urllib2.HTTPError,e :
             messages.append("Returned Http code %s" % e.code) 
        except urllib2.URLError, e:     
             messages.append("%s" % e.reason) 
        #except Exception, e:
        #    messages.append(e.message)

        return messages
            
            
@receiver(signals.post_save, sender=UrlModel)
def del_api_client_urls_to_check(sender, instance, **kwargs):
    cache.delete('api_client_urls_to_check')
     
