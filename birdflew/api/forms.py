import re
from lxml import etree
from django import forms 
from . import validators

class RawUrlForm(object):
        
    def __init__(self, data=""):
        self.raw_data = data
        self.errors = []

    def clean_url(self, url):
        
        clean, messages = validators.validate_url_chars(url)

        if not clean:
            self.errors = self.errors + messages
            url = ''
        return url

    def is_valid(self):
        
        self.errors = []
        try:
            radx = etree.fromstring(self.raw_data)
        except Exception, e:
            self.errors.append(e.message)
    
    
        if not self.errors:
            relax =  validators.input_message_spec_relaxing()
            result = relax.validate(radx)
            if not result:
                self.errors.append(relax.error_log)

        if not self.errors:
            try:
                url_nodes = map(lambda x: x.text, radx.xpath('/urls/*'))
            except Exception, e:
                self.errors.append(e.message)
                
        if not self.errors:
            if not reduce(lambda y, z: y & z, map(lambda x: bool(x), url_nodes)):
                self.errors.append('urls must not contain null values')
        
        if not self.errors:
            url_nodes = map(lambda x: self.clean_url(x), url_nodes)  
        
        if not self.errors:
            cleaned_url_pices = []
            cleaned_urls = []
            for url_node in url_nodes:                
                burl, messages = validators.validate_url_format(url_node)

                if messages:
                    self.errors = self.errors + messages
                else:
                    cleaned_urls.append(burl.url_socket)
            
                cleaned_url_pices.append((burl.domain, burl.port))

        if not self.errors:
            self.cleaned_data = {}
            self.cleaned_data['url_pieces'] = cleaned_url_pices 
            self.cleaned_data['urls'] = cleaned_urls 
        
        return (not bool(self.errors))