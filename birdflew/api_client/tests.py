"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.test import TestCase, Client
from api_client import utils
from api.forms import RawUrlForm
from lxml import etree

from bcore.models import UrlModel

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO



class SimpleTest(TestCase):
    
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ClientTest(TestCase):
    
    class ClientParserTester(utils.ClientParser):
        
        def __init__(self, xml, *args, **kwargs):
            self.xml = xml 
            super(self.__class__, self).__init__(*args, **kwargs)
          
    
        def get_url_as_file(self, url): 

            neighbor_file = StringIO(self.xml)       
            return neighbor_file    
    
    
    def setUp(self):
        self.xml = """<?xml version="1.0" encoding="UTF-8" ?>
            <urls>
              <url>%s</url>
              <url>%s</url>
            </urls>"""


        self.xml2 = """<?xml version="1.0" encoding="UTF-8" ?>
            <urls>
              <url>%s</url>
              <url>%s</url>
            """
        
        
        self.xml_urls = ('192.168.0.1','127.0.0.1')
        
        UrlModel(url="192.168.0.1:80").save()
        UrlModel(url="10.10.0.1:80").save()        
        

        self.xml_file = StringIO(self.xml % self.xml_urls)
        self.xml_file2 = StringIO(self.xml2 % self.xml_urls)
    


    def test_get_neighbors_urls(self):
        c = utils.ClientParser()
        root, messages = c.get_neighbors_urls('http://localhost:8000/')
        self.assertTrue(not messages)


    def test_get_neighbors_urls(self):
        c = utils.ClientParser()
        burl, messages = c.validate_base_url('http://192.168.9.1')
        self.assertTrue(not messages)
        burl, messages = c.validate_base_url('http://192.168.9.1:8000')
        self.assertTrue(not messages)
        self.assertEqual(burl.port, 8000)
        burl, messages = c.validate_base_url('http://192.168.9.1: 80')
        self.assertTrue(messages)        
        burl, messages = c.validate_base_url('http://192.168.9.1:a80')
        self.assertTrue(not messages)
        self.assertEqual(burl.port, 80)
        burl, messages = c.validate_base_url('192.168.9.1:80')
        self.assertTrue(not messages)     
        burl, messages = c.validate_base_url('www.google.com:80')
        self.assertTrue(not messages)  
        burl, messages = c.validate_base_url('www. google.com:80')
        self.assertTrue(messages) 
        

    def test_get_neighborhood_urls2(self):
        c = self.ClientParserTester(xml=self.xml % self.xml_urls)
        root, messages = c.get_neighbors_urls('http://localhost:8000/')
        self.assertTrue(not messages)        
        

    def test_get_neighborhood_urls2(self):
        c = self.ClientParserTester(xml=self.xml2 % self.xml_urls)
        root, messages = c.get_neighbors_urls('http://localhost:8000/')
        self.assertTrue(messages)  
    
    
    def test_get_urls_to_check(self):
        
        c = utils.ClientParser()
        urls = c.get_urls_to_check()
        self.assertEqual(set(['192.168.0.1:80','10.10.0.1:80']), set(urls))
    
    
    def test_forms_1(self):
        form = RawUrlForm(data=self.xml % self.xml_urls)
        self.assertTrue(form.is_valid())
        self.assertTrue(hasattr(form, 'cleaned_data'))
        self.assertEqual(
            form.cleaned_data.get('urls',''), list(self.xml_urls) )


    def test_forms_2(self):
        test_urls = ("http://192.168.0.9:80","localhost")
        form = RawUrlForm(data=self.xml % test_urls)
        self.assertTrue(form.is_valid())
        self.assertTrue(hasattr(form, 'cleaned_data'))
        self.assertEqual(
            form.cleaned_data.get('urls',''), list(test_urls) )
        self.assertEqual(form.cleaned_data.get('url_pieces'),
                         [('192.168.0.9', 80), ('localhost', 80)])

    def test_forms_3(self):
        test_urls = ("http://192.168.0.9:80/","localhost")
        form = RawUrlForm(data=self.xml % test_urls)
        self.assertTrue(form.is_valid())
        self.assertTrue(hasattr(form, 'cleaned_data'))
        self.assertEqual(
            form.cleaned_data.get('urls',''), list(test_urls) )
        self.assertEqual(form.cleaned_data.get('url_pieces'),
                         [('192.168.0.9', 80), ('localhost', 80)])


    def test_forms_4(self):
        test_urls = ("http://192.168.0.9:80/","local host")
        form = RawUrlForm(data=self.xml % test_urls)
        self.assertTrue(not form.is_valid())
        self.assertTrue(not hasattr(form, 'cleaned_data'))
        self.assertEqual(len(form.errors), 1)


    def test_forms_5(self):
        test_urls = ("http://192.168.0.9: 80/","local host")
        form = RawUrlForm(data=self.xml % test_urls)
        self.assertTrue(not form.is_valid())
        self.assertTrue(not hasattr(form, 'cleaned_data'))
        self.assertEqual(len(form.errors), 2)


    def test_forms_6(self):
        test_urls = ("http://192.1()68.0.9:80/","local*&^@!host")
        form = RawUrlForm(data=self.xml % test_urls)
        self.assertTrue(not form.is_valid())
        self.assertTrue(not hasattr(form, 'cleaned_data'))
        self.assertEqual(len(form.errors), 1)
        
    def test_forms_7(self):
        form = RawUrlForm(data=self.xml2 % self.xml_urls)
        self.assertTrue(not form.is_valid())
        self.assertTrue(not hasattr(form, 'cleaned_data'))
        self.assertEqual(len(form.errors), 1)

    def test_forms_8(self):
        form = RawUrlForm(data='' )
        self.assertTrue(not form.is_valid())
        self.assertTrue(not hasattr(form, 'cleaned_data'))
        self.assertEqual(len(form.errors), 1)

    def test_forms_9(self):
        form = RawUrlForm(data='<response />' )
        self.assertTrue(not form.is_valid())
        self.assertTrue(not hasattr(form, 'cleaned_data'))
        self.assertEqual(len(form.errors), 1)

   