from django import forms 
from . import validators
from lxml import etree

class RawUrlForm(object):
        
    def __init__(self, raw_data=""):
        self.raw_data = raw_data
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
            
        if not stop:
            url_nodes = map(lambda x: self.clean(x.get('url')), radx.xpath('/urls/*'))
            self.cleaned_data = {}
            self.cleaned_data['urls'] = url_nodes 
        else:
            self.errors.append(relax.error_log)
        
        return not stop