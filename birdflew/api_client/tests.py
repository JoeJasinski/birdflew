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
    
    def test_get_tree_from_file(self):
        c = utils.ClientParser()
        tree = c.get_tree_from_file(self.xml_file)
        self.assertTrue(tree, etree._Element)


    def test_get_neighbors_urls(self):
        c = utils.ClientParser()
        root, messages = c.get_neighbors_urls('http://localhost:8000/v1/lookupurls/')
        self.assertTrue(root == None)
        print messages
        self.assertTrue(messages)
        

    def test_get_root_from_tree(self):
        c = utils.ClientParser()
        tree = c.get_tree_from_file(self.xml_file)
        root = c.get_root_from_tree(tree)
        self.assertEqual(root.tag, 'urls')
        self.assertTrue(root, etree._Element)


    def test_get_url_from_root(self):
        c = utils.ClientParser()
        tree = c.get_tree_from_file(self.xml_file)
        root = c.get_root_from_tree(tree)
        children = c.get_url_from_root(root)
        self.assertTrue(len(children) == 2)
        self.assertTrue(children[0].tag == 'url')
        self.assertTrue(children[1].tag == 'url')
        self.assertTrue(isinstance(children[0], etree._Element))
        
        
    def test_get_url(self):
        test_client = Client()
        request = test_client.get(reverse('api_lookupurls'))
        c = utils.ClientParser()
        tree = c.get_tree_from_file(StringIO(request.content))
        root = c.get_root_from_tree(tree)
        children = c.get_url_from_root(root)
        self.assertTrue(len(children) == 2)
        self.assertTrue(children[0].tag == 'url')
        self.assertTrue(children[1].tag == 'url')
        self.assertTrue(isinstance(children[0], etree._Element))
    
    
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

#    def test_get_url_2(self):
#        c = utils.ClientParser()
#        file = c.get_url_as_file("http://%s/%s" % (Site.objects.get_current(), reverse('api_lookupurls')))
#        tree = c.get_tree_from_file(file)
#        root = c.get_root_from_tree(tree)
#        children = c.get_url_from_root(root)
#        self.assertTrue(len(children) == 2)
#        self.assertTrue(children[0].tag == 'url')
#        self.assertTrue(children[1].tag == 'url')
#        self.assertTrue(isinstance(children[0], etree._Element))        
#        