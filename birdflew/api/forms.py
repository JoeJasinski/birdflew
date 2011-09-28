from django import forms 
from . import validators
from lxml import etree

class RawUrlForm(object):
        
    def __init__(self, data=""):
        self.raw_data = data
        self.errors = []

    def clean_url(self, url):
        """ Needs implementation """
        return url

    def is_valid(self):
        stop = False
        try:
            radx = etree.fromstring(self.raw_data)
        except Exception, e:
            stop = True
            self.errors.append(e)
            
        if not stop:
            relax =  validators.input_message_spec_relaxing()
            result = relax.validate(radx)
            stop = not relax 
            if not relax:
                self.errors.append(relax.error_log)
            
        if not stop:
            url_nodes = map(lambda x: self.clean_url(x.get('url')), radx.xpath('/urls/*'))
            
            if not reduce(lambda y, z: y & z, map(lambda x: bool(x), url_nodes)):
                stop = True
                self.errors.append('urls must not contain null values')
        
        if not stop:
            self.cleaned_data = {}
            self.cleaned_data['urls'] = url_nodes 
        
        return not stop