from urllib2 import Request, urlopen, URLError, HTTPError
from lxml import etree
from api import validators
from django.core.urlresolvers import reverse

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from bcore.models import UrlModel
from api.forms import RawUrlForm

class ClientParser(object):

    def get_url_as_file(self, url):
        
        neighbor_file = None
    
        req = Request(url)
    
        try:
            response = urlopen(req)
            neighbor_file = StringIO(response.read())
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
            
        return neighbor_file
    
    def validate_base_url(self, url_socket):

        class BaseURL(): pass

        messages = []
        url, domain, port = None, None, None
        valid, messages = validators.validate_url_chars(url_socket)
        burl = BaseURL()
        if not messages:
            url, domain, port, messages_loc = validators.validate_url_format(url_socket)
        burl.url = url
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
                url = "%s%s" % (url_socket, reverse('api_lookupurls') )
                neighbor_file = self.get_url_as_file(url)
                form = RawUrlForm(data=neighbor_file.read())
                if form.is_valid():
                    url_list = form.cleaned_data.get('urls')
                    for u in url_list:
                        url_model = UrlModel(url=u)
                        url_model.save()
                else:
                    messages = messages + form.errors

            except Exception, e:
                messages.append(e.message)

        
        return root, messages
            
        