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
from django.conf import settings
from bcore.models import UrlModel
from api.forms import RawUrlForm

class ClientParser(object):

    def get_url_as_file(self, url):
        
        neighbor_file = None

        req = Request(url, timetout=5)
    
        try:
            response = urlopen(req)
            neighbor_file = StringIO(response.read())
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
            
        return neighbor_file

    def get_urls_to_check(self):
        urls = cache.get('api_client_urls_to_check', None)
        if not urls:
            urls = UrlModel.objects.values_list('url', flat=True)
            cache.set('api_client_urls_to_check', urls, settings.DEFAULT_CACHE_TIMEOUT)
        return urls
    
    
    def process(self, *args, **kwargs):
        urls_to_check = self.get_urls_to_check()
        print urls_to_check
        for url_socket in urls_to_check:
            self.get_neighbors_urls(url_socket)
    
    def validate_base_url(self, url_socket):

        class BaseURL(): pass

        messages = []
        domain, port = None, None
        valid, messages = validators.validate_url_chars(url_socket)
        burl = BaseURL()
        if not messages:
            url_socket, domain, port, messages_loc = validators.validate_url_format(url_socket)
        burl.url_socket = url_socket
        burl.domain = domain
        burl.port = port
            
        return burl, messages
        
    
    def get_neighbors_urls(self, url_socket):
        """ START PARSING HERE """
        root = None
        url_socket = url_socket.rstrip("/")

        burl, messages = self.validate_base_url(url_socket)
        
        if not messages:
            try:
                url = "%s%s" % (burl.url_socket, reverse('api_lookupurls') )
                neighbor_file = self.get_url_as_file(url)
                form = RawUrlForm(data=neighbor_file.read())
                if form.is_valid():
                    parent = UrlModel.objects.get_or_create(url=burl.url_socket)
                    url_list = form.cleaned_data.get('urls')
                    for u in url_list:
                        url_model, created = UrlModel.objects.get_or_create(url=u, 
                                defaults={'parent':parent})
                else:
                    messages = messages + form.errors

            except Exception, e:
                messages.append(e.message)

        return root, messages
            

def del_api_client_urls_to_check(sender, instance, **kwargs):
    cache.delete('api_client_urls_to_check')
signals.post_save.connect(api_client_urls_to_check)        