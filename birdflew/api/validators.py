import re
from urlparse import urlparse
from lxml import etree


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
    
    return (url, domain, port, messages)