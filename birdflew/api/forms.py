import re
from lxml import etree
from django import forms 
from django.contrib.auth.models import User
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
        
        cleaned_url_pices = None
        cleaned_url = None
        
        self.errors = []
        try:
            radx = etree.fromstring(self.raw_data)
        except Exception, e:
            self.errors.append(e.message)
    
    
        if not self.errors:
            relax =  validators.input_message_spec_relaxing(validators.input_url_message_spec)
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
    

class RawUserForm(object):

    def __init__(self, data=""):
        self.raw_data = data
        self.errors = []
        

    def is_valid(self):
        self.errors = []
        cleaned_username = ''
        
        try:
            radx = etree.fromstring(self.raw_data)
        except Exception, e:
            self.errors.append(e.message)
    
        if not self.errors:
            relax =  validators.input_message_spec_relaxing(validators.input_user_message_spec)
            result = relax.validate(radx)
            if not result:
                self.errors.append(relax.error_log)

        if not self.errors:
            try:
                username = map(lambda x: x.text, radx.xpath('/user/email'))[0]
            except Exception, e:
                self.errors.append(e.message)
        
        if not self.errors:
            cleaned_username, messages = validators.validate_email(username)
            self.errors += messages 
            
        if not self.errors:
            if len(User.objects.filter(email=cleaned_username)):
                self.errors.append('Username already exists.')
        
        if not self.errors:
            self.cleaned_data = {}
            self.cleaned_data['username'] = cleaned_username 
        
        return (not bool(self.errors))
           

class RawBookmarkForm(object):
        
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
        cleaned_categories = []
        cleaned_comments = []
        try:
            radx = etree.fromstring(self.raw_data)
        except Exception, e:
            self.errors.append(e.message)
    
    
        if not self.errors:
            relax =  validators.input_message_spec_relaxing(validators.input_bookmark_message_spec)
            result = relax.validate(radx)
            if not result:
                self.errors.append(relax.error_log)

        if not self.errors:
            try:
                uri = map(lambda x: x.text, radx.xpath('/url/uri'))[0]
            except Exception, e:
                self.errors.append(e.message)

            try:
                categories = map(lambda x: x.text, radx.xpath('/url/categories/category'))
            except Exception, e:
                self.errors.append(e.message)
            
            try:
                comments = map(lambda x: x.text, radx.xpath('/url/comments/comment'))
            except Exception, e:
                self.errors.append(e.message)
        
        if not self.errors:
            cleaned_uri, messages = validators.validate_url_format(uri)
            if messages:
                self.errors += messages
            
            for category in categories:
                cleaned_category, messages = validators.validate_category(category)
                self.errors += messages 
                if not self.errors:
                    cleaned_categories.append(cleaned_category)
            for comment in comments:
                cleaned_comment, messages = validators.validate_comment(comment)
                self.errors += messages
                if not self.errors:
                    cleaned_comments.append(cleaned_comment)

        if not self.errors:
            self.cleaned_data = {}
            self.cleaned_data['uri'] = cleaned_uri 
            self.cleaned_data['categories'] = cleaned_categories 
            self.cleaned_data['comments'] = cleaned_comments 
        
        return (not bool(self.errors))