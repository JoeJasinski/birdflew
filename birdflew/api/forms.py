import re
from django import forms 
from . import validators
from lxml import etree

class RawUrlForm(object):
        
    def __init__(self, data=""):
        self.raw_data = data
        self.errors = []

    def clean_url(self, url):
        """ Needs implementation """
        if not url:
            self.errors.append("URL cannot be blank.")
            url = ""
        m = re.compile('^[a-zA-Z0-9:._\-+/]+$')
        match = m.match(url)
        if not match:
            self.errors.append("Invalid url input.")
        return url

    def is_valid(self):
        
        self.errors = []
        try:
            radx = etree.fromstring(self.raw_data)
        except Exception, e:
            self.errors.append(e)
    
        if not self.errors:
            relax =  validators.input_message_spec_relaxing()
            result = relax.validate(radx)
            if not relax:
                self.errors.append(relax.error_log)
 
        if not self.errors:
            try:
                url_nodes = map(lambda x: x.text, radx.xpath('/urls/*'))
            except Exception, e:
                self.errors.append(e.exc_info())
        
        if not self.errors:
            if not reduce(lambda y, z: y & z, map(lambda x: bool(x), url_nodes)):
                self.errors.append('urls must not contain null values')
        
        if not self.errors:
            url_nodes = map(lambda x: self.clean_url(x), url_nodes)  
        
        if not self.errors:
            self.cleaned_data = {}
            self.cleaned_data['urls'] = url_nodes 

        return not bool(self.errors)