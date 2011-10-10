import re
from urlparse import urlparse
from lxml import etree
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

input_message_spec = """<element name="urls" xmlns="http://relaxng.org/ns/structure/1.0">
  <oneOrMore>
    <element name="url">
      <text/>
    </element>
  </oneOrMore>
</element>
"""

def input_message_spec_relaxing():
    xml = etree.fromstring(input_message_spec)
    return etree.RelaxNG(xml)


def validate_url_chars(url):
    messages = []
    if not url:
        messages.append("URL cannot be blank.")

    if not messages:
        m = re.compile('^[a-zA-Z0-9:._\-+/]+$')
        match = m.match(url)
        if not match:         
            messages.append("Invalid URL characters.")

    return (not bool(messages), messages)


def validate_url_format(url):

    # normalize the output
    messages = []
    domain = ""
    port = ""
    m = re.compile('^http[s]?://')
    if not m.match(url):
        url = "http://%s" % url
    
    try:
        up = urlparse(url)
    except ValueError:
        messages.append("Improper port value. Must be an integer. ")
    domain = up.hostname
    
    if not domain:
        messages.append("No hostname given.")

    if not messages:
        port = None

        try:
            port = int(up.port)
        except ValueError:
            pass    
        except TypeError:
            pass
        
        if not port:
            port = 80
    
    url = "%s%s:%s" % (up.schema, domain, port)
    
    return (url, domain, port, messages)


class RateLimitDecorator(object):
    def __init__(self, orig_func):
        self.orig_func = orig_func
        self.__name__ = orig_func.__name__
        
    __name__ = 'rate_limit'

    def __call__(self,  *args, **kwargs):
        # influenced by http://charlesleifer.com/blog/django-patterns-view-decorators/
        request = args[0]
        remote_addr = request.META.get('REMOTE_ADDR')
        key = '%s.%s' % (remote_addr, request.get_full_path())
        allow = True
        view_count = cache.get(key, '')
        if view_count:
            if view_count >= settings.DEFAULT_MAX_REQUESTS_PER_INTERVAL:
                allow = False
            else:
                allow = True
                cache.incr(key)
        else:
            cache.set(key, 1, settings.DEFAULT_CACHE_RATE_LIMIT)
            allow = True
        
        if not allow:
            response = HttpResponse("throttled", status=403, content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=test.txt'
            return response
        
        return self.orig_func(*args, **kwargs)
    
    